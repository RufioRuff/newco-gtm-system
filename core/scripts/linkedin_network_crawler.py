#!/usr/bin/env python3
"""
LinkedIn Network Crawler for Multi-Degree Connections

Crawls 1st, 2nd, 3rd, and 4th degree connections to build comprehensive
network graph for social network analysis.

Uses BFS (Breadth-First Search) to traverse the network systematically.
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from collections import deque
from typing import Dict, List, Set
from linkedin_scraper import LinkedInScraper

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
NETWORK_DIR = DATA_DIR / "linkedin_networks"
NETWORK_DIR.mkdir(parents=True, exist_ok=True)


class LinkedInNetworkCrawler:
    """Crawl multi-degree LinkedIn networks"""

    def __init__(self):
        self.scraper = LinkedInScraper()
        self.visited_profiles: Set[str] = set()
        self.network_graph: Dict[str, Dict] = {}
        self.relationships: List[Dict] = []

    async def crawl_network(
        self,
        seed_profile_url: str,
        max_degrees: int = 4,
        max_connections_per_profile: int = 100,
        max_total_profiles: int = 500
    ):
        """
        Crawl multi-degree network starting from seed profile

        Args:
            seed_profile_url: Starting LinkedIn profile URL
            max_degrees: Maximum degrees of separation to crawl (1-4)
            max_connections_per_profile: Max connections to scrape per profile
            max_total_profiles: Maximum total profiles to scrape

        Returns:
            Network graph data structure
        """
        print("\n" + "="*70)
        print("🕸️  LINKEDIN NETWORK CRAWLER")
        print("="*70)
        print(f"Seed profile: {seed_profile_url}")
        print(f"Max degrees: {max_degrees}")
        print(f"Max connections per profile: {max_connections_per_profile}")
        print(f"Max total profiles: {max_total_profiles}")
        print("="*70 + "\n")

        await self.scraper.init_browser()
        await self.scraper.login()

        # BFS queue: (profile_url, degree, parent_url)
        queue = deque([(seed_profile_url, 0, None)])
        profiles_scraped = 0

        while queue and profiles_scraped < max_total_profiles:
            profile_url, degree, parent_url = queue.popleft()

            # Skip if already visited
            if profile_url in self.visited_profiles:
                continue

            # Skip if exceeding max degrees
            if degree > max_degrees:
                continue

            print(f"\n{'  ' * degree}📊 [Degree {degree}] Scraping: {profile_url}")

            try:
                # Scrape profile
                profile_data = await self.scraper.scrape_profile(profile_url)
                profiles_scraped += 1

                # Add to network graph
                profile_id = self._normalize_profile_url(profile_url)
                self.network_graph[profile_id] = {
                    **profile_data,
                    'degree': degree,
                    'profile_url': profile_url
                }

                # Mark as visited
                self.visited_profiles.add(profile_url)

                # Record relationship with parent
                if parent_url:
                    parent_id = self._normalize_profile_url(parent_url)
                    self.relationships.append({
                        'from': parent_id,
                        'to': profile_id,
                        'degree_from_seed': degree
                    })

                # Scrape connections if not at max degree
                if degree < max_degrees:
                    print(f"{'  ' * degree}👥 Scraping connections...")

                    connections = await self.scraper.scrape_connections(
                        profile_url,
                        max_connections=max_connections_per_profile
                    )

                    # Add connections to queue
                    for conn in connections:
                        if conn.get('profile_url'):
                            conn_url = conn['profile_url']
                            if conn_url not in self.visited_profiles:
                                queue.append((conn_url, degree + 1, profile_url))

                    print(f"{'  ' * degree}✅ Added {len(connections)} connections to queue")

                # Progress update
                print(f"\n{'='*70}")
                print(f"Progress: {profiles_scraped}/{max_total_profiles} profiles | Queue: {len(queue)} | Degree: {degree}")
                print(f"{'='*70}")

                # Rate limiting
                await asyncio.sleep(2)

            except Exception as e:
                print(f"❌ Error scraping {profile_url}: {e}")
                continue

        print("\n" + "="*70)
        print("✅ NETWORK CRAWLING COMPLETE")
        print("="*70)
        print(f"Total profiles scraped: {profiles_scraped}")
        print(f"Total relationships: {len(self.relationships)}")
        print(f"Network size by degree:")

        # Count by degree
        degree_counts = {}
        for profile_id, data in self.network_graph.items():
            degree = data['degree']
            degree_counts[degree] = degree_counts.get(degree, 0) + 1

        for degree in sorted(degree_counts.keys()):
            print(f"  Degree {degree}: {degree_counts[degree]} profiles")

        print("="*70 + "\n")

        await self.scraper.close()

        return {
            'network_graph': self.network_graph,
            'relationships': self.relationships,
            'metadata': {
                'seed_profile': seed_profile_url,
                'total_profiles': profiles_scraped,
                'total_relationships': len(self.relationships),
                'max_degrees': max_degrees,
                'scraped_at': datetime.now().isoformat()
            }
        }

    def _normalize_profile_url(self, url: str) -> str:
        """Extract profile ID from URL"""
        # Extract username from URL like https://www.linkedin.com/in/username/
        if '/in/' in url:
            parts = url.split('/in/')[1].split('/')[0].split('?')[0]
            return parts
        return url

    def save_network(self, network_data: Dict, filename: str):
        """Save network data to JSON"""
        output_file = NETWORK_DIR / f"{filename}.json"

        with open(output_file, 'w') as f:
            json.dump(network_data, f, indent=2)

        print(f"💾 Network saved to: {output_file}")

        # Also save in formats for different tools

        # 1. Save as edge list for network analysis
        edge_file = NETWORK_DIR / f"{filename}_edges.csv"
        with open(edge_file, 'w') as f:
            f.write("source,target,degree\n")
            for rel in network_data['relationships']:
                f.write(f"{rel['from']},{rel['to']},{rel['degree_from_seed']}\n")
        print(f"💾 Edge list saved to: {edge_file}")

        # 2. Save as node list
        node_file = NETWORK_DIR / f"{filename}_nodes.csv"
        with open(node_file, 'w') as f:
            f.write("id,name,headline,company,location,degree,connection_count\n")
            for profile_id, data in network_data['network_graph'].items():
                name = data.get('name', '').replace(',', ';')
                headline = data.get('headline', '').replace(',', ';')
                company = data.get('current_position', {}).get('company', '').replace(',', ';')
                location = data.get('location', '').replace(',', ';')
                degree = data.get('degree', 0)
                conn_count = data.get('connection_count', 0)

                f.write(f"{profile_id},{name},{headline},{company},{location},{degree},{conn_count}\n")
        print(f"💾 Node list saved to: {node_file}")

        return output_file


async def crawl_jason_goldman_network():
    """Crawl Jason Goldman's multi-degree network"""

    crawler = LinkedInNetworkCrawler()

    # First, find Jason Goldman's profile
    await crawler.scraper.init_browser()
    await crawler.scraper.login()

    profile_url = await crawler.scraper.search_person("Jason Eliot Goldman", "G2 Insurance")

    if not profile_url:
        profile_url = await crawler.scraper.search_person("Jason Goldman", "Evil Twin")

    if not profile_url:
        print("❌ Could not find Jason Goldman's profile")
        print("   Enter LinkedIn URL manually: ", end='')
        profile_url = input().strip()

    await crawler.scraper.close()

    if profile_url:
        print(f"\n✅ Found profile: {profile_url}\n")

        # Crawl network
        network_data = await crawler.crawl_network(
            seed_profile_url=profile_url,
            max_degrees=4,  # 1st, 2nd, 3rd, 4th degree
            max_connections_per_profile=50,  # Balance between completeness and speed
            max_total_profiles=500  # Limit total profiles to avoid excessive scraping
        )

        # Save network
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        crawler.save_network(network_data, f'jason_goldman_network_{timestamp}')

        return network_data
    else:
        print("❌ No profile URL provided")
        return None


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         LinkedIn Multi-Degree Network Crawler                ║
║              For NEWCO Network Effects Engine                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

This script will crawl Jason Goldman's LinkedIn network up to 4 degrees
of separation, building a comprehensive network graph.

⚠️  WARNING:
  - This will make many requests to LinkedIn
  - Use responsibly and respect LinkedIn's Terms of Service
  - Consider starting with max_degrees=2 for testing
  - Expect this to take 30-60 minutes for full 4-degree crawl

Network Analysis:
  - 1st degree: Direct connections
  - 2nd degree: Connections of connections (most valuable for network effects)
  - 3rd degree: Friends of friends of friends
  - 4th degree: Extended network reach

Requirements:
  export LINKEDIN_EMAIL="your@email.com"
  export LINKEDIN_PASSWORD="yourpassword"

Press Enter to start (Ctrl+C to cancel)...
""")

    input()

    asyncio.run(crawl_jason_goldman_network())

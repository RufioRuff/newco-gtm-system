#!/usr/bin/env python3
"""
LinkedIn Profile Scraper for NEWCO Network Effects Engine

Scrapes LinkedIn profiles to extract:
- Profile information (name, title, company, location)
- Work history
- Connections (where visible)
- Mutual connections
- Skills and endorsements

Note: LinkedIn has strict anti-scraping policies. This script:
1. Uses Playwright for browser automation (handles JavaScript)
2. Respects rate limits
3. Requires authentication
4. Should be used responsibly and in compliance with LinkedIn's Terms of Service
"""

import asyncio
import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

try:
    from playwright.async_api import async_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not installed. Install with: pip install playwright && playwright install chromium")

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "data" / "linkedin_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class LinkedInScraper:
    """Scrape LinkedIn profiles with authentication"""

    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        self.email = email or os.getenv('LINKEDIN_EMAIL')
        self.password = password or os.getenv('LINKEDIN_PASSWORD')
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def init_browser(self):
        """Initialize Playwright browser"""
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright not available. Install with: pip install playwright && playwright install chromium")

        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=False,  # Set to True for headless mode
            args=['--disable-blink-features=AutomationControlled']
        )

        # Create context with realistic user agent
        context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )

        self.page = await context.new_page()

    async def login(self):
        """Login to LinkedIn"""
        if not self.email or not self.password:
            raise ValueError("LinkedIn credentials required. Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables.")

        print("🔐 Logging in to LinkedIn...")

        await self.page.goto('https://www.linkedin.com/login')
        await self.page.wait_for_load_state('networkidle')

        # Fill login form
        await self.page.fill('input[name="session_key"]', self.email)
        await self.page.fill('input[name="session_password"]', self.password)
        await self.page.click('button[type="submit"]')

        # Wait for navigation
        try:
            await self.page.wait_for_url('**/feed/**', timeout=10000)
            print("✅ Successfully logged in")
        except:
            # Check if we need to handle verification
            if 'checkpoint' in self.page.url or 'challenge' in self.page.url:
                print("⚠️  LinkedIn security checkpoint detected.")
                print("    Please complete the verification in the browser window.")
                print("    Press Enter when done...")
                input()
                await self.page.wait_for_url('**/feed/**', timeout=60000)
                print("✅ Successfully logged in after verification")
            else:
                raise Exception("Login failed. Check credentials.")

    async def scrape_profile(self, profile_url: str) -> Dict:
        """
        Scrape a LinkedIn profile

        Args:
            profile_url: LinkedIn profile URL (e.g., 'https://www.linkedin.com/in/username')

        Returns:
            Dictionary with profile data
        """
        print(f"\n🔍 Scraping profile: {profile_url}")

        await self.page.goto(profile_url)
        await self.page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)  # Additional wait for dynamic content

        profile_data = {
            'url': profile_url,
            'scraped_at': datetime.now().isoformat(),
        }

        try:
            # Extract basic profile information
            profile_data['name'] = await self._extract_name()
            profile_data['headline'] = await self._extract_headline()
            profile_data['location'] = await self._extract_location()
            profile_data['about'] = await self._extract_about()

            # Extract current position
            profile_data['current_position'] = await self._extract_current_position()

            # Extract work experience
            profile_data['experience'] = await self._extract_experience()

            # Extract education
            profile_data['education'] = await self._extract_education()

            # Extract skills (limited without scrolling)
            profile_data['skills'] = await self._extract_skills()

            # Extract connection count
            profile_data['connection_count'] = await self._extract_connection_count()

            print(f"✅ Scraped profile: {profile_data['name']}")

        except Exception as e:
            print(f"❌ Error scraping profile: {e}")
            profile_data['error'] = str(e)

        return profile_data

    async def scrape_connections(self, profile_url: str, max_connections: int = 100) -> List[Dict]:
        """
        Scrape visible connections from a profile

        Note: LinkedIn only shows mutual connections and limited 1st-degree connections
        without being connected yourself.
        """
        print(f"\n👥 Scraping connections from: {profile_url}")

        # Navigate to connections page (if accessible)
        connections_url = profile_url.rstrip('/') + '/details/connections/'

        try:
            await self.page.goto(connections_url)
            await self.page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)

            connections = []

            # Scroll to load more connections
            for _ in range(min(max_connections // 10, 10)):
                await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(1)

            # Extract connection cards
            connection_cards = await self.page.query_selector_all('.mn-connection-card')

            for card in connection_cards[:max_connections]:
                try:
                    connection_data = await self._extract_connection_card(card)
                    connections.append(connection_data)
                except:
                    continue

            print(f"✅ Scraped {len(connections)} connections")
            return connections

        except Exception as e:
            print(f"⚠️  Could not access connections (may require being connected): {e}")
            return []

    async def search_person(self, name: str, company: Optional[str] = None) -> Optional[str]:
        """
        Search for a person on LinkedIn and return their profile URL

        Args:
            name: Person's name
            company: Optional company name to narrow search

        Returns:
            Profile URL if found, None otherwise
        """
        search_query = name
        if company:
            search_query += f" {company}"

        print(f"\n🔍 Searching for: {search_query}")

        search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query.replace(' ', '%20')}"

        await self.page.goto(search_url)
        await self.page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

        # Get first result
        try:
            first_result = await self.page.query_selector('.reusable-search__result-container')
            if first_result:
                link = await first_result.query_selector('a.app-aware-link')
                if link:
                    profile_url = await link.get_attribute('href')
                    # Clean URL (remove query params)
                    profile_url = profile_url.split('?')[0]
                    print(f"✅ Found profile: {profile_url}")
                    return profile_url
        except Exception as e:
            print(f"❌ Search failed: {e}")

        return None

    # Helper extraction methods

    async def _extract_name(self) -> str:
        """Extract profile name"""
        try:
            name_elem = await self.page.query_selector('h1.text-heading-xlarge')
            if name_elem:
                return await name_elem.inner_text()
        except:
            pass
        return ""

    async def _extract_headline(self) -> str:
        """Extract profile headline"""
        try:
            headline_elem = await self.page.query_selector('.text-body-medium.break-words')
            if headline_elem:
                return await headline_elem.inner_text()
        except:
            pass
        return ""

    async def _extract_location(self) -> str:
        """Extract location"""
        try:
            location_elem = await self.page.query_selector('.text-body-small.inline.t-black--light.break-words')
            if location_elem:
                return await location_elem.inner_text()
        except:
            pass
        return ""

    async def _extract_about(self) -> str:
        """Extract about section"""
        try:
            # Click "see more" if present
            see_more = await self.page.query_selector('#about ~ div button[aria-label*="more"]')
            if see_more:
                await see_more.click()
                await asyncio.sleep(0.5)

            about_elem = await self.page.query_selector('#about ~ div .display-flex.ph5.pv3')
            if about_elem:
                return await about_elem.inner_text()
        except:
            pass
        return ""

    async def _extract_current_position(self) -> Dict:
        """Extract current position"""
        try:
            exp_section = await self.page.query_selector('#experience ~ div ul li:first-child')
            if exp_section:
                title_elem = await exp_section.query_selector('.t-bold span[aria-hidden="true"]')
                company_elem = await exp_section.query_selector('.t-14.t-normal span[aria-hidden="true"]')

                title = await title_elem.inner_text() if title_elem else ""
                company = await company_elem.inner_text() if company_elem else ""

                return {
                    'title': title,
                    'company': company
                }
        except:
            pass
        return {}

    async def _extract_experience(self) -> List[Dict]:
        """Extract work experience"""
        experience = []
        try:
            exp_items = await self.page.query_selector_all('#experience ~ div ul li')

            for item in exp_items[:10]:  # Limit to 10 most recent
                try:
                    title_elem = await item.query_selector('.t-bold span[aria-hidden="true"]')
                    company_elem = await item.query_selector('.t-14.t-normal span[aria-hidden="true"]')
                    date_elem = await item.query_selector('.t-14.t-normal.t-black--light span[aria-hidden="true"]')

                    title = await title_elem.inner_text() if title_elem else ""
                    company = await company_elem.inner_text() if company_elem else ""
                    date_range = await date_elem.inner_text() if date_elem else ""

                    if title or company:
                        experience.append({
                            'title': title,
                            'company': company,
                            'date_range': date_range
                        })
                except:
                    continue
        except:
            pass
        return experience

    async def _extract_education(self) -> List[Dict]:
        """Extract education"""
        education = []
        try:
            edu_items = await self.page.query_selector_all('#education ~ div ul li')

            for item in edu_items[:5]:
                try:
                    school_elem = await item.query_selector('.t-bold span[aria-hidden="true"]')
                    degree_elem = await item.query_selector('.t-14.t-normal span[aria-hidden="true"]')

                    school = await school_elem.inner_text() if school_elem else ""
                    degree = await degree_elem.inner_text() if degree_elem else ""

                    if school:
                        education.append({
                            'school': school,
                            'degree': degree
                        })
                except:
                    continue
        except:
            pass
        return education

    async def _extract_skills(self) -> List[str]:
        """Extract skills (limited without scrolling to skills section)"""
        skills = []
        try:
            skill_items = await self.page.query_selector_all('#skills ~ div ul li')

            for item in skill_items[:10]:
                try:
                    skill_elem = await item.query_selector('.t-bold span[aria-hidden="true"]')
                    if skill_elem:
                        skill = await skill_elem.inner_text()
                        skills.append(skill)
                except:
                    continue
        except:
            pass
        return skills

    async def _extract_connection_count(self) -> int:
        """Extract connection count"""
        try:
            conn_elem = await self.page.query_selector('.t-black--light.t-normal span:has-text("connection")')
            if conn_elem:
                text = await conn_elem.inner_text()
                # Extract number from text like "500+ connections"
                match = re.search(r'(\d+)', text)
                if match:
                    return int(match.group(1))
        except:
            pass
        return 0

    async def _extract_connection_card(self, card) -> Dict:
        """Extract data from a connection card"""
        name_elem = await card.query_selector('.mn-connection-card__name')
        occupation_elem = await card.query_selector('.mn-connection-card__occupation')
        link_elem = await card.query_selector('a')

        name = await name_elem.inner_text() if name_elem else ""
        occupation = await occupation_elem.inner_text() if occupation_elem else ""
        profile_url = await link_elem.get_attribute('href') if link_elem else ""

        return {
            'name': name,
            'occupation': occupation,
            'profile_url': profile_url.split('?')[0] if profile_url else ""
        }

    def save_cache(self, profile_data: Dict, filename: str):
        """Save scraped data to cache"""
        cache_file = CACHE_DIR / f"{filename}.json"
        with open(cache_file, 'w') as f:
            json.dump(profile_data, f, indent=2)
        print(f"💾 Saved to cache: {cache_file}")

    def load_cache(self, filename: str) -> Optional[Dict]:
        """Load cached profile data"""
        cache_file = CACHE_DIR / f"{filename}.json"
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None

    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()


async def scrape_jason_goldman():
    """Scrape Jason Eliot Goldman's profile"""

    scraper = LinkedInScraper()

    try:
        await scraper.init_browser()
        await scraper.login()

        # Search for Jason Goldman
        print("\n" + "="*70)
        print("Searching for Jason Eliot Goldman...")
        print("="*70)

        # Try multiple search queries
        profile_url = await scraper.search_person("Jason Eliot Goldman", "G2 Insurance")

        if not profile_url:
            profile_url = await scraper.search_person("Jason Goldman", "Evil Twin")

        if not profile_url:
            print("❌ Could not find profile. Please provide the LinkedIn URL manually.")
            print("   Enter URL (or press Enter to skip): ", end='')
            manual_url = input().strip()
            if manual_url:
                profile_url = manual_url

        if profile_url:
            # Scrape profile
            profile_data = await scraper.scrape_profile(profile_url)

            # Save to cache
            scraper.save_cache(profile_data, 'jason_goldman_profile')

            # Try to scrape connections (may be limited)
            connections = await scraper.scrape_connections(profile_url, max_connections=50)

            if connections:
                scraper.save_cache({'connections': connections}, 'jason_goldman_connections')

            print("\n" + "="*70)
            print("✅ SCRAPING COMPLETE")
            print("="*70)
            print(f"Profile: {profile_data.get('name', 'Unknown')}")
            print(f"Headline: {profile_data.get('headline', 'N/A')}")
            print(f"Current: {profile_data.get('current_position', {}).get('title', 'N/A')} at {profile_data.get('current_position', {}).get('company', 'N/A')}")
            print(f"Connections scraped: {len(connections)}")
            print(f"\nData saved to: {CACHE_DIR}/")

            return profile_data, connections
        else:
            print("❌ No profile found")
            return None, []

    except Exception as e:
        print(f"\n❌ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
        return None, []

    finally:
        await scraper.close()


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              LinkedIn Profile Scraper for NEWCO              ║
║                  Network Effects Engine                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

This script will scrape Jason Eliot Goldman's LinkedIn profile.

Requirements:
  1. Set environment variables:
     export LINKEDIN_EMAIL="your@email.com"
     export LINKEDIN_PASSWORD="yourpassword"

  2. Install Playwright:
     pip install playwright
     playwright install chromium

Note: LinkedIn scraping should be done responsibly and in compliance
      with LinkedIn's Terms of Service.
""")

    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not installed. Install with:")
        print("   pip install playwright && playwright install chromium")
        exit(1)

    print("\nPress Enter to start scraping (Ctrl+C to cancel)...")
    input()

    asyncio.run(scrape_jason_goldman())

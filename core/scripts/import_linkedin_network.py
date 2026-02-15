#!/usr/bin/env python3
"""
Import LinkedIn Network Data into NEWCO System

Takes scraped LinkedIn network data and imports it into:
1. contacts.csv - Contact information
2. relationships.csv - Relationship graph

Then runs network effects analysis to identify:
- Network multipliers
- Structural holes
- Brokers
- Warm intro paths
"""

import csv
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from network_analysis import NetworkAnalysisEngine
from relationship_manager import RelationshipManager

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
NETWORK_DIR = DATA_DIR / "linkedin_networks"


class LinkedInNetworkImporter:
    """Import LinkedIn network data into NEWCO"""

    def __init__(self):
        self.contacts_file = DATA_DIR / "contacts.csv"
        self.relationships_file = DATA_DIR / "relationships.csv"
        self.rm = RelationshipManager()
        self.imported_contacts = {}
        self.contact_id_counter = self._get_max_contact_id() + 1

    def _get_max_contact_id(self) -> int:
        """Get the highest existing contact ID"""
        if not self.contacts_file.exists():
            return 0

        max_id = 0
        with open(self.contacts_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    contact_id = int(row['id'])
                    max_id = max(max_id, contact_id)
                except:
                    continue
        return max_id

    def load_linkedin_network(self, network_file: Path) -> Dict:
        """Load LinkedIn network JSON file"""
        print(f"📂 Loading network data from: {network_file}")

        with open(network_file, 'r') as f:
            network_data = json.load(f)

        print(f"✅ Loaded {len(network_data['network_graph'])} profiles")
        print(f"✅ Loaded {len(network_data['relationships'])} relationships")

        return network_data

    def import_contacts(self, network_data: Dict) -> Dict[str, int]:
        """
        Import contacts from network data

        Returns:
            Mapping of LinkedIn profile ID to NEWCO contact ID
        """
        print("\n" + "="*70)
        print("📇 IMPORTING CONTACTS")
        print("="*70)

        # Load existing contacts
        existing_contacts = []
        if self.contacts_file.exists():
            with open(self.contacts_file, 'r') as f:
                reader = csv.DictReader(f)
                existing_contacts = list(reader)

        linkedin_to_newco_id = {}

        # Import new contacts
        new_contacts = []
        for profile_id, profile_data in network_data['network_graph'].items():
            # Check if contact already exists (by name matching)
            name = profile_data.get('name', '')
            existing_match = next(
                (c for c in existing_contacts if c.get('name', '').lower() == name.lower()),
                None
            )

            if existing_match:
                # Contact already exists
                linkedin_to_newco_id[profile_id] = int(existing_match['id'])
                print(f"  ↪️  Existing: {name} (ID: {existing_match['id']})")
            else:
                # Create new contact
                newco_id = self.contact_id_counter
                self.contact_id_counter += 1

                linkedin_to_newco_id[profile_id] = newco_id

                # Extract contact data
                current_pos = profile_data.get('current_position', {})
                company = current_pos.get('company', '')
                title = current_pos.get('title', '')

                # Determine category based on title/company
                category = self._infer_category(title, company)

                # Determine tier based on degree from seed
                degree = profile_data.get('degree', 0)
                tier = min(degree + 1, 4)  # Tier 1 = seed, Tier 2 = 1st degree, etc.

                new_contact = {
                    'id': str(newco_id),
                    'name': name,
                    'company': company,
                    'title': title,
                    'category': category,
                    'tier': str(tier),
                    'status': 'Identified',  # Start as identified from LinkedIn
                    'email': '',  # Not available from LinkedIn scrape
                    'linkedin': profile_data.get('profile_url', ''),
                    'location': profile_data.get('location', ''),
                    'tags': f"linkedin_degree_{degree}",
                    'notes': f"Imported from LinkedIn. Headline: {profile_data.get('headline', '')}",
                    'priority_score': '',
                    'next_action': 'Research and validate contact',
                    'last_contact_date': '',
                    'created_date': datetime.now().strftime('%Y-%m-%d')
                }

                new_contacts.append(new_contact)
                existing_contacts.append(new_contact)
                print(f"  ✅ New: {name} (ID: {newco_id}, Tier: {tier}, {category})")

        # Save all contacts
        if new_contacts:
            self._save_contacts(existing_contacts)
            print(f"\n✅ Imported {len(new_contacts)} new contacts")
        else:
            print(f"\n✅ All contacts already exist")

        return linkedin_to_newco_id

    def import_relationships(self, network_data: Dict, id_mapping: Dict[str, int]):
        """Import relationships from network data"""
        print("\n" + "="*70)
        print("🔗 IMPORTING RELATIONSHIPS")
        print("="*70)

        relationships_imported = 0

        for rel in network_data['relationships']:
            linkedin_from = rel['from']
            linkedin_to = rel['to']

            # Map to NEWCO IDs
            newco_from = id_mapping.get(linkedin_from)
            newco_to = id_mapping.get(linkedin_to)

            if newco_from and newco_to:
                # Add relationship
                degree = rel.get('degree_from_seed', 0)

                # Infer relationship strength based on degree
                # Closer connections likely have stronger ties
                if degree == 1:
                    strength = 0.6  # Direct connection from seed
                elif degree == 2:
                    strength = 0.4  # 2nd degree - weaker tie
                elif degree == 3:
                    strength = 0.3  # 3rd degree
                else:
                    strength = 0.2  # 4th degree

                result = self.rm.add_relationship(
                    contact_id_1=str(newco_from),
                    contact_id_2=str(newco_to),
                    relationship_type='linkedin_connection',
                    strength=strength,
                    notes=f'LinkedIn connection (degree {degree} from seed)'
                )

                if result:
                    relationships_imported += 1
                    if relationships_imported % 50 == 0:
                        print(f"  Progress: {relationships_imported} relationships imported...")

        print(f"\n✅ Imported {relationships_imported} relationships")

    def _infer_category(self, title: str, company: str) -> str:
        """Infer contact category from title and company"""
        title_lower = title.lower()
        company_lower = company.lower()

        # VC/Investment categories
        if any(kw in title_lower for kw in ['partner', 'principal', 'associate']) and \
           any(kw in company_lower for kw in ['capital', 'ventures', 'partners', 'vc']):
            return "VC Partner"

        if any(kw in title_lower for kw in ['fund', 'investment']) or \
           'family office' in company_lower:
            return "Family Office CIO"

        if any(kw in title_lower for kw in ['cio', 'investment officer', 'investment director']):
            return "Institutional Investor"

        # Executive categories
        if any(kw in title_lower for kw in ['ceo', 'founder', 'co-founder']):
            return "Founder/CEO"

        if any(kw in title_lower for kw in ['cfo', 'coo', 'cto', 'chief']):
            return "Executive"

        # Insurance/finance
        if 'insurance' in company_lower or 'insurance' in title_lower:
            return "Insurance Executive"

        # Default
        return "Professional"

    def _save_contacts(self, contacts: List[Dict]):
        """Save contacts to CSV"""
        if not contacts:
            return

        fieldnames = [
            'id', 'name', 'company', 'title', 'category', 'tier', 'status',
            'email', 'linkedin', 'location', 'tags', 'notes', 'priority_score',
            'next_action', 'last_contact_date', 'created_date'
        ]

        with open(self.contacts_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contacts)

        print(f"💾 Saved {len(contacts)} contacts to {self.contacts_file}")

    def run_network_analysis(self):
        """Run network effects analysis on imported data"""
        print("\n" + "="*70)
        print("🕸️  RUNNING NETWORK EFFECTS ANALYSIS")
        print("="*70 + "\n")

        engine = NetworkAnalysisEngine()
        engine.show_network_analysis_report()


def import_and_analyze(network_file: str = None):
    """Import LinkedIn network and run analysis"""

    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         LinkedIn Network Import & Analysis for NEWCO         ║
║                   Network Effects Engine                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

    importer = LinkedInNetworkImporter()

    # Find network file
    if not network_file:
        # Find most recent network file
        network_files = list(NETWORK_DIR.glob('jason_goldman_network_*.json'))

        if not network_files:
            print("❌ No network files found in:", NETWORK_DIR)
            print("   Run linkedin_network_crawler.py first to scrape the network")
            return

        network_file = max(network_files, key=lambda f: f.stat().st_mtime)
        print(f"📂 Using most recent network file: {network_file.name}\n")

    network_file = Path(network_file)

    if not network_file.exists():
        print(f"❌ Network file not found: {network_file}")
        return

    # Load network data
    network_data = importer.load_linkedin_network(network_file)

    # Import contacts
    id_mapping = importer.import_contacts(network_data)

    # Import relationships
    importer.import_relationships(network_data, id_mapping)

    # Run network analysis
    importer.run_network_analysis()

    print("\n" + "="*70)
    print("✅ IMPORT AND ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nData stored in:")
    print(f"  Contacts: {importer.contacts_file}")
    print(f"  Relationships: {importer.relationships_file}")
    print(f"\nNext steps:")
    print(f"  1. Review contacts: ./scripts/newco_cli.py contact list")
    print(f"  2. View network multipliers: ./scripts/newco_cli.py network multipliers")
    print(f"  3. Find warm intro paths: ./scripts/newco_cli.py relationship intro-path <id>")
    print(f"  4. Generate outreach emails: ./scripts/newco_cli.py email generate <id>")
    print()


if __name__ == '__main__':
    import sys

    network_file = sys.argv[1] if len(sys.argv) > 1 else None
    import_and_analyze(network_file)

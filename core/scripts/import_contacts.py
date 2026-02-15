#!/usr/bin/env python3
"""
Contact Import Helper

This script helps import contacts from source documents into the NEWCO system.
You can either:
1. Parse structured data files (CSV, JSON)
2. Manually add contacts via interactive mode
3. Bulk import from a template
"""

import csv
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONTACTS_FILE = DATA_DIR / "contacts.csv"


class ContactImporter:
    """Import contacts into NEWCO system"""

    def __init__(self):
        self.contacts = self.load_existing_contacts()
        self.next_id = self.get_next_id()

    def load_existing_contacts(self):
        """Load existing contacts"""
        contacts = []
        if CONTACTS_FILE.exists():
            with open(CONTACTS_FILE, 'r') as f:
                reader = csv.DictReader(f)
                contacts = list(reader)
        return contacts

    def get_next_id(self):
        """Get next available ID"""
        if self.contacts:
            return max(int(c['id']) for c in self.contacts) + 1
        return 1

    def add_contact(self, name, company, title='', category='', tier=4,
                   email='', linkedin_url='', phone='', status='Cold',
                   notes='', tags=''):
        """Add a single contact"""
        contact = {
            'id': str(self.next_id),
            'name': name,
            'company': company,
            'title': title,
            'category': category,
            'tier': str(tier),
            'linkedin_url': linkedin_url,
            'email': email,
            'phone': phone,
            'status': status,
            'last_contact': '',
            'next_action': '',
            'next_action_date': '',
            'priority_score': '50',
            'notes': notes,
            'tags': tags
        }

        self.contacts.append(contact)
        self.next_id += 1
        return contact['id']

    def save_contacts(self):
        """Save all contacts to CSV"""
        fieldnames = [
            'id', 'name', 'company', 'title', 'category', 'tier',
            'linkedin_url', 'email', 'phone', 'status', 'last_contact',
            'next_action', 'next_action_date', 'priority_score', 'notes', 'tags'
        ]

        with open(CONTACTS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.contacts)

        print(f"✓ Saved {len(self.contacts)} contacts to {CONTACTS_FILE}")

    def interactive_add(self):
        """Interactively add contacts"""
        print("\n=== Add Contact Interactively ===\n")

        while True:
            print("\nEnter contact information (or 'done' to finish):")

            name = input("Name: ").strip()
            if name.lower() == 'done':
                break

            company = input("Company: ").strip()
            title = input("Title: ").strip()

            print("\nCategory options:")
            print("1. Platform Gatekeeper")
            print("2. Family Office CIO")
            print("3. VC Partner")
            print("4. Foundation Leader")
            print("5. Network Multiplier")
            print("6. Strategic Connector")
            category_choice = input("Select category (1-6): ").strip()

            category_map = {
                '1': 'Platform Gatekeeper',
                '2': 'Family Office CIO',
                '3': 'VC Partner',
                '4': 'Foundation Leader',
                '5': 'Network Multiplier',
                '6': 'Strategic Connector'
            }
            category = category_map.get(category_choice, 'Strategic Connector')

            tier = input("Tier (0-4, default 4): ").strip() or '4'
            email = input("Email: ").strip()
            linkedin = input("LinkedIn URL: ").strip()
            notes = input("Notes: ").strip()

            contact_id = self.add_contact(
                name=name,
                company=company,
                title=title,
                category=category,
                tier=int(tier),
                email=email,
                linkedin_url=linkedin,
                notes=notes
            )

            print(f"✓ Added contact {contact_id}: {name}")

    def import_from_csv(self, csv_file):
        """Import contacts from CSV file"""
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.add_contact(
                    name=row.get('name', ''),
                    company=row.get('company', ''),
                    title=row.get('title', ''),
                    category=row.get('category', 'Strategic Connector'),
                    tier=int(row.get('tier', 4)),
                    email=row.get('email', ''),
                    linkedin_url=row.get('linkedin_url', ''),
                    phone=row.get('phone', ''),
                    notes=row.get('notes', '')
                )

        print(f"✓ Imported contacts from {csv_file}")

    def add_sample_contacts(self):
        """Add sample contacts for testing"""
        samples = [
            {
                'name': 'Bob Burlinson',
                'company': 'Omniscient',
                'title': 'CEO',
                'category': 'Network Multiplier',
                'tier': 0,
                'notes': 'Top connector - Goldman intros, platform strategy'
            },
            {
                'name': 'Alistair Savides',
                'company': 'Hamilton Lane',
                'title': 'Managing Director',
                'category': 'Platform Gatekeeper',
                'tier': 1,
                'notes': 'Educational meeting on emerging managers'
            },
            {
                'name': 'Marie Young',
                'company': 'Threshold Family Office',
                'title': 'CIO',
                'category': 'Family Office CIO',
                'tier': 2,
                'notes': 'Focus on liquid VC access, fee transparency'
            },
            {
                'name': 'Sample VC Partner',
                'company': 'Sample Ventures',
                'title': 'Partner',
                'category': 'VC Partner',
                'tier': 3,
                'notes': 'LP intro pathway, co-investment interest'
            },
            {
                'name': 'Jessica Mancini',
                'company': 'Barr Foundation',
                'title': 'Investment Director',
                'category': 'Foundation Leader',
                'tier': 3,
                'notes': 'Mission-aligned vehicle, emerging manager diversity'
            }
        ]

        for sample in samples:
            self.add_contact(**sample)

        print(f"✓ Added {len(samples)} sample contacts")


def main():
    """Main entry point"""
    print("NEWCO Contact Importer")
    print("=" * 50)

    importer = ContactImporter()

    if len(sys.argv) > 1:
        # Import from file
        csv_file = sys.argv[1]
        if Path(csv_file).exists():
            importer.import_from_csv(csv_file)
            importer.save_contacts()
        else:
            print(f"Error: File not found: {csv_file}")
            sys.exit(1)
    else:
        # Interactive mode
        print("\nOptions:")
        print("1. Add contacts interactively")
        print("2. Add sample contacts (for testing)")
        print("3. Exit")

        choice = input("\nSelect option (1-3): ").strip()

        if choice == '1':
            importer.interactive_add()
            importer.save_contacts()
        elif choice == '2':
            importer.add_sample_contacts()
            importer.save_contacts()
        elif choice == '3':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice")
            sys.exit(1)

    print("\n✓ Import complete!")
    print(f"Total contacts in database: {len(importer.contacts)}")


if __name__ == '__main__':
    main()

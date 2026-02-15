#!/usr/bin/env python3
"""
NEWCO PE-VC Source Data Scraper
================================

Scrapes and structures PE/VC company data including:
- Company details (name, sector, stage, funding)
- People (founders, executives, board members)
- Relationships (investors, portfolio companies)
- Financial metrics (revenue, burn, growth)
- Events (funding rounds, IPOs, acquisitions)

Data sources:
- Public filings (SEC, EDGAR)
- Company websites
- LinkedIn (via API or structured search)
- Crunchbase (if API available)
- PitchBook (if access available)
- Custom curated lists
"""

import json
import os
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd

# Configuration
DATA_DIR = "/Users/rufio/NEWCO/PE-VC-Source-Data"
os.makedirs(DATA_DIR, exist_ok=True)

class Company:
    """Company data structure"""

    def __init__(self, name: str):
        self.name = name
        self.sector = None
        self.stage = None  # Seed, Series A-F, Growth, Pre-IPO
        self.founded = None
        self.location = None
        self.employees = None
        self.revenue = None
        self.revenue_growth = None
        self.burn_rate = None
        self.burn_multiple = None
        self.valuation = None
        self.total_funding = None
        self.last_funding_date = None
        self.last_funding_amount = None
        self.investors = []
        self.people = []
        self.website = None
        self.linkedin = None
        self.description = None
        self.tags = []
        self.ipo_date = None
        self.ipo_probability = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "sector": self.sector,
            "stage": self.stage,
            "founded": self.founded,
            "location": self.location,
            "employees": self.employees,
            "revenue": self.revenue,
            "revenue_growth": self.revenue_growth,
            "burn_rate": self.burn_rate,
            "burn_multiple": self.burn_multiple,
            "valuation": self.valuation,
            "total_funding": self.total_funding,
            "last_funding_date": self.last_funding_date,
            "last_funding_amount": self.last_funding_amount,
            "investors": self.investors,
            "people": self.people,
            "website": self.website,
            "linkedin": self.linkedin,
            "description": self.description,
            "tags": self.tags,
            "ipo_date": self.ipo_date,
            "ipo_probability": self.ipo_probability
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Company':
        """Create from dictionary"""
        company = cls(data['name'])
        for key, value in data.items():
            if hasattr(company, key):
                setattr(company, key, value)
        return company

class Person:
    """Person data structure"""

    def __init__(self, name: str):
        self.name = name
        self.linkedin = None
        self.title = None
        self.companies = []  # List of company associations
        self.roles = []  # Founder, CEO, Investor, Board Member, etc.
        self.education = []
        self.previous_companies = []
        self.investments = []
        self.expertise = []
        self.location = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "linkedin": self.linkedin,
            "title": self.title,
            "companies": self.companies,
            "roles": self.roles,
            "education": self.education,
            "previous_companies": self.previous_companies,
            "investments": self.investments,
            "expertise": self.expertise,
            "location": self.location
        }

class PEVCDataScraper:
    """Main scraper class"""

    def __init__(self):
        self.companies = {}
        self.people = {}
        self.data_dir = DATA_DIR

    def add_company(self, company: Company):
        """Add company to database"""
        self.companies[company.name] = company

        # Associate people with company
        for person_name in company.people:
            if person_name not in self.people:
                self.people[person_name] = Person(person_name)

            person = self.people[person_name]
            if company.name not in person.companies:
                person.companies.append(company.name)

    def add_person(self, person: Person):
        """Add person to database"""
        self.people[person.name] = person

        # Associate companies with person
        for company_name in person.companies:
            if company_name in self.companies:
                company = self.companies[company_name]
                if person.name not in company.people:
                    company.people.append(person.name)

    def scrape_from_csv(self, filepath: str):
        """Import from CSV file"""
        try:
            df = pd.read_csv(filepath)

            for _, row in df.iterrows():
                company = Company(row.get('company_name', row.get('name', '')))

                # Map CSV columns to company attributes
                company.sector = row.get('sector', row.get('industry', None))
                company.stage = row.get('stage', None)
                company.founded = row.get('founded', row.get('founded_year', None))
                company.location = row.get('location', row.get('hq_location', None))
                company.employees = row.get('employees', row.get('employee_count', None))
                company.revenue = row.get('revenue', None)
                company.revenue_growth = row.get('growth_rate', row.get('revenue_growth', None))
                company.valuation = row.get('valuation', None)
                company.total_funding = row.get('total_funding', None)
                company.website = row.get('website', None)
                company.linkedin = row.get('linkedin', None)
                company.description = row.get('description', None)

                # Parse people if available
                if 'founders' in row and pd.notna(row['founders']):
                    company.people = [p.strip() for p in str(row['founders']).split(',')]

                self.add_company(company)

            print(f"✅ Imported {len(self.companies)} companies from {filepath}")

        except Exception as e:
            print(f"❌ Error importing CSV: {str(e)}")

    def scrape_from_json(self, filepath: str):
        """Import from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            if isinstance(data, list):
                for item in data:
                    company = Company.from_dict(item)
                    self.add_company(company)
            elif isinstance(data, dict):
                for name, details in data.items():
                    details['name'] = name
                    company = Company.from_dict(details)
                    self.add_company(company)

            print(f"✅ Imported {len(self.companies)} companies from {filepath}")

        except Exception as e:
            print(f"❌ Error importing JSON: {str(e)}")

    def create_sample_dataset(self):
        """Create sample PE/VC dataset for testing"""
        print("📊 Creating sample PE/VC dataset...")

        # Sample defense tech companies
        companies_data = [
            {
                "name": "Palantir Technologies",
                "sector": "Defense Tech",
                "stage": "Public",
                "founded": 2003,
                "location": "Denver, CO",
                "employees": 3500,
                "revenue": 2200000000,
                "revenue_growth": 18,
                "valuation": 45000000000,
                "people": ["Alex Karp", "Stephen Cohen", "Peter Thiel"],
                "investors": ["Founders Fund", "In-Q-Tel", "Tiger Global"],
                "tags": ["AI", "Data Analytics", "Government"],
                "ipo_date": "2020-09-30",
                "ipo_probability": 100
            },
            {
                "name": "Anduril Industries",
                "sector": "Defense Tech",
                "stage": "Series E",
                "founded": 2017,
                "location": "Costa Mesa, CA",
                "employees": 1800,
                "revenue": 500000000,
                "revenue_growth": 150,
                "burn_rate": 50000000,
                "burn_multiple": 0.1,
                "valuation": 8500000000,
                "total_funding": 2100000000,
                "people": ["Palmer Luckey", "Matt Grimm", "Brian Schimpf"],
                "investors": ["Founders Fund", "Andreessen Horowitz", "8VC"],
                "tags": ["Drones", "AI", "Autonomous Systems"],
                "ipo_probability": 85
            },
            {
                "name": "Shield AI",
                "sector": "Defense Tech",
                "stage": "Series F",
                "founded": 2015,
                "location": "San Diego, CA",
                "employees": 500,
                "revenue": 120000000,
                "revenue_growth": 200,
                "burn_rate": 30000000,
                "burn_multiple": 0.25,
                "valuation": 2700000000,
                "total_funding": 1000000000,
                "people": ["Brandon Tseng", "Ryan Tseng", "Andrew Reiter"],
                "investors": ["Point72 Ventures", "Andreessen Horowitz", "Shield Capital"],
                "tags": ["AI", "Autonomous Drones", "Edge Computing"],
                "ipo_probability": 75
            },
            {
                "name": "Scale AI",
                "sector": "AI Infrastructure",
                "stage": "Series E",
                "founded": 2016,
                "location": "San Francisco, CA",
                "employees": 800,
                "revenue": 600000000,
                "revenue_growth": 100,
                "burn_rate": 100000000,
                "burn_multiple": 0.17,
                "valuation": 7300000000,
                "total_funding": 1600000000,
                "people": ["Alexandr Wang", "Lucy Guo"],
                "investors": ["Accel", "Index Ventures", "Tiger Global"],
                "tags": ["AI", "Data Labeling", "ML Infrastructure"],
                "ipo_probability": 90
            },
            {
                "name": "SpaceX",
                "sector": "Aerospace",
                "stage": "Growth",
                "founded": 2002,
                "location": "Hawthorne, CA",
                "employees": 13000,
                "revenue": 8000000000,
                "revenue_growth": 30,
                "valuation": 180000000000,
                "total_funding": 10000000000,
                "people": ["Elon Musk", "Gwynne Shotwell", "Tom Mueller"],
                "investors": ["Founders Fund", "Sequoia Capital", "Gigafund"],
                "tags": ["Rockets", "Satellites", "Starlink"],
                "ipo_probability": 60
            }
        ]

        for data in companies_data:
            company = Company(data['name'])
            for key, value in data.items():
                if hasattr(company, key):
                    setattr(company, key, value)
            self.add_company(company)

        print(f"✅ Created {len(self.companies)} sample companies")
        print(f"✅ Associated {len(self.people)} people")

    def export_to_json(self, filename: str = "pe_vc_data.json"):
        """Export to JSON"""
        filepath = os.path.join(self.data_dir, filename)

        data = {
            "companies": {name: company.to_dict() for name, company in self.companies.items()},
            "people": {name: person.to_dict() for name, person in self.people.items()},
            "metadata": {
                "total_companies": len(self.companies),
                "total_people": len(self.people),
                "last_updated": datetime.now().isoformat()
            }
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Exported to {filepath}")
        return filepath

    def export_to_csv(self):
        """Export companies to CSV"""
        filepath = os.path.join(self.data_dir, "companies.csv")

        companies_list = [company.to_dict() for company in self.companies.values()]
        df = pd.DataFrame(companies_list)

        df.to_csv(filepath, index=False)

        print(f"✅ Exported to {filepath}")
        return filepath

    def get_stats(self) -> Dict[str, Any]:
        """Get dataset statistics"""
        return {
            "total_companies": len(self.companies),
            "total_people": len(self.people),
            "sectors": list(set([c.sector for c in self.companies.values() if c.sector])),
            "stages": list(set([c.stage for c in self.companies.values() if c.stage])),
            "avg_valuation": sum([c.valuation or 0 for c in self.companies.values()]) / len(self.companies) if self.companies else 0,
            "total_funding": sum([c.total_funding or 0 for c in self.companies.values()])
        }

def main():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║              NEWCO PE-VC DATA SCRAPER                        ║
╚═══════════════════════════════════════════════════════════════╝
""")

    scraper = PEVCDataScraper()

    # Check for existing data files
    data_files = []
    for ext in ['*.csv', '*.json']:
        import glob
        data_files.extend(glob.glob(os.path.join(DATA_DIR, ext)))

    if data_files:
        print(f"Found {len(data_files)} existing data files")
        for filepath in data_files:
            if filepath.endswith('.csv'):
                scraper.scrape_from_csv(filepath)
            elif filepath.endswith('.json'):
                scraper.scrape_from_json(filepath)
    else:
        print("No existing data found. Creating sample dataset...")
        scraper.create_sample_dataset()

    # Export data
    scraper.export_to_json()
    scraper.export_to_csv()

    # Print stats
    stats = scraper.get_stats()
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DATASET STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Companies:      {stats['total_companies']}
People:         {stats['total_people']}
Sectors:        {', '.join(stats['sectors'][:5])}
Stages:         {', '.join(stats['stages'][:5])}
Avg Valuation:  ${stats['avg_valuation']/1e9:.2f}B
Total Funding:  ${stats['total_funding']/1e9:.2f}B

Data Location: {DATA_DIR}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    print("✅ PE-VC data ready for agents!")
    print("")
    print("Next steps:")
    print("  1. Add your own companies to CSV/JSON files in PE-VC-Source-Data/")
    print("  2. Feed data to agents via agent APIs")
    print("  3. Sync to Supabase for partner access")

if __name__ == "__main__":
    main()

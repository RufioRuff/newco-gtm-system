"""
Email Template Generation Engine
"""

import csv
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates" / "email"


class EmailGenerator:
    """Generate personalized emails from templates"""

    def __init__(self):
        self.templates_dir = TEMPLATES_DIR
        self.contacts_file = DATA_DIR / "contacts.csv"

    def load_contact(self, contact_id):
        """Load contact by ID"""
        with open(self.contacts_file, 'r') as f:
            reader = csv.DictReader(f)
            for contact in reader:
                if contact['id'] == str(contact_id):
                    return contact
        return None

    def load_template(self, template_name):
        """Load email template"""
        template_file = self.templates_dir / f"{template_name}.md"
        if not template_file.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")

        with open(template_file, 'r') as f:
            content = f.read()

        # Parse frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                # frontmatter = parts[1]
                body = parts[2].strip()
                return body

        return content

    def detect_template(self, contact):
        """Auto-detect appropriate template based on contact category"""
        category_to_template = {
            'Platform Gatekeeper': 'platform_gatekeeper',
            'Family Office CIO': 'family_office_cio',
            'VC Partner': 'vc_partner',
            'Foundation Leader': 'foundation_leader',
            'Network Multiplier': 'network_multiplier'
        }
        return category_to_template.get(contact['category'], 'platform_gatekeeper')

    def generate(self, contact_id, template_name=None):
        """Generate personalized email"""
        contact = self.load_contact(contact_id)
        if not contact:
            return f"Error: Contact {contact_id} not found"

        # Auto-detect template if not provided
        if not template_name:
            template_name = self.detect_template(contact)

        # Load template
        try:
            template = self.load_template(template_name)
        except FileNotFoundError as e:
            return f"Error: {e}"

        # Build context for template variables
        context = self.build_context(contact)

        # Substitute variables
        email = self.substitute_variables(template, context)

        return email

    def build_context(self, contact):
        """Build context dictionary for template substitution"""
        # Split name into parts
        name_parts = contact['name'].split()
        first_name = name_parts[0] if name_parts else contact['name']

        context = {
            'name': first_name,
            'full_name': contact['name'],
            'company': contact['company'],
            'title': contact['title'],
            'category': contact['category'],
            'hook': self.generate_hook(contact),
            'mutual_connection_mention': '',  # Could be customized
            'your_firm': 'NEWCO',
            'firm_name': contact['company'],
            'investment_focus': 'venture capital',  # Could be customized
            'specific_interest': 'your recent investments',  # Could be customized
            'custom_subject': f"Partnership opportunity - {contact['company']}",
            'highly_personalized_hook': f"I've been following your work at {contact['company']}",
            'specific_opportunity_description': "I'm launching NEWCO, a liquid emerging VC manager fund-of-funds",
            'specific_reason': "your expertise and network in the emerging manager space",
            'specific_ask': "30 minutes to discuss potential collaboration",
            'value_exchange_proposition': "I think there are strong synergies between what we're building",
            'specific_time_suggestion': "Next week or the following?",
            'personal_connection_note': '',
            'foundation_name': contact['company'],
            'mission_area': 'innovation and impact',
            'relevant_sectors': 'technology, healthcare, climate',
            'org_specific_alignment': f"NEWCO aligns with {contact['company']}'s mission",
            'need_1': 'Diversified VC exposure',
            'need_2': 'Cost-effective fee structure',
            'need_3': 'Quarterly liquidity',
        }

        return context

    def generate_hook(self, contact):
        """Generate personalized hook based on contact info"""
        hooks = {
            'Platform Gatekeeper': f"I've been following {contact['company']}'s work in institutional manager selection",
            'Family Office CIO': f"I came across {contact['company']} while researching innovative family offices",
            'VC Partner': f"I've been impressed by {contact['company']}'s portfolio and approach",
            'Foundation Leader': f"I've long admired {contact['company']}'s impact-focused investment strategy",
            'Network Multiplier': f"I've been following your work and would love to connect"
        }
        return hooks.get(contact['category'], f"I came across your work at {contact['company']}")

    def substitute_variables(self, template, context):
        """Substitute {{variable}} placeholders in template"""
        def replace(match):
            var_name = match.group(1)
            return context.get(var_name, match.group(0))

        return re.sub(r'\{\{(\w+)\}\}', replace, template)

    def preview(self, contact_id):
        """Preview email without saving"""
        return self.generate(contact_id)

    def batch_generate(self, tier=None, week=None):
        """Batch generate emails for multiple contacts"""
        contacts = []
        with open(self.contacts_file, 'r') as f:
            reader = csv.DictReader(f)
            contacts = list(reader)

        # Filter by tier
        if tier is not None:
            contacts = [c for c in contacts if c['tier'] == str(tier)]

        # Filter by week (would need week planning data)
        # For now, just generate for all filtered contacts

        results = []
        for contact in contacts:
            # Skip if already contacted or not interested
            if contact['status'] in ['Initial Outreach Sent', 'Meeting Scheduled',
                                      'Meeting Completed', 'Committed/Closed', 'Not Interested']:
                continue

            email = self.generate(contact['id'])
            results.append({
                'contact_id': contact['id'],
                'contact_name': contact['name'],
                'email': email
            })

            # Save to file
            output_dir = BASE_DIR / "reports" / "emails"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"email_{contact['id']}_{datetime.now().strftime('%Y%m%d')}.txt"
            output_file.write_text(email)

        return results


if __name__ == '__main__':
    # Test
    gen = EmailGenerator()
    email = gen.generate('1')
    print(email)

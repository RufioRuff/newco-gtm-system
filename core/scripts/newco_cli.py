#!/usr/bin/env python3
"""
NEWCO GTM Management System - Main CLI Tool
"""

import argparse
import csv
import sys
from pathlib import Path
from datetime import datetime, timedelta
import yaml

# Base directory
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"

# Import submodules
sys.path.insert(0, str(BASE_DIR / "scripts"))
from email_generator import EmailGenerator
from pipeline_manager import PipelineManager
from reports import ReportGenerator
from automation import AutomationEngine
from network_analysis import NetworkAnalysisEngine
from relationship_manager import RelationshipManager
from analytics import AnalyticsEngine
from public_markets import PublicMarketsEngine, InvestorRelations
from regulatory_compliance import RegulatoryComplianceEngine
from portfolio_management import PortfolioManager
from manager_crm import ManagerCRM
from risk_management import RiskManager
from board_reporting import BoardReportGenerator
from lp_reporting import LPReportGenerator
from financial_modeling import FinancialModeler
from competitive_intelligence import CompetitiveIntelligence
from team_management import TeamManager
from governance import InstitutionalGovernance


class ContactManager:
    """Manages contact database operations"""

    def __init__(self):
        self.contacts_file = DATA_DIR / "contacts.csv"
        self.interactions_file = DATA_DIR / "interactions.csv"

    def load_contacts(self):
        """Load all contacts from CSV"""
        contacts = []
        if self.contacts_file.exists():
            with open(self.contacts_file, 'r') as f:
                reader = csv.DictReader(f)
                contacts = list(reader)
        return contacts

    def save_contacts(self, contacts):
        """Save contacts to CSV"""
        if not contacts:
            return

        fieldnames = contacts[0].keys()
        with open(self.contacts_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contacts)

    def get_contact(self, contact_id):
        """Get a single contact by ID"""
        contacts = self.load_contacts()
        for contact in contacts:
            if contact['id'] == str(contact_id):
                return contact
        return None

    def list_contacts(self, tier=None, status=None, category=None):
        """List contacts with optional filters"""
        contacts = self.load_contacts()

        # Apply filters
        if tier is not None:
            contacts = [c for c in contacts if c.get('tier') == str(tier)]
        if status:
            contacts = [c for c in contacts if c.get('status') == status]
        if category:
            contacts = [c for c in contacts if c.get('category') == category]

        return contacts

    def update_contact(self, contact_id, **updates):
        """Update a contact's fields"""
        contacts = self.load_contacts()
        updated = False

        for contact in contacts:
            if contact['id'] == str(contact_id):
                contact.update(updates)
                contact['last_contact'] = datetime.now().strftime('%Y-%m-%d')
                updated = True
                break

        if updated:
            self.save_contacts(contacts)
            return True
        return False

    def add_contact(self, **contact_data):
        """Add a new contact"""
        contacts = self.load_contacts()

        # Generate new ID
        if contacts:
            max_id = max(int(c['id']) for c in contacts if c['id'])
            new_id = max_id + 1
        else:
            new_id = 1

        contact_data['id'] = str(new_id)
        contact_data['last_contact'] = contact_data.get('last_contact', '')
        contact_data['priority_score'] = contact_data.get('priority_score', '50')
        contact_data['status'] = contact_data.get('status', 'Cold')

        contacts.append(contact_data)
        self.save_contacts(contacts)
        return new_id

    def search_contacts(self, query):
        """Search contacts by name or company"""
        contacts = self.load_contacts()
        query = query.lower()
        results = []

        for contact in contacts:
            if (query in contact.get('name', '').lower() or
                query in contact.get('company', '').lower()):
                results.append(contact)

        return results

    def get_priority_contacts(self, limit=20):
        """Get top priority contacts"""
        contacts = self.load_contacts()

        # Filter out closed/not interested
        active = [c for c in contacts if c.get('status') not in
                 ['Committed/Closed', 'Not Interested']]

        # Sort by priority score (descending) and tier (ascending)
        sorted_contacts = sorted(
            active,
            key=lambda c: (
                -float(c.get('priority_score', 50)),
                int(c.get('tier', 4))
            )
        )

        return sorted_contacts[:limit]

    def log_interaction(self, contact_id, interaction_type, subject, notes='', outcome='', next_steps=''):
        """Log an interaction with a contact"""
        interactions = []
        if self.interactions_file.exists():
            with open(self.interactions_file, 'r') as f:
                reader = csv.DictReader(f)
                interactions = list(reader)

        # Generate new ID
        if interactions:
            max_id = max(int(i['id']) for i in interactions if i['id'])
            new_id = max_id + 1
        else:
            new_id = 1

        interaction = {
            'id': str(new_id),
            'contact_id': str(contact_id),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': interaction_type,
            'subject': subject,
            'notes': notes,
            'outcome': outcome,
            'next_steps': next_steps
        }

        interactions.append(interaction)

        # Save interactions
        with open(self.interactions_file, 'w', newline='') as f:
            fieldnames = ['id', 'contact_id', 'date', 'type', 'subject', 'notes', 'outcome', 'next_steps']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(interactions)

        return new_id


class NewcoCLI:
    """Main CLI application"""

    def __init__(self):
        self.contact_mgr = ContactManager()
        self.email_gen = EmailGenerator()
        self.pipeline_mgr = PipelineManager()
        self.report_gen = ReportGenerator()
        self.automation = AutomationEngine()
        self.network_analysis = NetworkAnalysisEngine()
        self.relationship_mgr = RelationshipManager()
        self.analytics = AnalyticsEngine()
        self.public_markets = PublicMarketsEngine()
        self.investor_relations = InvestorRelations()
        self.compliance = RegulatoryComplianceEngine()
        self.portfolio = PortfolioManager()
        self.manager_crm = ManagerCRM()
        self.risk = RiskManager()
        self.board = BoardReportGenerator()
        self.lp_reporting = LPReportGenerator()
        self.finance = FinancialModeler()
        self.intel = CompetitiveIntelligence()
        self.team = TeamManager()
        self.governance = InstitutionalGovernance()
        self.config = self.load_config()

    def load_config(self):
        """Load configuration"""
        config_file = CONFIG_DIR / "config.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def run(self):
        """Main entry point"""
        parser = argparse.ArgumentParser(
            description='NEWCO GTM Management System',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        subparsers = parser.add_subparsers(dest='command', help='Commands')

        # Contact commands
        self.setup_contact_commands(subparsers)

        # Email commands
        self.setup_email_commands(subparsers)

        # Log commands
        self.setup_log_commands(subparsers)

        # Pipeline commands
        self.setup_pipeline_commands(subparsers)

        # Task commands
        self.setup_task_commands(subparsers)

        # Report commands
        self.setup_report_commands(subparsers)

        # Network analysis commands
        self.setup_network_commands(subparsers)

        # Relationship commands
        self.setup_relationship_commands(subparsers)

        # Analytics commands
        self.setup_analytics_commands(subparsers)

        # Public markets commands
        self.setup_public_markets_commands(subparsers)

        # Compliance commands
        self.setup_compliance_commands(subparsers)

        # Portfolio commands
        self.setup_portfolio_commands(subparsers)

        # Manager CRM commands
        self.setup_manager_commands(subparsers)

        # Risk management commands
        self.setup_risk_commands(subparsers)

        # Board reporting commands
        self.setup_board_commands(subparsers)

        # LP reporting commands
        self.setup_lp_commands(subparsers)

        # Financial modeling commands
        self.setup_finance_commands(subparsers)

        # Competitive intelligence commands
        self.setup_intel_commands(subparsers)

        # Team management commands
        self.setup_team_commands(subparsers)

        # Institutional governance commands
        self.setup_governance_commands(subparsers)

        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        # Route to appropriate handler
        handler = getattr(self, f'cmd_{args.command}', None)
        if handler:
            handler(args)
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)

    def setup_contact_commands(self, subparsers):
        """Setup contact subcommands"""
        contact_parser = subparsers.add_parser('contact', help='Contact management')
        contact_sub = contact_parser.add_subparsers(dest='subcommand')

        # List contacts
        list_parser = contact_sub.add_parser('list', help='List contacts')
        list_parser.add_argument('--tier', type=int, help='Filter by tier')
        list_parser.add_argument('--status', help='Filter by status')
        list_parser.add_argument('--category', help='Filter by category')

        # Show contact
        show_parser = contact_sub.add_parser('show', help='Show contact details')
        show_parser.add_argument('id', help='Contact ID')

        # Update contact
        update_parser = contact_sub.add_parser('update', help='Update contact')
        update_parser.add_argument('id', help='Contact ID')
        update_parser.add_argument('--status', help='New status')
        update_parser.add_argument('--next-action', help='Next action')
        update_parser.add_argument('--next-action-date', help='Next action date (YYYY-MM-DD)')
        update_parser.add_argument('--notes', help='Notes')

        # Search contacts
        search_parser = contact_sub.add_parser('search', help='Search contacts')
        search_parser.add_argument('query', help='Search query')

        # Prioritize
        contact_sub.add_parser('prioritize', help='Show top priority contacts')

        # Add contact
        add_parser = contact_sub.add_parser('add', help='Add new contact')
        add_parser.add_argument('--name', required=True, help='Contact name')
        add_parser.add_argument('--company', required=True, help='Company name')
        add_parser.add_argument('--title', help='Job title')
        add_parser.add_argument('--category', required=True, help='Contact category')
        add_parser.add_argument('--tier', type=int, required=True, help='Tier (0-4)')
        add_parser.add_argument('--email', help='Email address')
        add_parser.add_argument('--linkedin', help='LinkedIn URL')

    def setup_email_commands(self, subparsers):
        """Setup email subcommands"""
        email_parser = subparsers.add_parser('email', help='Email generation')
        email_sub = email_parser.add_subparsers(dest='subcommand')

        # Generate email
        gen_parser = email_sub.add_parser('generate', help='Generate email')
        gen_parser.add_argument('contact_id', help='Contact ID')
        gen_parser.add_argument('--template', help='Template name (auto-detected if not provided)')
        gen_parser.add_argument('--output', help='Output file')

        # Preview email
        preview_parser = email_sub.add_parser('preview', help='Preview email')
        preview_parser.add_argument('contact_id', help='Contact ID')

        # Batch generate
        batch_parser = email_sub.add_parser('batch', help='Batch generate emails')
        batch_parser.add_argument('--tier', type=int, help='Filter by tier')
        batch_parser.add_argument('--week', type=int, help='Week number')

    def setup_log_commands(self, subparsers):
        """Setup log subcommands"""
        log_parser = subparsers.add_parser('log', help='Log interactions')
        log_sub = log_parser.add_subparsers(dest='subcommand')

        # Log email
        email_parser = log_sub.add_parser('email', help='Log email')
        email_parser.add_argument('contact_id', help='Contact ID')
        email_parser.add_argument('subject', help='Email subject')
        email_parser.add_argument('--sent', action='store_true', help='Email was sent (vs received)')
        email_parser.add_argument('--notes', help='Notes')

        # Log meeting
        meeting_parser = log_sub.add_parser('meeting', help='Log meeting')
        meeting_parser.add_argument('contact_id', help='Contact ID')
        meeting_parser.add_argument('subject', help='Meeting subject')
        meeting_parser.add_argument('--outcome', help='Meeting outcome')
        meeting_parser.add_argument('--next-steps', help='Next steps')

        # Log call
        call_parser = log_sub.add_parser('call', help='Log call')
        call_parser.add_argument('contact_id', help='Contact ID')
        call_parser.add_argument('subject', help='Call subject')
        call_parser.add_argument('--notes', help='Notes')

    def setup_pipeline_commands(self, subparsers):
        """Setup pipeline subcommands"""
        pipeline_parser = subparsers.add_parser('pipeline', help='Pipeline tracking')
        pipeline_sub = pipeline_parser.add_subparsers(dest='subcommand')

        pipeline_sub.add_parser('show', help='Show pipeline overview')
        pipeline_sub.add_parser('weekly', help='Show weekly metrics')

        report_parser = pipeline_sub.add_parser('report', help='Generate pipeline report')
        report_parser.add_argument('--week', type=int, help='Week number')

    def setup_task_commands(self, subparsers):
        """Setup task subcommands"""
        task_parser = subparsers.add_parser('tasks', help='Task management')
        task_sub = task_parser.add_subparsers(dest='subcommand')

        task_sub.add_parser('today', help='Show today\'s tasks')
        task_sub.add_parser('week', help='Show this week\'s tasks')
        task_sub.add_parser('overdue', help='Show overdue tasks')

    def setup_report_commands(self, subparsers):
        """Setup report subcommands"""
        report_parser = subparsers.add_parser('report', help='Generate reports')
        report_sub = report_parser.add_subparsers(dest='subcommand')

        report_sub.add_parser('weekly', help='Generate weekly report')
        report_sub.add_parser('dashboard', help='Show CLI dashboard')
        report_sub.add_parser('export', help='Export data')

    # Command handlers
    def cmd_contact(self, args):
        """Handle contact commands"""
        if args.subcommand == 'list':
            contacts = self.contact_mgr.list_contacts(
                tier=args.tier,
                status=args.status,
                category=args.category
            )
            self.print_contact_list(contacts)

        elif args.subcommand == 'show':
            contact = self.contact_mgr.get_contact(args.id)
            if contact:
                self.print_contact_details(contact)
            else:
                print(f"Contact {args.id} not found")

        elif args.subcommand == 'update':
            updates = {}
            if args.status:
                updates['status'] = args.status
            if args.next_action:
                updates['next_action'] = args.next_action
            if args.next_action_date:
                updates['next_action_date'] = args.next_action_date
            if args.notes:
                updates['notes'] = args.notes

            if self.contact_mgr.update_contact(args.id, **updates):
                print(f"✓ Contact {args.id} updated")
            else:
                print(f"Contact {args.id} not found")

        elif args.subcommand == 'search':
            results = self.contact_mgr.search_contacts(args.query)
            self.print_contact_list(results)

        elif args.subcommand == 'prioritize':
            contacts = self.contact_mgr.get_priority_contacts()
            print("\n🎯 Top Priority Contacts\n")
            self.print_contact_list(contacts)

        elif args.subcommand == 'add':
            contact_data = {
                'name': args.name,
                'company': args.company,
                'title': args.title or '',
                'category': args.category,
                'tier': str(args.tier),
                'email': args.email or '',
                'linkedin_url': args.linkedin or '',
                'phone': '',
                'next_action': '',
                'next_action_date': '',
                'notes': '',
                'tags': ''
            }
            new_id = self.contact_mgr.add_contact(**contact_data)
            print(f"✓ Contact added with ID: {new_id}")

    def cmd_email(self, args):
        """Handle email commands"""
        if args.subcommand == 'generate':
            email = self.email_gen.generate(args.contact_id, args.template)
            if args.output:
                Path(args.output).write_text(email)
                print(f"✓ Email saved to {args.output}")
            else:
                print(email)

        elif args.subcommand == 'preview':
            email = self.email_gen.preview(args.contact_id)
            print(email)

        elif args.subcommand == 'batch':
            results = self.email_gen.batch_generate(tier=args.tier, week=args.week)
            print(f"✓ Generated {len(results)} emails")

    def cmd_log(self, args):
        """Handle log commands"""
        if args.subcommand == 'email':
            interaction_type = 'email_sent' if args.sent else 'email_received'
            interaction_id = self.contact_mgr.log_interaction(
                args.contact_id,
                interaction_type,
                args.subject,
                notes=args.notes or ''
            )

            # Update contact status
            if args.sent:
                self.contact_mgr.update_contact(
                    args.contact_id,
                    status='Initial Outreach Sent'
                )

            print(f"✓ Logged {interaction_type} (ID: {interaction_id})")

        elif args.subcommand == 'meeting':
            interaction_id = self.contact_mgr.log_interaction(
                args.contact_id,
                'meeting',
                args.subject,
                outcome=args.outcome or '',
                next_steps=args.next_steps or ''
            )

            # Update contact status
            self.contact_mgr.update_contact(
                args.contact_id,
                status='Meeting Completed'
            )

            print(f"✓ Logged meeting (ID: {interaction_id})")

        elif args.subcommand == 'call':
            interaction_id = self.contact_mgr.log_interaction(
                args.contact_id,
                'call',
                args.subject,
                notes=args.notes or ''
            )
            print(f"✓ Logged call (ID: {interaction_id})")

    def cmd_pipeline(self, args):
        """Handle pipeline commands"""
        if args.subcommand == 'show':
            self.pipeline_mgr.show_overview()
        elif args.subcommand == 'weekly':
            self.pipeline_mgr.show_weekly()
        elif args.subcommand == 'report':
            self.pipeline_mgr.generate_report(args.week)

    def cmd_tasks(self, args):
        """Handle task commands"""
        if args.subcommand == 'today':
            tasks = self.automation.get_tasks_today()
            self.print_tasks(tasks, "Today's Tasks")
        elif args.subcommand == 'week':
            tasks = self.automation.get_tasks_week()
            self.print_tasks(tasks, "This Week's Tasks")
        elif args.subcommand == 'overdue':
            tasks = self.automation.get_overdue_tasks()
            self.print_tasks(tasks, "Overdue Tasks")

    def cmd_report(self, args):
        """Handle report commands"""
        if args.subcommand == 'weekly':
            self.report_gen.generate_weekly_report()
        elif args.subcommand == 'dashboard':
            self.report_gen.show_dashboard()
        elif args.subcommand == 'export':
            self.report_gen.export_data()

    # Helper methods for printing
    def print_contact_list(self, contacts):
        """Print a list of contacts"""
        if not contacts:
            print("No contacts found")
            return

        print(f"\n{'ID':<5} {'Name':<25} {'Company':<25} {'Tier':<5} {'Status':<20}")
        print("-" * 85)
        for contact in contacts:
            print(f"{contact['id']:<5} {contact['name']:<25} {contact['company']:<25} "
                  f"{contact['tier']:<5} {contact['status']:<20}")
        print(f"\nTotal: {len(contacts)} contacts\n")

    def print_contact_details(self, contact):
        """Print detailed contact information"""
        print(f"\n{'='*60}")
        print(f"Contact ID: {contact['id']}")
        print(f"{'='*60}")
        print(f"Name:          {contact['name']}")
        print(f"Company:       {contact['company']}")
        print(f"Title:         {contact['title']}")
        print(f"Category:      {contact['category']}")
        print(f"Tier:          {contact['tier']}")
        print(f"Email:         {contact['email']}")
        print(f"Phone:         {contact['phone']}")
        print(f"LinkedIn:      {contact['linkedin_url']}")
        print(f"\nStatus:        {contact['status']}")
        print(f"Last Contact:  {contact['last_contact']}")
        print(f"Next Action:   {contact['next_action']}")
        print(f"Action Date:   {contact['next_action_date']}")
        print(f"Priority:      {contact['priority_score']}")
        print(f"\nNotes:         {contact['notes']}")
        print(f"Tags:          {contact['tags']}")
        print(f"{'='*60}\n")

    def setup_network_commands(self, subparsers):
        """Setup network analysis subcommands"""
        network_parser = subparsers.add_parser('network', help='Network analysis')
        network_sub = network_parser.add_subparsers(dest='subcommand')

        network_sub.add_parser('analyze', help='Show comprehensive network analysis')
        network_sub.add_parser('multipliers', help='Identify network multipliers')
        network_sub.add_parser('brokers', help='Show brokers (high betweenness)')
        network_sub.add_parser('influence', help='Show network influence scores')

        reach_parser = network_sub.add_parser('reach', help='Calculate network reach')
        reach_parser.add_argument('contact_id', help='Contact ID')
        reach_parser.add_argument('--degrees', type=int, default=2, help='Degrees of separation')

        network_sub.add_parser('export', help='Export network graph')

    def setup_relationship_commands(self, subparsers):
        """Setup relationship management subcommands"""
        rel_parser = subparsers.add_parser('relationship', help='Relationship management')
        rel_sub = rel_parser.add_subparsers(dest='subcommand')

        # Add relationship
        add_parser = rel_sub.add_parser('add', help='Add relationship between contacts')
        add_parser.add_argument('contact_id_1', help='First contact ID')
        add_parser.add_argument('contact_id_2', help='Second contact ID')
        add_parser.add_argument('--type', default='knows', help='Relationship type')
        add_parser.add_argument('--strength', type=float, default=0.5,
                               help='Tie strength 0.0-1.0 (0.0-0.3=weak, 0.4-0.6=medium, 0.7-1.0=strong)')
        add_parser.add_argument('--notes', default='', help='Notes')

        # Show relationships
        show_parser = rel_sub.add_parser('show', help='Show relationships for a contact')
        show_parser.add_argument('contact_id', help='Contact ID')

        # Find mutual connections
        mutual_parser = rel_sub.add_parser('mutual', help='Find mutual connections')
        mutual_parser.add_argument('contact_id_1', help='First contact ID')
        mutual_parser.add_argument('contact_id_2', help='Second contact ID')

        # Find warm intro paths
        path_parser = rel_sub.add_parser('intro-path', help='Find warm introduction path')
        path_parser.add_argument('target_contact_id', help='Target contact ID')

        # Introduction opportunities
        rel_sub.add_parser('opportunities', help='Find introduction opportunities')

    def setup_analytics_commands(self, subparsers):
        """Setup analytics subcommands"""
        analytics_parser = subparsers.add_parser('analytics', help='Advanced analytics')
        analytics_sub = analytics_parser.add_subparsers(dest='subcommand')

        analytics_sub.add_parser('show', help='Show advanced analytics dashboard')
        analytics_sub.add_parser('insights', help='Show insights and recommendations')
        analytics_sub.add_parser('funnel', help='Show conversion funnel')
        analytics_sub.add_parser('stalled', help='Show stalled contacts')
        analytics_sub.add_parser('predictions', help='Show week 12 predictions')

    def cmd_network(self, args):
        """Handle network analysis commands"""
        if args.subcommand == 'analyze':
            self.network_analysis.show_network_analysis_report()

        elif args.subcommand == 'multipliers':
            multipliers = self.network_analysis.identify_network_multipliers()
            print("\n🌟 NETWORK MULTIPLIERS")
            print("=" * 70)
            if multipliers:
                for i, m in enumerate(multipliers[:15], 1):
                    print(f"\n{i}. {m['name']} ({m['company']}) - Tier {m['tier']}")
                    print(f"   Multiplier Score: {m['multiplier_score']:.2f}")
                    print(f"   {m['why_valuable']}")
            else:
                print("No network data available. Add relationships first.")
            print()

        elif args.subcommand == 'brokers':
            brokers = self.network_analysis.calculate_betweenness_centrality()
            print("\n🌉 BROKERS (Bridge Different Groups)")
            print("=" * 70)
            for i, b in enumerate(brokers[:10], 1):
                print(f"{i}. {b['name']:<30} Broker Score: {b['broker_score']:.2f}")
            print()

        elif args.subcommand == 'influence':
            influence = self.network_analysis.calculate_network_influence_score()
            print("\n⚡ NETWORK INFLUENCE SCORES")
            print("=" * 70)
            for i, inf in enumerate(influence[:10], 1):
                print(f"{i}. {inf['name']:<30} Influence: {inf['influence_score']:.2f}")
            print()

        elif args.subcommand == 'reach':
            reach = self.network_analysis.calculate_network_reach(args.contact_id, args.degrees)
            contact = self.contact_mgr.get_contact(args.contact_id)
            if contact:
                print(f"\nNetwork Reach for {contact['name']}:")
                print(f"Total reachable: {reach['total_reach']} contacts within {args.degrees} degrees")
                if reach['reachable_contacts']:
                    print(f"\nSample reachable contacts:")
                    for rc in reach['reachable_contacts'][:10]:
                        print(f"  • {rc['name']} ({rc['company']})")
            print()

        elif args.subcommand == 'export':
            self.network_analysis.export_network_graph()

    def cmd_relationship(self, args):
        """Handle relationship commands"""
        if args.subcommand == 'add':
            rel_id = self.relationship_mgr.add_relationship(
                args.contact_id_1,
                args.contact_id_2,
                relationship_type=args.type,
                strength=args.strength,
                notes=args.notes
            )
            if rel_id:
                print(f"✓ Relationship added (ID: {rel_id})")

        elif args.subcommand == 'show':
            self.relationship_mgr.show_relationship_summary(args.contact_id)

        elif args.subcommand == 'mutual':
            mutual = self.relationship_mgr.find_mutual_connections(
                args.contact_id_1,
                args.contact_id_2
            )
            c1 = self.contact_mgr.get_contact(args.contact_id_1)
            c2 = self.contact_mgr.get_contact(args.contact_id_2)

            if c1 and c2:
                print(f"\nMutual Connections: {c1['name']} & {c2['name']}")
                print("=" * 60)
                if mutual:
                    for mc in mutual:
                        print(f"  • {mc['name']} ({mc['company']})")
                else:
                    print("No mutual connections found")
                print()

        elif args.subcommand == 'intro-path':
            paths = self.relationship_mgr.suggest_warm_intro_paths(args.target_contact_id)
            target = self.contact_mgr.get_contact(args.target_contact_id)

            if target:
                print(f"\nWarm Introduction Paths to: {target['name']}")
                print("=" * 60)
                if paths:
                    for i, path in enumerate(paths[:5], 1):
                        path_str = " → ".join(p['name'] for p in path['path'])
                        print(f"{i}. {path_str}")
                        print(f"   Degrees: {path['degrees']}, Strength: {path['strength']:.2f}")
                else:
                    print("No introduction paths found")
                print()

        elif args.subcommand == 'opportunities':
            opps = self.relationship_mgr.identify_introduction_opportunities()
            print("\n🤝 INTRODUCTION OPPORTUNITIES")
            print("=" * 70)
            if opps:
                for i, opp in enumerate(opps[:10], 1):
                    print(f"{i}. {opp['action']}")
                    print(f"   Reason: {opp['reason']}")
            else:
                print("No introduction opportunities found")
            print()

    def cmd_analytics(self, args):
        """Handle analytics commands"""
        if args.subcommand == 'show':
            self.analytics.show_advanced_analytics()

        elif args.subcommand == 'insights':
            self.analytics.show_insights_report()

        elif args.subcommand == 'funnel':
            funnel = self.analytics.calculate_conversion_funnel()
            print("\n📊 CONVERSION FUNNEL")
            print("=" * 60)
            print(f"Total Contacts: {funnel['total']}")
            print(f"Cold: {funnel['cold']}")
            print(f"Outreach Sent: {funnel['outreach_sent']} ({funnel.get('outreach_rate', 0):.1f}%)")
            print(f"Meetings: {funnel['meeting_scheduled']} ({funnel.get('meeting_rate', 0):.1f}%)")
            print(f"Active Conversations: {funnel['active_conversation']}")
            print(f"Committed: {funnel['committed']} ({funnel.get('close_rate', 0):.1f}%)")
            print()

        elif args.subcommand == 'stalled':
            stalled = self.analytics.identify_stalled_contacts()
            print("\n⚠ STALLED CONTACTS (14+ days since last interaction)")
            print("=" * 70)
            if stalled:
                for i, s in enumerate(stalled[:15], 1):
                    print(f"{i}. {s['name']} ({s['company']})")
                    print(f"   Status: {s['status']} | {s['days_since_last_interaction']} days")
            else:
                print("No stalled contacts")
            print()

        elif args.subcommand == 'predictions':
            pred = self.analytics.predict_week_12_outcomes()
            print("\n🔮 WEEK 12 PROJECTIONS")
            print("=" * 60)
            print(f"Projected Meetings: {pred['total_meetings_projected']}")
            print(f"Projected Commits: {pred['total_commits_projected']}")
            print(f"\nHigh Probability Contacts ({len(pred['high_probability_contacts'])}):")
            for hp in pred['high_probability_contacts'][:10]:
                print(f"  • {hp['name']} ({hp['company']}) - {hp['probability']:.0f}%")
            print()

    def setup_public_markets_commands(self, subparsers):
        """Setup public markets subcommands"""
        public_parser = subparsers.add_parser('public', help='Public markets (for publicly traded fund)')
        public_sub = public_parser.add_subparsers(dest='subcommand')

        public_sub.add_parser('show', help='Show public market analysis')
        public_sub.add_parser('nav', help='Show NAV and premium/discount')
        public_sub.add_parser('comparables', help='Show comparable vehicles')
        public_sub.add_parser('investors', help='Show investor base composition')
        public_sub.add_parser('liquidity', help='Show liquidity metrics')

        # Add stock price
        price_parser = public_sub.add_parser('add-price', help='Add stock price data')
        price_parser.add_argument('--date', required=True, help='Date (YYYY-MM-DD)')
        price_parser.add_argument('--close', type=float, required=True, help='Closing price')
        price_parser.add_argument('--volume', type=int, required=True, help='Volume')

        # Add NAV
        nav_parser = public_sub.add_parser('add-nav', help='Add NAV data')
        nav_parser.add_argument('--date', required=True, help='Date (YYYY-MM-DD)')
        nav_parser.add_argument('--nav', type=float, required=True, help='NAV per share')
        nav_parser.add_argument('--shares', type=int, required=True, help='Shares outstanding')

    def setup_compliance_commands(self, subparsers):
        """Setup compliance subcommands"""
        compliance_parser = subparsers.add_parser('compliance', help='Regulatory compliance')
        compliance_sub = compliance_parser.add_subparsers(dest='subcommand')

        compliance_sub.add_parser('status', help='Show compliance dashboard')
        compliance_sub.add_parser('blackout', help='Check trading blackout status')

        calendar_parser = compliance_sub.add_parser('calendar', help='Show compliance calendar')
        calendar_parser.add_argument('--quarter', type=int, help='Quarter (1-4)')
        calendar_parser.add_argument('--year', type=int, help='Year')

        compliance_sub.add_parser('sec-filings', help='Show SEC filing requirements')
        compliance_sub.add_parser('insider-rules', help='Show insider trading rules')

    def cmd_public(self, args):
        """Handle public markets commands"""
        if args.subcommand == 'show':
            self.public_markets.generate_public_market_report()

        elif args.subcommand == 'nav':
            prem_disc = self.public_markets.calculate_premium_discount()
            if prem_disc:
                print(f"\nNAV ANALYSIS")
                print("=" * 60)
                print(f"Date:             {prem_disc['date']}")
                print(f"Stock Price:      ${prem_disc['stock_price']:.2f}")
                print(f"NAV per Share:    ${prem_disc['nav_per_share']:.2f}")
                print(f"Premium/Discount: {prem_disc['premium_discount']:+.2f}%")
                print(f"\n{prem_disc['interpretation']}")
                print()
            else:
                print("No NAV data available")

        elif args.subcommand == 'comparables':
            comps = self.public_markets.analyze_comparables()
            print("\nCOMPARABLE PUBLIC VEHICLES")
            print("=" * 80)
            if comps.get('comparables'):
                print(f"Peer Group: {comps['total_comps']} vehicles")
                print(f"Avg Premium/Discount: {comps['avg_premium_discount']:+.2f}%\n")
                for comp in comps['comparables']:
                    print(f"{comp['ticker']:<8} {comp['name']:<35} {comp.get('premium_discount', 'N/A'):>8}%")
                    print(f"         {comp['type']:<35} {comp.get('strategy', '')}")
                    print()
            else:
                print("No comparables data available")

        elif args.subcommand == 'investors':
            investor_data = self.public_markets.track_investor_base()
            print("\nINVESTOR BASE ANALYSIS")
            print("=" * 60)
            print(f"Total Shareholders: {investor_data['total_shareholders']}")
            print(f"Total Shares:       {investor_data['total_shares']:,}")
            print(f"\nComposition:")
            for inv_type, data in investor_data['composition'].items():
                if data['percent'] > 0:
                    print(f"  {inv_type:<15} {data['percent']:>5.1f}%  ({data['shares']:,} shares, {data['count']} holders)")
            print(f"\nConcentration:")
            print(f"  Top 10 Holders:  {investor_data['concentration']['top_10_ownership']:.1f}%")
            print()

        elif args.subcommand == 'liquidity':
            liquidity = self.public_markets.calculate_liquidity_metrics()
            if 'avg_daily_volume' in liquidity:
                print("\nLIQUIDITY METRICS")
                print("=" * 60)
                print(f"Avg Daily Volume:  {liquidity['avg_daily_volume']:,.0f} shares")
                print(f"Avg Daily Value:   ${liquidity['avg_daily_value']:,.0f}")
                print(f"20-Day Volatility: {liquidity['volatility_20d']:.2f}%")
                print(f"Liquidity Score:   {liquidity['liquidity_score']:.0f}/100")
                print()
            else:
                print("Insufficient data for liquidity analysis")

        elif args.subcommand == 'add-price':
            self.public_markets.add_stock_price(
                date=args.date,
                open_price=args.close - 0.10,
                high=args.close + 0.20,
                low=args.close - 0.20,
                close=args.close,
                volume=args.volume,
                market_cap=args.close * 10000000
            )
            print(f"✓ Added stock price: ${args.close:.2f} on {args.date}")

        elif args.subcommand == 'add-nav':
            premium_discount = self.public_markets.add_nav_data(
                date=args.date,
                nav_per_share=args.nav,
                total_nav=args.nav * args.shares,
                shares_outstanding=args.shares
            )
            print(f"✓ Added NAV: ${args.nav:.2f} on {args.date}")
            print(f"  Premium/Discount: {premium_discount:+.2f}%")

    def cmd_compliance(self, args):
        """Handle compliance commands"""
        if args.subcommand == 'status':
            self.compliance.generate_compliance_dashboard()

        elif args.subcommand == 'blackout':
            status = self.compliance.check_blackout_status()
            print("\nTRADING WINDOW STATUS")
            print("=" * 60)
            icon = "🔴" if status['status'] == 'BLACKOUT' else "🟢"
            print(f"{icon} Status: {status['status']}")
            print(f"Can Trade: {'No' if not status['can_trade'] else 'Yes'}")
            if not status['can_trade']:
                print(f"Reason: {status['reason']}")
                print(f"Ends: {status['end_date']}")
                print(f"Affected: {status['affected_persons']}")
            print()

        elif args.subcommand == 'calendar':
            from datetime import datetime
            quarter = args.quarter or ((datetime.now().month - 1) // 3 + 1)
            year = args.year or datetime.now().year

            calendar = self.compliance.generate_quarterly_calendar(quarter, year)
            print(f"\nCOMPLIANCE CALENDAR - {calendar['quarter']}")
            print("=" * 70)
            print(f"Quarter End:        {calendar['quarter_end']}")
            if calendar['10q_due'] != 'N/A':
                print(f"10-Q Due:           {calendar['10q_due']}")
            if calendar['10k_due'] != 'N/A':
                print(f"10-K Due:           {calendar['10k_due']}")
            print(f"Earnings Call:      {calendar['earnings_call']}")
            print(f"Blackout Period:    {calendar['blackout_start']} to {calendar['blackout_end']}")
            print()

        elif args.subcommand == 'sec-filings':
            requirements = self.compliance.identify_disclosure_requirements()
            print("\nSEC FILING REQUIREMENTS")
            print("=" * 70)
            for req in requirements:
                print(f"\n{req['type']}")
                print(f"  Frequency: {req['frequency']}")
                print(f"  Deadline:  {req['deadline']}")
                print(f"  Content:   {req['description']}")

        elif args.subcommand == 'insider-rules':
            requirements = self.compliance.get_insider_trading_requirements()
            print("\nINSIDER TRADING REQUIREMENTS (Section 16)")
            print("=" * 70)
            for form, details in requirements.items():
                print(f"\n{form}")
                print(f"  Description: {details['description']}")
                print(f"  Deadline:    {details['deadline']}")
                print(f"  Who:         {details['who']}")
            print()

    def setup_portfolio_commands(self, subparsers):
        """Setup portfolio management subcommands"""
        portfolio_parser = subparsers.add_parser('portfolio', help='Portfolio management')
        portfolio_sub = portfolio_parser.add_subparsers(dest='subcommand')

        portfolio_sub.add_parser('show', help='Show portfolio dashboard')
        portfolio_sub.add_parser('performance', help='Show fund performance')

        cashflow_parser = portfolio_sub.add_parser('cashflow', help='Forecast capital calls')
        cashflow_parser.add_argument('--months', type=int, default=12, help='Forecast months')

        portfolio_sub.add_parser('diversification', help='Analyze portfolio construction')

        # Add fund
        add_fund_parser = portfolio_sub.add_parser('add-fund', help='Add fund investment')
        add_fund_parser.add_argument('--name', required=True, help='Fund name')
        add_fund_parser.add_argument('--manager', required=True, help='Manager name')
        add_fund_parser.add_argument('--commitment', type=float, required=True, help='Commitment amount')
        add_fund_parser.add_argument('--vintage', type=int, required=True, help='Vintage year')
        add_fund_parser.add_argument('--stage', default='', help='Stage focus')
        add_fund_parser.add_argument('--sector', default='', help='Sector focus')

    def setup_manager_commands(self, subparsers):
        """Setup manager CRM subcommands"""
        manager_parser = subparsers.add_parser('managers', help='Fund manager CRM')
        manager_sub = manager_parser.add_subparsers(dest='subcommand')

        manager_sub.add_parser('pipeline', help='Show manager pipeline')
        manager_sub.add_parser('referrals', help='Analyze referral sources')

        # Add manager
        add_mgr_parser = manager_sub.add_parser('add', help='Add manager to pipeline')
        add_mgr_parser.add_argument('--fund', required=True, help='Fund name')
        add_mgr_parser.add_argument('--gps', required=True, help='GP names')
        add_mgr_parser.add_argument('--firm', required=True, help='Firm name')
        add_mgr_parser.add_argument('--stage', default='', help='Stage focus')
        add_mgr_parser.add_argument('--source', default='', help='Referral source')

        # DD status
        dd_parser = manager_sub.add_parser('dd', help='Show due diligence status')
        dd_parser.add_argument('manager_id', help='Manager ID')

        # Start DD
        start_dd_parser = manager_sub.add_parser('start-dd', help='Start due diligence')
        start_dd_parser.add_argument('manager_id', help='Manager ID')
        start_dd_parser.add_argument('--analyst', required=True, help='Lead analyst')

    def cmd_portfolio(self, args):
        """Handle portfolio commands"""
        if args.subcommand == 'show':
            self.portfolio.show_portfolio_dashboard()

        elif args.subcommand == 'performance':
            summary = self.portfolio.get_portfolio_summary()
            print("\n📊 FUND PERFORMANCE")
            print("="*80)
            for fund in sorted(summary['funds'], key=lambda x: x['tvpi'], reverse=True):
                print(f"\n{fund['fund_name']}")
                print(f"  Manager:      {fund['manager']}")
                print(f"  Vintage:      {fund['vintage_year']}")
                print(f"  Commitment:   ${fund['commitment']:,.0f}")
                print(f"  Paid In:      ${fund['paid_in']:,.0f}")
                print(f"  Current NAV:  ${fund['current_nav']:,.0f}")
                print(f"  Distributed:  ${fund['distributions']:,.0f}")
                print(f"  TVPI:         {fund['tvpi']:.2f}x")
                print(f"  DPI:          {fund['dpi']:.2f}x")
                print(f"  RVPI:         {fund['rvpi']:.2f}x")
                print(f"  IRR:          {fund['irr']:.1f}%")
            print()

        elif args.subcommand == 'cashflow':
            self.portfolio.show_cashflow_forecast(args.months)

        elif args.subcommand == 'diversification':
            analysis = self.portfolio.analyze_portfolio_construction()
            print("\n🎯 PORTFOLIO CONSTRUCTION ANALYSIS")
            print("="*70)
            print(f"Diversification Score: {analysis['diversification_score']}/100")

            if analysis['warnings']:
                print(f"\n⚠️  WARNINGS ({len(analysis['warnings'])})")
                for warning in analysis['warnings']:
                    print(f"  {warning}")

            print(f"\n📊 BY VINTAGE YEAR")
            for vintage, data in sorted(analysis['by_vintage'].items()):
                pct = (data['commitment'] / self.portfolio.get_portfolio_summary()['total_commitment'] * 100)
                print(f"  {vintage}: {data['count']} funds, ${data['commitment']:,.0f} ({pct:.1f}%)")

            print(f"\n📊 BY STAGE")
            for stage, data in sorted(analysis['by_stage'].items()):
                if data['commitment'] > 0:
                    pct = (data['commitment'] / self.portfolio.get_portfolio_summary()['total_commitment'] * 100)
                    print(f"  {stage}: {data['count']} funds, ${data['commitment']:,.0f} ({pct:.1f}%)")
            print()

        elif args.subcommand == 'add-fund':
            fund_id = self.portfolio.add_fund(
                fund_name=args.name,
                manager_name=args.manager,
                commitment=args.commitment,
                vintage_year=args.vintage,
                stage_focus=args.stage,
                sector_focus=args.sector
            )

    def cmd_managers(self, args):
        """Handle manager CRM commands"""
        if args.subcommand == 'pipeline':
            self.manager_crm.show_pipeline_dashboard()

        elif args.subcommand == 'add':
            manager_id = self.manager_crm.add_manager(
                fund_name=args.fund,
                gp_names=args.gps,
                firm_name=args.firm,
                stage_focus=args.stage,
                source=args.source
            )

        elif args.subcommand == 'dd':
            self.manager_crm.show_dd_status(args.manager_id)

        elif args.subcommand == 'start-dd':
            self.manager_crm.start_due_diligence(args.manager_id, args.analyst)

        elif args.subcommand == 'referrals':
            referrals = self.manager_crm.get_referral_analytics()
            print("\n🤝 REFERRAL SOURCE ANALYTICS")
            print("="*70)
            for source, data in sorted(referrals.items(), key=lambda x: -x[1]['conversion_rate']):
                print(f"\n{source}")
                print(f"  Total:          {data['total']}")
                print(f"  Committed:      {data['committed']}")
                print(f"  Active:         {data['active']}")
                print(f"  Passed:         {data['passed']}")
                print(f"  Conversion:     {data['conversion_rate']:.1f}%")
            print()

    def setup_risk_commands(self, subparsers):
        """Setup risk management subcommands"""
        risk_parser = subparsers.add_parser('risk', help='Portfolio risk management')
        risk_sub = risk_parser.add_subparsers(dest='subcommand')

        risk_sub.add_parser('dashboard', help='Show comprehensive risk dashboard')
        risk_sub.add_parser('concentration', help='Check concentration risk')
        risk_sub.add_parser('vintage', help='Analyze vintage year risk')
        risk_sub.add_parser('liquidity', help='Check liquidity risk')
        risk_sub.add_parser('correlation', help='Analyze fund correlations')
        risk_sub.add_parser('governance', help='Governance compliance report')

    def cmd_risk(self, args):
        """Handle risk management commands"""
        if args.subcommand == 'dashboard':
            self.risk.show_risk_dashboard()

        elif args.subcommand == 'concentration':
            result = self.risk.check_concentration_risk()
            print("\n🎯 CONCENTRATION RISK CHECK")
            print("="*70)
            print(f"Status: {result['status']}")
            print(f"Fund Count: {result['fund_count']}")

            if result['violations']:
                print(f"\n⚠️  VIOLATIONS ({len(result['violations'])})")
                for v in result['violations']:
                    print(f"  • {v['message']}")

            if result['warnings']:
                print(f"\n⚡ WARNINGS ({len(result['warnings'])})")
                for w in result['warnings']:
                    print(f"  • {w['message']}")

            if not result['violations'] and not result['warnings']:
                print("\n✓ All concentration limits compliant")
            print()

        elif args.subcommand == 'vintage':
            result = self.risk.check_vintage_risk()
            print("\n📅 VINTAGE YEAR RISK ANALYSIS")
            print("="*70)
            print(f"Bubble Era Exposure (2020-2021): {result['bubble_exposure']:.1%}")
            print(f"Correction Era Exposure (2023-2024): {result['correction_exposure']:.1%}")
            print(f"Vintage Diversification: {result['diversification_score']} years")

            print(f"\nVintage Breakdown:")
            for vintage, data in sorted(result['vintage_breakdown'].items()):
                print(f"  {vintage}: {data['percentage']:.1%} ({data['count']} funds) - Risk: {data['risk_level']}")

            if result['recommendations']:
                print(f"\nRecommendations:")
                for rec in result['recommendations']:
                    print(f"  {rec}")
            print()

        elif args.subcommand == 'liquidity':
            result = self.risk.check_liquidity_risk()
            print("\n💰 LIQUIDITY RISK CHECK")
            print("="*70)
            print(f"Unfunded Commitments: ${result['unfunded_commitments']:,.0f}")
            print(f"12-Month Forecast: ${result['forecast_12m']:,.0f}")
            print(f"Required Cash Reserve: ${result['required_cash_reserve']:,.0f}")

            if result['recommendations']:
                print(f"\nRecommendations:")
                for rec in result['recommendations']:
                    print(f"  • {rec}")
            print()

        elif args.subcommand == 'correlation':
            result = self.risk.analyze_correlation_risk()
            print("\n🔗 CORRELATION RISK ANALYSIS")
            print("="*70)
            print(f"Status: {result['status']}")
            print(f"Tracked Correlations: {result['tracked_correlations']}")
            print(f"High Overlap Pairs: {result['high_overlap_pairs']}")

            if result['recommendations']:
                print(f"\nRecommendations:")
                for rec in result['recommendations']:
                    print(f"  • {rec}")
            print()

        elif args.subcommand == 'governance':
            self.risk.show_governance_report()

    def setup_board_commands(self, subparsers):
        """Setup board reporting subcommands"""
        board_parser = subparsers.add_parser('board', help='Board meeting materials')
        board_sub = board_parser.add_subparsers(dest='subcommand')

        # Generate board deck
        deck_parser = board_sub.add_parser('deck', help='Generate board deck')
        deck_parser.add_argument('--quarter', type=int, help='Quarter (1-4)')
        deck_parser.add_argument('--year', type=int, help='Year')
        deck_parser.add_argument('--format', choices=['markdown', 'text'], default='markdown', help='Output format')

        # Action items
        board_sub.add_parser('actions', help='List action items')

        add_action_parser = board_sub.add_parser('add-action', help='Add action item')
        add_action_parser.add_argument('item', help='Action item description')
        add_action_parser.add_argument('--owner', required=True, help='Item owner')
        add_action_parser.add_argument('--due', required=True, help='Due date (YYYY-MM-DD)')

        update_action_parser = board_sub.add_parser('update-action', help='Update action item')
        update_action_parser.add_argument('item_id', help='Action item ID')
        update_action_parser.add_argument('--status', help='New status')
        update_action_parser.add_argument('--notes', help='Notes')

    def cmd_board(self, args):
        """Handle board reporting commands"""
        if args.subcommand == 'deck':
            print("\n🎯 Generating board deck...")
            output_path = self.board.generate_board_deck(
                output_format=args.format
            )
            print(f"\n✓ Board deck generated: {output_path}")
            print(f"\nOpen with: open {output_path}")

        elif args.subcommand == 'actions':
            action_items = self.board.list_action_items()
            print("\n📋 BOARD ACTION ITEMS")
            print("="*70)

            open_items = [item for item in action_items if item['status'] != 'Completed']
            completed_items = [item for item in action_items if item['status'] == 'Completed']

            if open_items:
                print(f"\n🔓 Open Items ({len(open_items)})")
                for item in open_items:
                    print(f"\n{item['item_id']}: {item['item']}")
                    print(f"  Owner: {item['owner']}")
                    print(f"  Due: {item['due_date']}")
                    print(f"  Status: {item['status']}")

            if completed_items:
                print(f"\n✅ Recently Completed ({len(completed_items)})")
                for item in completed_items[:5]:
                    print(f"\n{item['item_id']}: {item['item']}")
                    print(f"  Completed: {item['completed_date']}")
            print()

        elif args.subcommand == 'add-action':
            self.board.add_action_item(
                item=args.item,
                owner=args.owner,
                due_date=args.due
            )

        elif args.subcommand == 'update-action':
            self.board.update_action_item(
                item_id=args.item_id,
                status=args.status,
                notes=args.notes
            )

    def setup_lp_commands(self, subparsers):
        """Setup LP reporting subcommands"""
        lp_parser = subparsers.add_parser('lp', help='LP reporting and communications')
        lp_sub = lp_parser.add_subparsers(dest='subcommand')

        # Quarterly letter
        letter_parser = lp_sub.add_parser('letter', help='Generate quarterly LP letter')
        letter_parser.add_argument('--quarter', type=int, help='Quarter (1-4)')
        letter_parser.add_argument('--year', type=int, help='Year')

        # Capital call notice
        call_parser = lp_sub.add_parser('capital-call', help='Generate capital call notice')
        call_parser.add_argument('fund_id', help='Fund ID')
        call_parser.add_argument('amount', type=float, help='Call amount')
        call_parser.add_argument('due_date', help='Due date (YYYY-MM-DD)')

        # Distribution notice
        dist_parser = lp_sub.add_parser('distribution', help='Generate distribution notice')
        dist_parser.add_argument('fund_id', help='Fund ID')
        dist_parser.add_argument('amount', type=float, help='Distribution amount')
        dist_parser.add_argument('date', help='Distribution date (YYYY-MM-DD)')

        # Annual summary
        annual_parser = lp_sub.add_parser('annual', help='Generate annual summary')
        annual_parser.add_argument('year', type=int, help='Year')

    def cmd_lp(self, args):
        """Handle LP reporting commands"""
        if args.subcommand == 'letter':
            print("\n📝 Generating quarterly LP letter...")
            output_path = self.lp_reporting.generate_quarterly_letter(
                quarter=args.quarter,
                year=args.year
            )
            print(f"\n✓ Quarterly letter generated: {output_path}")
            print(f"\nOpen with: open {output_path}")
            print(f"\nNote: Edit the CEO message and market commentary sections before distribution")

        elif args.subcommand == 'capital-call':
            print(f"\n💰 Generating capital call notice for {args.fund_id}...")
            output_path = self.lp_reporting.generate_capital_call_notice(
                fund_id=args.fund_id,
                amount=args.amount,
                due_date=args.due_date
            )
            print(f"\n✓ Capital call notice generated: {output_path}")
            print(f"\nOpen with: open {output_path}")

        elif args.subcommand == 'distribution':
            print(f"\n💵 Generating distribution notice for {args.fund_id}...")
            output_path = self.lp_reporting.generate_distribution_notice(
                fund_id=args.fund_id,
                amount=args.amount,
                distribution_date=args.date
            )
            print(f"\n✓ Distribution notice generated: {output_path}")
            print(f"\nOpen with: open {output_path}")

        elif args.subcommand == 'annual':
            print(f"\n📊 Generating annual summary for {args.year}...")
            output_path = self.lp_reporting.generate_annual_summary(year=args.year)
            print(f"\n✓ Annual summary generated: {output_path}")
            print(f"\nOpen with: open {output_path}")

    def setup_finance_commands(self, subparsers):
        """Setup financial modeling subcommands"""
        finance_parser = subparsers.add_parser('finance', help='Financial modeling and forecasting')
        finance_sub = finance_parser.add_subparsers(dest='subcommand')

        # Scenario analysis
        scenario_parser = finance_sub.add_parser('scenarios', help='Run scenario analysis')
        scenario_parser.add_argument('--years', type=int, default=3, help='Years to project')

        # Cash flow projection
        cashflow_parser = finance_sub.add_parser('project', help='Project cash flows')
        cashflow_parser.add_argument('--years', type=int, default=3, help='Years to project')
        cashflow_parser.add_argument('--scenario', choices=['bull', 'base', 'bear'], default='base', help='Scenario')

        # Budget variance
        variance_parser = finance_sub.add_parser('variance', help='Budget vs actual variance')
        variance_parser.add_argument('--year', type=int, help='Year to analyze')

        # Fundraising analysis
        fundraise_parser = finance_sub.add_parser('fundraising', help='Fundraising analysis')
        fundraise_parser.add_argument('cash', type=float, help='Current cash position')
        fundraise_parser.add_argument('--runway', type=int, default=24, help='Desired runway in months')

        # Budget management
        add_budget_parser = finance_sub.add_parser('add-budget', help='Add budget line item')
        add_budget_parser.add_argument('year', type=int, help='Year')
        add_budget_parser.add_argument('category', help='Category')
        add_budget_parser.add_argument('amount', type=float, help='Budgeted amount')

        add_actual_parser = finance_sub.add_parser('add-actual', help='Log actual spending')
        add_actual_parser.add_argument('month', type=int, help='Month (1-12)')
        add_actual_parser.add_argument('year', type=int, help='Year')
        add_actual_parser.add_argument('category', help='Category')
        add_actual_parser.add_argument('amount', type=float, help='Actual amount')

    def cmd_finance(self, args):
        """Handle financial modeling commands"""
        if args.subcommand == 'scenarios':
            self.finance.show_scenario_comparison(years=args.years)

        elif args.subcommand == 'project':
            projections = self.finance.project_cashflow(years=args.years, scenario=args.scenario)

            print(f"\n📊 CASH FLOW PROJECTION - {args.scenario.upper()} SCENARIO")
            print("="*80)

            for proj in projections:
                print(f"\nYear {proj['year']}:")
                print(f"  Capital Calls:       ${proj['capital_calls']:>15,.0f}")
                print(f"  Distributions:       ${proj['distributions']:>15,.0f}")
                print(f"  New Commitments:     ${proj['new_commitments']:>15,.0f}")
                print(f"  Management Fees:     ${proj['management_fees']:>15,.0f}")
                print(f"  Operating Expenses:  ${proj['operating_expenses']:>15,.0f}")
                print(f"  ─────────────────────────────────────")
                print(f"  Net Cash Flow:       ${proj['net_cashflow']:>15,.0f}")
                print(f"  Estimated NAV:       ${proj['nav_estimate']:>15,.0f}")

            print("\n" + "="*80 + "\n")

        elif args.subcommand == 'variance':
            self.finance.show_budget_variance(year=args.year)

        elif args.subcommand == 'fundraising':
            self.finance.show_fundraising_analysis(current_cash=args.cash)

        elif args.subcommand == 'add-budget':
            self.finance.add_budget(
                year=args.year,
                category=args.category,
                amount=args.amount
            )

        elif args.subcommand == 'add-actual':
            self.finance.add_actual(
                month=args.month,
                year=args.year,
                category=args.category,
                amount=args.amount
            )

    def setup_intel_commands(self, subparsers):
        """Setup competitive intelligence subcommands"""
        intel_parser = subparsers.add_parser('intel', help='Competitive intelligence')
        intel_sub = intel_parser.add_subparsers(dest='subcommand')

        # Competitor landscape
        intel_sub.add_parser('landscape', help='Show competitor landscape')

        # Manager universe
        universe_parser = intel_sub.add_parser('universe', help='Show manager universe')
        universe_parser.add_argument('--stage', help='Filter by stage')
        universe_parser.add_argument('--sector', help='Filter by sector')
        universe_parser.add_argument('--status', help='Filter by our status')

        # Fee benchmarks
        intel_sub.add_parser('fees', help='Show fee benchmarks')

        # LP overlap
        intel_sub.add_parser('lp-overlap', help='Analyze LP overlap')

        # Positioning matrix
        intel_sub.add_parser('positioning', help='Show competitive positioning')

        # Market trends
        intel_sub.add_parser('trends', help='Show market trends')

        # Add competitor
        add_comp_parser = intel_sub.add_parser('add-competitor', help='Add competitor')
        add_comp_parser.add_argument('name', help='Competitor name')
        add_comp_parser.add_argument('type', help='Vehicle type')
        add_comp_parser.add_argument('--aum', type=float, default=0, help='AUM')
        add_comp_parser.add_argument('--fee', type=float, default=0, help='Management fee %')

        # Add manager
        add_mgr_parser = intel_sub.add_parser('add-manager', help='Add manager to universe')
        add_mgr_parser.add_argument('firm', help='Firm name')
        add_mgr_parser.add_argument('fund', help='Fund name')
        add_mgr_parser.add_argument('size', type=float, help='Fund size')
        add_mgr_parser.add_argument('vintage', type=int, help='Vintage year')
        add_mgr_parser.add_argument('--stage', default='', help='Stage focus')
        add_mgr_parser.add_argument('--sector', default='', help='Sector focus')

    def cmd_intel(self, args):
        """Handle competitive intelligence commands"""
        if args.subcommand == 'landscape':
            self.intel.show_competitor_landscape()

        elif args.subcommand == 'universe':
            filters = {}
            if args.stage:
                filters['stage_focus'] = args.stage
            if args.sector:
                filters['sector_focus'] = args.sector
            if args.status:
                filters['our_status'] = args.status

            self.intel.show_manager_universe(filters if filters else None)

        elif args.subcommand == 'fees':
            self.intel.show_fee_benchmarks()

        elif args.subcommand == 'lp-overlap':
            self.intel.show_lp_overlap()

        elif args.subcommand == 'positioning':
            self.intel.show_positioning_matrix()

        elif args.subcommand == 'trends':
            self.intel.show_market_trends()

        elif args.subcommand == 'add-competitor':
            self.intel.add_competitor(
                name=args.name,
                type=args.type,
                aum=args.aum,
                management_fee=args.fee
            )

        elif args.subcommand == 'add-manager':
            self.intel.add_manager_to_universe(
                firm_name=args.firm,
                fund_name=args.fund,
                fund_size=args.size,
                vintage=args.vintage,
                stage_focus=args.stage,
                sector_focus=args.sector
            )

    def setup_team_commands(self, subparsers):
        """Setup team management commands"""
        team_parser = subparsers.add_parser('team', help='Team management')
        team_sub = team_parser.add_subparsers(dest='team_command')

        # Workload report
        workload = team_sub.add_parser('workload', help='Team workload report')
        workload.add_argument('--member-id', help='Filter by member ID')
        workload.add_argument('--status', help='Filter by status')

        # IC voting analysis
        ic_votes = team_sub.add_parser('ic-votes', help='IC voting history and analysis')
        ic_votes.add_argument('--member-id', help='Filter by member ID')
        ic_votes.add_argument('--manager-id', help='Filter by manager ID')

        # Professional development
        development = team_sub.add_parser('development', help='Professional development report')
        development.add_argument('--member-id', help='Filter by member ID')

        # Capacity analysis
        capacity = team_sub.add_parser('capacity', help='Team capacity analysis')

        # Add team member
        add_member = team_sub.add_parser('add-member', help='Add new team member')
        add_member.add_argument('name', help='Full name')
        add_member.add_argument('title', help='Job title')
        add_member.add_argument('role', help='Role category')
        add_member.add_argument('--hire-date', help='Hire date (YYYY-MM-DD)')
        add_member.add_argument('--email', help='Email address')

        # Assign work
        assign_work = team_sub.add_parser('assign-work', help='Assign work to team member')
        assign_work.add_argument('member_id', help='Team member ID')
        assign_work.add_argument('task_type', help='Type of task')
        assign_work.add_argument('description', help='Task description')
        assign_work.add_argument('--related-id', help='Related manager/fund ID')
        assign_work.add_argument('--hours', type=float, help='Estimated hours')
        assign_work.add_argument('--due-date', help='Due date (YYYY-MM-DD)')

        # Log development activity
        log_dev = team_sub.add_parser('log-development', help='Log professional development activity')
        log_dev.add_argument('member_id', help='Team member ID')
        log_dev.add_argument('activity_type', help='Activity type')
        log_dev.add_argument('description', help='Activity description')
        log_dev.add_argument('--hours', type=float, help='Hours spent')
        log_dev.add_argument('--competency', help='Competency area')

        # Record IC vote
        record_vote = team_sub.add_parser('record-vote', help='Record IC vote')
        record_vote.add_argument('member_id', help='Team member ID')
        record_vote.add_argument('manager_id', help='Manager ID')
        record_vote.add_argument('vote', choices=['Yes', 'No', 'Abstain'], help='Vote')
        record_vote.add_argument('rationale', help='Vote rationale')
        record_vote.add_argument('--ic-date', help='IC date (YYYY-MM-DD)')

    def cmd_team(self, args):
        """Handle team management commands"""
        if args.team_command == 'workload':
            self.team.show_team_workload(member_id=args.member_id)

        elif args.team_command == 'ic-votes':
            if args.member_id or args.manager_id:
                # Show filtered votes
                votes = self.team._load_csv(self.team.ic_votes_file)
                members = self.team._load_csv(self.team.team_members_file)

                if args.member_id:
                    votes = [v for v in votes if v['member_id'] == args.member_id]
                if args.manager_id:
                    votes = [v for v in votes if v['manager_id'] == args.manager_id]

                print("\n" + "="*80)
                print("IC VOTING HISTORY")
                print("="*80)

                if not votes:
                    print("\nNo voting data found")
                else:
                    for vote in votes:
                        member = next((m for m in members if m['member_id'] == vote['member_id']), None)
                        member_name = member['name'] if member else vote['member_id']

                        print(f"\n{vote['ic_date']} | {member_name} | {vote['manager_id']}")
                        print(f"  Vote: {vote['vote']}")
                        print(f"  Rationale: {vote['rationale']}")
                        if vote['fund_performance']:
                            print(f"  Performance: {vote['fund_performance']}")
                        if vote['outcome']:
                            print(f"  Outcome: {vote['outcome']}")

                print("\n" + "="*80 + "\n")
            else:
                # Show full analysis
                self.team.show_ic_voting_patterns()

        elif args.team_command == 'development':
            self.team.show_team_development(member_id=args.member_id)

        elif args.team_command == 'capacity':
            self.team.show_capacity_analysis()

        elif args.team_command == 'add-member':
            member_id = self.team.add_team_member(
                name=args.name,
                title=args.title,
                role=args.role,
                hire_date=args.hire_date,
                email=args.email
            )
            print(f"✓ Added team member: {args.name} ({member_id})")

        elif args.team_command == 'assign-work':
            work_id = self.team.assign_work(
                member_id=args.member_id,
                task_type=args.task_type,
                description=args.description,
                related_id=args.related_id,
                hours_estimated=args.hours,
                due_date=args.due_date
            )
            print(f"✓ Assigned work item: {work_id}")

        elif args.team_command == 'log-development':
            activity_id = self.team.log_development_activity(
                member_id=args.member_id,
                activity_type=args.activity_type,
                description=args.description,
                hours=args.hours,
                competency=args.competency
            )
            print(f"✓ Logged development activity: {activity_id}")

        elif args.team_command == 'record-vote':
            vote_id = self.team.record_ic_vote(
                ic_date=args.ic_date,
                manager_id=args.manager_id,
                member_id=args.member_id,
                vote=args.vote,
                rationale=args.rationale
            )
            print(f"✓ Recorded IC vote: {vote_id}")

    def setup_governance_commands(self, subparsers):
        """Setup institutional governance commands"""
        gov_parser = subparsers.add_parser('governance', help='Institutional governance')
        gov_sub = gov_parser.add_subparsers(dest='governance_command')

        # IC Committee
        ic_committee = gov_sub.add_parser('ic-committee', help='Show IC committee composition')

        # IC Meetings
        ic_meetings = gov_sub.add_parser('ic-meetings', help='Show IC meeting history')
        ic_meetings.add_argument('--since', help='Show meetings since date (YYYY-MM-DD)')

        # Co-invest Pipeline
        coinvest = gov_sub.add_parser('coinvest-pipeline', help='Show co-invest decision pipeline')
        coinvest.add_argument('--tier', help='Filter by tier')

        # Manager Contacts
        contacts = gov_sub.add_parser('manager-contacts', help='Show manager relationship tracking')
        contacts.add_argument('--manager-id', help='Filter by manager ID')
        contacts.add_argument('--since', help='Show contacts since date (YYYY-MM-DD)')

        # Governance Calendar
        calendar = gov_sub.add_parser('calendar', help='Show governance calendar')
        calendar.add_argument('--days', type=int, default=90, help='Show next N days')

        # IC Activity Report
        ic_report = gov_sub.add_parser('ic-report', help='Generate quarterly IC activity report')
        ic_report.add_argument('--quarter-start', required=True, help='Quarter start date (YYYY-MM-DD)')
        ic_report.add_argument('--quarter-end', required=True, help='Quarter end date (YYYY-MM-DD)')

        # Add IC Member
        add_ic = gov_sub.add_parser('add-ic-member', help='Add IC committee member')
        add_ic.add_argument('member_id', help='Team member ID')
        add_ic.add_argument('name', help='Full name')
        add_ic.add_argument('--role', default='Member', help='IC Chair, Member, Independent Member')
        add_ic.add_argument('--voting', default='Full', help='Full, Advisory, Observer')
        add_ic.add_argument('--appointed', help='Appointed date (YYYY-MM-DD)')

        # Log IC Meeting
        log_meeting = gov_sub.add_parser('log-meeting', help='Log IC meeting')
        log_meeting.add_argument('date', help='Meeting date (YYYY-MM-DD)')
        log_meeting.add_argument('--type', default='Regular', help='Regular, Special, Emergency')
        log_meeting.add_argument('--attendees', help='Comma-separated member IDs')
        log_meeting.add_argument('--agenda', help='Meeting agenda')
        log_meeting.add_argument('--decisions', type=int, default=0, help='Number of decisions made')

        # Record Co-invest
        record_coinvest = gov_sub.add_parser('record-coinvest', help='Record co-invest decision')
        record_coinvest.add_argument('company', help='Company name')
        record_coinvest.add_argument('manager_id', help='Lead manager ID')
        record_coinvest.add_argument('tier', help='Watchlist, Signal Density, Base, Confirmed, Conviction')
        record_coinvest.add_argument('allocation', type=float, help='Allocation amount ($)')
        record_coinvest.add_argument('nav_pct', type=float, help='NAV percentage')
        record_coinvest.add_argument('vote', help='Approved, Declined, Defer, Watchlist')
        record_coinvest.add_argument('--rationale', help='Investment rationale')
        record_coinvest.add_argument('--managers', help='Participating managers (comma-separated)')

        # Log Manager Contact
        log_contact = gov_sub.add_parser('log-contact', help='Log manager contact')
        log_contact.add_argument('manager_id', help='Manager ID')
        log_contact.add_argument('manager_name', help='Manager firm name')
        log_contact.add_argument('type', help='Call, Meeting, Email, Pipeline Review, Quarterly Update')
        log_contact.add_argument('subject', help='Subject/topic')
        log_contact.add_argument('--outcome', help='Outcome of interaction')
        log_contact.add_argument('--next-steps', help='Follow-up actions')

    def cmd_governance(self, args):
        """Handle institutional governance commands"""
        if args.governance_command == 'ic-committee':
            self.governance.show_ic_committee()

        elif args.governance_command == 'ic-meetings':
            self.governance.show_ic_meetings(since_date=args.since)

        elif args.governance_command == 'coinvest-pipeline':
            self.governance.show_coinvest_pipeline(tier=args.tier)

        elif args.governance_command == 'manager-contacts':
            self.governance.show_manager_contacts(
                manager_id=args.manager_id,
                since_date=args.since
            )

        elif args.governance_command == 'calendar':
            self.governance.show_governance_calendar(upcoming_days=args.days)

        elif args.governance_command == 'ic-report':
            self.governance.generate_ic_activity_report(
                quarter_start=args.quarter_start,
                quarter_end=args.quarter_end
            )

        elif args.governance_command == 'add-ic-member':
            self.governance.add_ic_member(
                member_id=args.member_id,
                name=args.name,
                ic_role=args.role,
                voting_authority=args.voting,
                appointed_date=args.appointed
            )

        elif args.governance_command == 'log-meeting':
            self.governance.log_ic_meeting(
                meeting_date=args.date,
                meeting_type=args.type,
                attendees=args.attendees,
                agenda=args.agenda,
                decisions_made=args.decisions
            )

        elif args.governance_command == 'record-coinvest':
            self.governance.record_coinvest_decision(
                company_name=args.company,
                manager_id=args.manager_id,
                tier=args.tier,
                allocation_amount=args.allocation,
                nav_percentage=args.nav_pct,
                ic_vote=args.vote,
                rationale=args.rationale,
                managers_participating=args.managers
            )

        elif args.governance_command == 'log-contact':
            self.governance.log_manager_contact(
                manager_id=args.manager_id,
                manager_name=args.manager_name,
                contact_type=args.type,
                subject=args.subject,
                outcome=args.outcome,
                next_steps=args.next_steps
            )

    def print_tasks(self, tasks, title):
        """Print task list"""
        print(f"\n{title}")
        print("=" * 60)
        if not tasks:
            print("No tasks found")
        else:
            for i, task in enumerate(tasks, 1):
                print(f"{i}. [{task['contact_name']}] {task['action']} (Due: {task['date']})")
        print()


if __name__ == '__main__':
    cli = NewcoCLI()
    cli.run()

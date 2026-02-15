"""
Reporting and Analytics Module
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"


class ReportGenerator:
    """Generate various reports and dashboards"""

    def __init__(self):
        self.contacts_file = DATA_DIR / "contacts.csv"
        self.interactions_file = DATA_DIR / "interactions.csv"
        self.reports_dir = REPORTS_DIR / "weekly"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def load_contacts(self):
        """Load all contacts"""
        contacts = []
        if self.contacts_file.exists():
            with open(self.contacts_file, 'r') as f:
                reader = csv.DictReader(f)
                contacts = list(reader)
        return contacts

    def load_interactions(self):
        """Load all interactions"""
        interactions = []
        if self.interactions_file.exists():
            with open(self.interactions_file, 'r') as f:
                reader = csv.DictReader(f)
                interactions = list(reader)
        return interactions

    def generate_weekly_report(self):
        """Generate weekly markdown report"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=7)

        # Get data
        contacts = self.load_contacts()
        interactions = self.load_interactions()

        # Filter this week's interactions
        week_interactions = []
        for interaction in interactions:
            try:
                int_date = datetime.strptime(interaction['date'].split()[0], '%Y-%m-%d')
                if week_start <= int_date < week_end:
                    week_interactions.append(interaction)
            except:
                pass

        # Generate report
        report = self.build_weekly_report_markdown(
            week_start, contacts, week_interactions
        )

        # Save report
        report_file = self.reports_dir / f"week_{week_start.strftime('%Y%m%d')}.md"
        report_file.write_text(report)

        print(f"✓ Weekly report generated: {report_file}")
        print(f"\n{report}\n")

    def build_weekly_report_markdown(self, week_start, contacts, interactions):
        """Build weekly report in markdown format"""
        week_str = week_start.strftime('%Y-%m-%d')

        # Calculate metrics
        emails_sent = sum(1 for i in interactions if i['type'] == 'email_sent')
        meetings = sum(1 for i in interactions if i['type'] == 'meeting')
        calls = sum(1 for i in interactions if i['type'] == 'call')

        # Pipeline stats
        status_counts = Counter(c['status'] for c in contacts)
        active = sum(1 for c in contacts if c['status'] in [
            'Warm Intro Requested', 'Warm Intro Received', 'Initial Outreach Sent',
            'Meeting Scheduled', 'Active Conversation'
        ])

        # Top priorities
        active_contacts = [c for c in contacts if c['status'] not in
                          ['Committed/Closed', 'Not Interested']]
        top_contacts = sorted(
            active_contacts,
            key=lambda c: (-float(c.get('priority_score', 50)), int(c.get('tier', 4)))
        )[:10]

        report = f"""# NEWCO Weekly Report
## Week of {week_str}

### Activity Summary
- **Emails Sent:** {emails_sent}
- **Meetings:** {meetings}
- **Calls:** {calls}
- **Total Interactions:** {len(interactions)}

### Pipeline Overview
- **Active Conversations:** {active}
- **Meeting Scheduled:** {status_counts.get('Meeting Scheduled', 0)}
- **Meeting Completed:** {status_counts.get('Meeting Completed', 0)}
- **Committed/Closed:** {status_counts.get('Committed/Closed', 0)}

### Top 10 Priorities for Next Week
"""

        for i, contact in enumerate(top_contacts, 1):
            report += f"{i}. **{contact['name']}** ({contact['company']}) - Tier {contact['tier']}\n"
            report += f"   - Status: {contact['status']}\n"
            report += f"   - Next Action: {contact['next_action']}\n"
            if contact['next_action_date']:
                report += f"   - Due: {contact['next_action_date']}\n"
            report += "\n"

        report += """
### Key Highlights
- [Add key wins, breakthroughs, or notable progress]

### Challenges
- [Add any blockers or challenges]

### Next Week Focus
- [Add priorities for next week]

---
*Generated automatically by NEWCO GTM System*
"""

        return report

    def show_dashboard(self):
        """Display CLI dashboard"""
        contacts = self.load_contacts()
        interactions = self.load_interactions()

        # Calculate current week number (simple calculation)
        start_date = datetime(2026, 1, 1)
        today = datetime.now()
        current_week = ((today - start_date).days // 7) + 1

        # Get this week's interactions
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=7)
        week_interactions = []
        for interaction in interactions:
            try:
                int_date = datetime.strptime(interaction['date'].split()[0], '%Y-%m-%d')
                if week_start <= int_date < week_end:
                    week_interactions.append(interaction)
            except:
                pass

        # Calculate metrics
        emails_sent = sum(1 for i in week_interactions if i['type'] == 'email_sent')
        meetings = sum(1 for i in week_interactions if i['type'] == 'meeting')

        status_counts = Counter(c['status'] for c in contacts)
        platform_convos = sum(1 for c in contacts if
                            c['category'] == 'Platform Gatekeeper' and
                            c['status'] in ['Meeting Completed', 'Active Conversation'])
        lp_commits = status_counts.get('Committed/Closed', 0)

        # Top priorities
        top_contacts = sorted(
            [c for c in contacts if c['status'] not in ['Committed/Closed', 'Not Interested']],
            key=lambda c: (-float(c.get('priority_score', 50)), int(c.get('tier', 4)))
        )[:5]

        # Overdue actions
        overdue = []
        for contact in contacts:
            if contact['next_action_date']:
                try:
                    due_date = datetime.strptime(contact['next_action_date'], '%Y-%m-%d')
                    if due_date < today:
                        overdue.append(contact)
                except:
                    pass

        # Print dashboard
        print("\n┌─── NEWCO GTM Dashboard " + "─" * 36 + "┐")
        print(f"│ Week {current_week} of 12" + " " * 48 + "│")
        print("│" + " " * 61 + "│")
        print("│ Pipeline:" + " " * 52 + "│")
        print(f"│ ├─ Platform Convos: {platform_convos}/4" + " " * (49 - len(str(platform_convos))) + "│")
        print(f"│ ├─ Active Conversations: {status_counts.get('Active Conversation', 0)}" +
              " " * (42 - len(str(status_counts.get('Active Conversation', 0)))) + "│")
        print(f"│ ├─ Meetings Scheduled: {status_counts.get('Meeting Scheduled', 0)}" +
              " " * (44 - len(str(status_counts.get('Meeting Scheduled', 0)))) + "│")
        print(f"│ └─ Soft Commits: {lp_commits}/2" + " " * (47 - len(str(lp_commits))) + "│")
        print("│" + " " * 61 + "│")
        print("│ This Week:" + " " * 51 + "│")
        print(f"│ ├─ Meetings: {meetings}" + " " * (49 - len(str(meetings))) + "│")
        print(f"│ ├─ Emails Sent: {emails_sent}" + " " * (45 - len(str(emails_sent))) + "│")
        print(f"│ ├─ Total Interactions: {len(week_interactions)}" +
              " " * (39 - len(str(len(week_interactions)))) + "│")
        print(f"│ └─ Overdue Actions: {len(overdue)}" + " " * (44 - len(str(len(overdue)))) + "│")
        print("│" + " " * 61 + "│")
        print("│ Top Priorities:" + " " * 46 + "│")

        for i, contact in enumerate(top_contacts, 1):
            name_company = f"{contact['name']} (T{contact['tier']})"
            if len(name_company) > 55:
                name_company = name_company[:52] + "..."
            spaces = 60 - len(str(i)) - len(name_company) - 3
            print(f"│ {i}. {name_company}" + " " * spaces + "│")

        print("└" + "─" * 61 + "┘\n")

    def export_data(self):
        """Export data to various formats"""
        contacts = self.load_contacts()
        interactions = self.load_interactions()

        # Export to JSON
        import json

        export_dir = REPORTS_DIR / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Export contacts
        contacts_file = export_dir / f"contacts_{timestamp}.json"
        with open(contacts_file, 'w') as f:
            json.dump(contacts, f, indent=2)

        # Export interactions
        interactions_file = export_dir / f"interactions_{timestamp}.json"
        with open(interactions_file, 'w') as f:
            json.dump(interactions, f, indent=2)

        print(f"✓ Data exported:")
        print(f"  - {contacts_file}")
        print(f"  - {interactions_file}")

    def get_contact_by_id(self, contact_id):
        """Get contact by ID"""
        contacts = self.load_contacts()
        for contact in contacts:
            if contact['id'] == str(contact_id):
                return contact
        return None


if __name__ == '__main__':
    # Test
    rg = ReportGenerator()
    rg.show_dashboard()

"""
Pipeline Tracking and Analytics
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


class PipelineManager:
    """Manage pipeline tracking and analytics"""

    def __init__(self):
        self.contacts_file = DATA_DIR / "contacts.csv"
        self.interactions_file = DATA_DIR / "interactions.csv"
        self.pipeline_file = DATA_DIR / "pipeline.csv"

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

    def get_pipeline_stats(self):
        """Get current pipeline statistics"""
        contacts = self.load_contacts()

        stats = {
            'total_contacts': len(contacts),
            'by_status': Counter(c['status'] for c in contacts),
            'by_tier': Counter(c['tier'] for c in contacts),
            'by_category': Counter(c['category'] for c in contacts)
        }

        return stats

    def get_weekly_stats(self, week_start=None):
        """Get stats for a specific week"""
        if week_start is None:
            # Use current week
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())

        week_end = week_start + timedelta(days=7)

        interactions = self.load_interactions()

        # Filter interactions for this week
        week_interactions = []
        for interaction in interactions:
            int_date = datetime.strptime(interaction['date'].split()[0], '%Y-%m-%d')
            if week_start <= int_date < week_end:
                week_interactions.append(interaction)

        stats = {
            'week_start': week_start.strftime('%Y-%m-%d'),
            'total_interactions': len(week_interactions),
            'emails_sent': sum(1 for i in week_interactions if i['type'] == 'email_sent'),
            'emails_received': sum(1 for i in week_interactions if i['type'] == 'email_received'),
            'meetings': sum(1 for i in week_interactions if i['type'] == 'meeting'),
            'calls': sum(1 for i in week_interactions if i['type'] == 'call')
        }

        return stats

    def show_overview(self):
        """Display pipeline overview"""
        stats = self.get_pipeline_stats()

        print("\n" + "="*60)
        print("NEWCO PIPELINE OVERVIEW")
        print("="*60)
        print(f"Total Contacts: {stats['total_contacts']}")
        print("\nBy Status:")
        for status, count in sorted(stats['by_status'].items(), key=lambda x: -x[1]):
            print(f"  {status:<25} {count:>3}")

        print("\nBy Tier:")
        for tier, count in sorted(stats['by_tier'].items()):
            print(f"  Tier {tier:<20} {count:>3}")

        print("\nBy Category:")
        for category, count in sorted(stats['by_category'].items(), key=lambda x: -x[1]):
            print(f"  {category:<25} {count:>3}")

        print("="*60 + "\n")

    def show_weekly(self):
        """Display this week's metrics"""
        stats = self.get_weekly_stats()

        print("\n" + "="*60)
        print(f"WEEK OF {stats['week_start']}")
        print("="*60)
        print(f"Total Interactions:   {stats['total_interactions']}")
        print(f"Emails Sent:          {stats['emails_sent']}")
        print(f"Emails Received:      {stats['emails_received']}")
        print(f"Meetings:             {stats['meetings']}")
        print(f"Calls:                {stats['calls']}")
        print("="*60 + "\n")

    def generate_report(self, week_number=None):
        """Generate detailed pipeline report"""
        if week_number:
            # Calculate week start based on week number
            # Assuming week 1 starts on a specific date
            base_date = datetime(2026, 1, 1)  # Adjust as needed
            week_start = base_date + timedelta(weeks=week_number-1)
            stats = self.get_weekly_stats(week_start)
        else:
            stats = self.get_weekly_stats()

        print(f"\nPipeline Report - Week of {stats['week_start']}")
        print("-" * 60)
        print(f"Emails Sent:      {stats['emails_sent']}")
        print(f"Meetings:         {stats['meetings']}")
        print(f"Calls:            {stats['calls']}")
        print("-" * 60 + "\n")

    def calculate_conversion_rate(self, from_status, to_status):
        """Calculate conversion rate between two statuses"""
        contacts = self.load_contacts()

        from_count = sum(1 for c in contacts if c['status'] == from_status)
        to_count = sum(1 for c in contacts if c['status'] == to_status)

        if from_count == 0:
            return 0.0

        return (to_count / from_count) * 100

    def get_funnel_metrics(self):
        """Get full funnel conversion metrics"""
        contacts = self.load_contacts()

        funnel_stages = [
            'Cold',
            'Warm Intro Requested',
            'Initial Outreach Sent',
            'Meeting Scheduled',
            'Meeting Completed',
            'Active Conversation',
            'Committed/Closed'
        ]

        metrics = {}
        for stage in funnel_stages:
            count = sum(1 for c in contacts if c['status'] == stage)
            metrics[stage] = count

        return metrics


if __name__ == '__main__':
    # Test
    pm = PipelineManager()
    pm.show_overview()
    pm.show_weekly()

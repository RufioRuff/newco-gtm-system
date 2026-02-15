"""
Automation and Workflow Engine
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
import yaml

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"


class AutomationEngine:
    """Automate workflows and task generation"""

    def __init__(self):
        self.contacts_file = DATA_DIR / "contacts.csv"
        self.config = self.load_config()

    def load_config(self):
        """Load configuration"""
        config_file = CONFIG_DIR / "config.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def load_contacts(self):
        """Load all contacts"""
        contacts = []
        if self.contacts_file.exists():
            with open(self.contacts_file, 'r') as f:
                reader = csv.DictReader(f)
                contacts = list(reader)
        return contacts

    def get_tasks_today(self):
        """Get tasks due today"""
        contacts = self.load_contacts()
        today = datetime.now().strftime('%Y-%m-%d')

        tasks = []
        for contact in contacts:
            if contact['next_action_date'] == today and contact['next_action']:
                tasks.append({
                    'contact_id': contact['id'],
                    'contact_name': contact['name'],
                    'action': contact['next_action'],
                    'date': contact['next_action_date']
                })

        return tasks

    def get_tasks_week(self):
        """Get tasks due this week"""
        contacts = self.load_contacts()
        today = datetime.now()
        week_end = today + timedelta(days=7)

        tasks = []
        for contact in contacts:
            if contact['next_action_date'] and contact['next_action']:
                try:
                    due_date = datetime.strptime(contact['next_action_date'], '%Y-%m-%d')
                    if today <= due_date <= week_end:
                        tasks.append({
                            'contact_id': contact['id'],
                            'contact_name': contact['name'],
                            'action': contact['next_action'],
                            'date': contact['next_action_date']
                        })
                except ValueError:
                    pass

        return sorted(tasks, key=lambda x: x['date'])

    def get_overdue_tasks(self):
        """Get overdue tasks"""
        contacts = self.load_contacts()
        today = datetime.now()

        tasks = []
        for contact in contacts:
            if contact['next_action_date'] and contact['next_action']:
                try:
                    due_date = datetime.strptime(contact['next_action_date'], '%Y-%m-%d')
                    if due_date < today:
                        tasks.append({
                            'contact_id': contact['id'],
                            'contact_name': contact['name'],
                            'action': contact['next_action'],
                            'date': contact['next_action_date'],
                            'days_overdue': (today - due_date).days
                        })
                except ValueError:
                    pass

        return sorted(tasks, key=lambda x: x['days_overdue'], reverse=True)

    def identify_stale_contacts(self):
        """Identify contacts that haven't been contacted recently"""
        contacts = self.load_contacts()
        today = datetime.now()
        stale_threshold = self.config.get('automation', {}).get('stale_threshold_days', 14)

        stale = []
        for contact in contacts:
            # Skip closed or not interested
            if contact['status'] in ['Committed/Closed', 'Not Interested', 'Cold']:
                continue

            if contact['last_contact']:
                try:
                    last_contact = datetime.strptime(contact['last_contact'], '%Y-%m-%d')
                    days_since = (today - last_contact).days
                    if days_since >= stale_threshold:
                        stale.append({
                            'contact': contact,
                            'days_since_contact': days_since
                        })
                except ValueError:
                    pass

        return sorted(stale, key=lambda x: x['days_since_contact'], reverse=True)

    def suggest_follow_ups(self):
        """Suggest follow-up actions for contacts"""
        contacts = self.load_contacts()
        suggestions = []

        for contact in contacts:
            suggestion = self.determine_next_action(contact)
            if suggestion:
                suggestions.append({
                    'contact_id': contact['id'],
                    'contact_name': contact['name'],
                    'current_status': contact['status'],
                    'suggested_action': suggestion['action'],
                    'suggested_date': suggestion['date'],
                    'reason': suggestion['reason']
                })

        return suggestions

    def determine_next_action(self, contact):
        """Determine appropriate next action based on contact status"""
        status = contact['status']
        follow_up_days = self.config.get('automation', {}).get('follow_up_days', 7)

        actions = {
            'Cold': {
                'action': 'Research contact and prepare personalized email',
                'days': 0,
                'reason': 'Initial outreach needed'
            },
            'Warm Intro Requested': {
                'action': 'Follow up on warm intro request',
                'days': follow_up_days,
                'reason': 'Check on intro status'
            },
            'Initial Outreach Sent': {
                'action': 'Send follow-up email',
                'days': follow_up_days,
                'reason': 'No response to initial outreach'
            },
            'Meeting Scheduled': {
                'action': 'Prepare for meeting',
                'days': 1,
                'reason': 'Meeting preparation'
            },
            'Meeting Completed': {
                'action': 'Send follow-up email with next steps',
                'days': 1,
                'reason': 'Post-meeting follow-up'
            },
            'Active Conversation': {
                'action': 'Continue conversation or schedule next meeting',
                'days': follow_up_days,
                'reason': 'Maintain momentum'
            }
        }

        if status in actions:
            action_plan = actions[status]
            today = datetime.now()
            suggested_date = today + timedelta(days=action_plan['days'])

            return {
                'action': action_plan['action'],
                'date': suggested_date.strftime('%Y-%m-%d'),
                'reason': action_plan['reason']
            }

        return None

    def calculate_priority_score(self, contact):
        """Calculate priority score for a contact"""
        score = 50  # Base score

        # Tier weight (40 points max)
        tier = int(contact.get('tier', 4))
        tier_score = {0: 40, 1: 35, 2: 30, 3: 25, 4: 20}
        score += tier_score.get(tier, 20)

        # Recency weight (30 points max)
        if contact['last_contact']:
            try:
                last_contact = datetime.strptime(contact['last_contact'], '%Y-%m-%d')
                days_since = (datetime.now() - last_contact).days
                if days_since <= 7:
                    score += 30
                elif days_since <= 14:
                    score += 20
                elif days_since <= 30:
                    score += 10
            except ValueError:
                pass

        # Status weight
        status_scores = {
            'Active Conversation': 20,
            'Meeting Scheduled': 18,
            'Meeting Completed': 15,
            'Warm Intro Received': 12,
            'Initial Outreach Sent': 10,
            'Warm Intro Requested': 8,
            'Cold': 5
        }
        score += status_scores.get(contact['status'], 5)

        return min(score, 100)  # Cap at 100

    def recalculate_priorities(self):
        """Recalculate priority scores for all contacts"""
        contacts = self.load_contacts()

        for contact in contacts:
            contact['priority_score'] = str(self.calculate_priority_score(contact))

        # Save updated contacts
        if contacts:
            fieldnames = contacts[0].keys()
            with open(self.contacts_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(contacts)

        print(f"✓ Recalculated priorities for {len(contacts)} contacts")

    def generate_weekly_tasks(self, week_number):
        """Generate tasks for a specific week based on 90-day plan"""
        # This would be customized based on the specific 90-day plan
        # For now, returns a template

        tasks = []

        if week_number <= 2:
            tasks = [
                "Request warm intros from key connectors",
                "Research and personalize emails for Tier 0-1 contacts",
                "Schedule platform gatekeeper meetings"
            ]
        elif week_number <= 4:
            tasks = [
                "Send 15-20 meeting requests",
                "Follow up on pending intros",
                "Prepare pitch materials"
            ]
        elif week_number <= 8:
            tasks = [
                "Conduct 3-4 meetings per week",
                "Send follow-up emails within 24 hours",
                "Request LP introductions from VC partners"
            ]
        else:
            tasks = [
                "Schedule second meetings with warm leads",
                "Draft commitment letters",
                "Close first LP commitments"
            ]

        return tasks


if __name__ == '__main__':
    # Test
    ae = AutomationEngine()
    tasks = ae.get_tasks_week()
    print(f"Tasks this week: {len(tasks)}")
    for task in tasks:
        print(f"- {task['contact_name']}: {task['action']}")

#!/usr/bin/env python3
"""
Advanced Analytics and Insights Engine
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import json

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


class AnalyticsEngine:
    """Advanced analytics and insights"""

    def __init__(self):
        self.contacts_file = DATA_DIR / "contacts.csv"
        self.interactions_file = DATA_DIR / "interactions.csv"

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

    def calculate_response_rate(self):
        """Calculate email response rate"""
        interactions = self.load_interactions()

        emails_sent = [i for i in interactions if i['type'] == 'email_sent']
        emails_received = [i for i in interactions if i['type'] == 'email_received']

        # Group by contact to find responses
        contact_emails = defaultdict(lambda: {'sent': 0, 'received': 0})

        for interaction in emails_sent:
            contact_emails[interaction['contact_id']]['sent'] += 1

        for interaction in emails_received:
            contact_emails[interaction['contact_id']]['received'] += 1

        # Calculate response rate
        total_sent = sum(c['sent'] for c in contact_emails.values())
        contacts_responded = sum(1 for c in contact_emails.values() if c['received'] > 0)

        response_rate = (contacts_responded / len(contact_emails) * 100) if contact_emails else 0

        return {
            'total_emails_sent': total_sent,
            'total_contacts_emailed': len(contact_emails),
            'contacts_responded': contacts_responded,
            'response_rate': response_rate
        }

    def calculate_conversion_funnel(self):
        """Calculate full conversion funnel metrics"""
        contacts = self.load_contacts()

        funnel = {
            'total': len(contacts),
            'cold': 0,
            'outreach_sent': 0,
            'responded': 0,
            'meeting_scheduled': 0,
            'meeting_completed': 0,
            'active_conversation': 0,
            'committed': 0
        }

        for contact in contacts:
            status = contact['status']

            if status == 'Cold':
                funnel['cold'] += 1
            elif status in ['Warm Intro Requested', 'Warm Intro Received', 'Initial Outreach Sent']:
                funnel['outreach_sent'] += 1
            elif status == 'Meeting Scheduled':
                funnel['meeting_scheduled'] += 1
            elif status == 'Meeting Completed':
                funnel['meeting_completed'] += 1
            elif status == 'Active Conversation':
                funnel['active_conversation'] += 1
            elif status == 'Committed/Closed':
                funnel['committed'] += 1

        # Calculate conversion rates
        if funnel['total'] > 0:
            funnel['outreach_rate'] = (funnel['outreach_sent'] / funnel['total']) * 100
            funnel['meeting_rate'] = (funnel['meeting_scheduled'] / funnel['total']) * 100
            funnel['close_rate'] = (funnel['committed'] / funnel['total']) * 100

        return funnel

    def analyze_by_tier(self):
        """Analyze performance by tier"""
        contacts = self.load_contacts()
        interactions = self.load_interactions()

        tier_stats = defaultdict(lambda: {
            'total': 0,
            'cold': 0,
            'active': 0,
            'meetings': 0,
            'committed': 0,
            'interactions': 0
        })

        # Count contacts by tier
        for contact in contacts:
            tier = contact['tier']
            tier_stats[tier]['total'] += 1

            if contact['status'] == 'Cold':
                tier_stats[tier]['cold'] += 1
            elif contact['status'] in ['Active Conversation', 'Meeting Scheduled', 'Meeting Completed']:
                tier_stats[tier]['active'] += 1
            elif contact['status'] == 'Committed/Closed':
                tier_stats[tier]['committed'] += 1

            if contact['status'] in ['Meeting Scheduled', 'Meeting Completed']:
                tier_stats[tier]['meetings'] += 1

        # Count interactions by tier
        for interaction in interactions:
            contact_id = interaction['contact_id']
            contact = next((c for c in contacts if c['id'] == contact_id), None)
            if contact:
                tier_stats[contact['tier']]['interactions'] += 1

        return dict(tier_stats)

    def analyze_by_category(self):
        """Analyze performance by category"""
        contacts = self.load_contacts()

        category_stats = defaultdict(lambda: {
            'total': 0,
            'cold': 0,
            'active': 0,
            'meetings': 0,
            'committed': 0
        })

        for contact in contacts:
            cat = contact['category']
            category_stats[cat]['total'] += 1

            if contact['status'] == 'Cold':
                category_stats[cat]['cold'] += 1
            elif contact['status'] in ['Active Conversation', 'Meeting Scheduled', 'Meeting Completed']:
                category_stats[cat]['active'] += 1
            elif contact['status'] == 'Committed/Closed':
                category_stats[cat]['committed'] += 1

            if contact['status'] in ['Meeting Scheduled', 'Meeting Completed']:
                category_stats[cat]['meetings'] += 1

        return dict(category_stats)

    def calculate_velocity_metrics(self):
        """Calculate velocity (how fast contacts move through pipeline)"""
        contacts = self.load_contacts()
        interactions = self.load_interactions()

        # Group interactions by contact
        contact_interactions = defaultdict(list)
        for interaction in interactions:
            contact_interactions[interaction['contact_id']].append(interaction)

        velocities = []

        for contact in contacts:
            contact_id = contact['id']
            if contact_id in contact_interactions:
                ints = sorted(contact_interactions[contact_id],
                            key=lambda x: x['date'])

                if len(ints) >= 2:
                    first = datetime.strptime(ints[0]['date'].split()[0], '%Y-%m-%d')
                    last = datetime.strptime(ints[-1]['date'].split()[0], '%Y-%m-%d')
                    days = (last - first).days

                    velocities.append({
                        'contact_id': contact_id,
                        'contact_name': contact['name'],
                        'days': days,
                        'interactions': len(ints),
                        'status': contact['status']
                    })

        if velocities:
            avg_days = sum(v['days'] for v in velocities) / len(velocities)
            avg_interactions = sum(v['interactions'] for v in velocities) / len(velocities)
        else:
            avg_days = 0
            avg_interactions = 0

        return {
            'average_days_to_current_stage': avg_days,
            'average_interactions_per_contact': avg_interactions,
            'contacts_analyzed': len(velocities)
        }

    def identify_stalled_contacts(self, days_threshold=14):
        """Identify contacts that have stalled"""
        contacts = self.load_contacts()
        interactions = self.load_interactions()

        # Get last interaction date for each contact
        contact_last_interaction = {}
        for interaction in interactions:
            contact_id = interaction['contact_id']
            try:
                date = datetime.strptime(interaction['date'].split()[0], '%Y-%m-%d')
                if contact_id not in contact_last_interaction or date > contact_last_interaction[contact_id]:
                    contact_last_interaction[contact_id] = date
            except:
                pass

        stalled = []
        today = datetime.now()

        for contact in contacts:
            # Skip if already closed or not interested
            if contact['status'] in ['Committed/Closed', 'Not Interested', 'Cold']:
                continue

            contact_id = contact['id']
            if contact_id in contact_last_interaction:
                last_date = contact_last_interaction[contact_id]
                days_since = (today - last_date).days

                if days_since >= days_threshold:
                    stalled.append({
                        'contact_id': contact_id,
                        'name': contact['name'],
                        'company': contact['company'],
                        'status': contact['status'],
                        'days_since_last_interaction': days_since,
                        'last_interaction': last_date.strftime('%Y-%m-%d')
                    })

        return sorted(stalled, key=lambda x: x['days_since_last_interaction'], reverse=True)

    def calculate_success_probability(self, contact):
        """Calculate probability of success for a contact"""
        score = 50  # Base probability

        # Tier influence
        tier_scores = {0: 30, 1: 25, 2: 20, 3: 15, 4: 10}
        score += tier_scores.get(int(contact.get('tier', 4)), 10)

        # Status influence
        status_scores = {
            'Active Conversation': 25,
            'Meeting Completed': 20,
            'Meeting Scheduled': 15,
            'Warm Intro Received': 12,
            'Initial Outreach Sent': 8,
            'Warm Intro Requested': 6,
            'Cold': 0
        }
        score += status_scores.get(contact['status'], 0)

        # Recency influence
        if contact['last_contact']:
            try:
                last_contact = datetime.strptime(contact['last_contact'], '%Y-%m-%d')
                days_since = (datetime.now() - last_contact).days

                if days_since <= 7:
                    score += 15
                elif days_since <= 14:
                    score += 10
                elif days_since <= 30:
                    score += 5
                else:
                    score -= 5  # Penalty for stale
            except:
                pass

        return min(score, 100)  # Cap at 100

    def predict_week_12_outcomes(self):
        """Predict outcomes by week 12 based on current trajectory"""
        contacts = self.load_contacts()
        interactions = self.load_interactions()

        predictions = {
            'total_meetings_projected': 0,
            'total_commits_projected': 0,
            'high_probability_contacts': [],
            'at_risk_contacts': []
        }

        for contact in contacts:
            if contact['status'] in ['Committed/Closed', 'Not Interested']:
                continue

            prob = self.calculate_success_probability(contact)

            if contact['status'] in ['Meeting Scheduled', 'Meeting Completed']:
                predictions['total_meetings_projected'] += 1

            if prob >= 70:
                predictions['total_commits_projected'] += 1
                predictions['high_probability_contacts'].append({
                    'name': contact['name'],
                    'company': contact['company'],
                    'probability': prob
                })
            elif prob < 30 and contact['status'] not in ['Cold']:
                predictions['at_risk_contacts'].append({
                    'name': contact['name'],
                    'company': contact['company'],
                    'probability': prob,
                    'status': contact['status']
                })

        return predictions

    def generate_insights(self):
        """Generate actionable insights"""
        insights = []

        # Response rate insight
        response_data = self.calculate_response_rate()
        if response_data['response_rate'] < 30:
            insights.append({
                'type': 'warning',
                'title': 'Low Response Rate',
                'message': f"Response rate is {response_data['response_rate']:.1f}%. Consider personalizing emails more or testing different subject lines.",
                'metric': response_data['response_rate']
            })
        elif response_data['response_rate'] > 50:
            insights.append({
                'type': 'success',
                'title': 'Strong Response Rate',
                'message': f"Excellent response rate of {response_data['response_rate']:.1f}%. Keep using current approach!",
                'metric': response_data['response_rate']
            })

        # Stalled contacts
        stalled = self.identify_stalled_contacts()
        if len(stalled) > 5:
            insights.append({
                'type': 'action',
                'title': 'Stalled Contacts',
                'message': f"{len(stalled)} contacts haven't been contacted in 14+ days. Time for re-engagement campaign.",
                'metric': len(stalled)
            })

        # Tier performance
        tier_stats = self.analyze_by_tier()
        if '0' in tier_stats:
            tier0 = tier_stats['0']
            if tier0['cold'] > 0:
                insights.append({
                    'type': 'urgent',
                    'title': 'Tier 0 Contacts Not Activated',
                    'message': f"{tier0['cold']} Tier 0 (Network Multipliers) are still cold. These are your highest priority!",
                    'metric': tier0['cold']
                })

        # Velocity insight
        velocity = self.calculate_velocity_metrics()
        if velocity['average_days_to_current_stage'] > 21:
            insights.append({
                'type': 'warning',
                'title': 'Slow Pipeline Velocity',
                'message': f"Average {velocity['average_days_to_current_stage']:.0f} days per stage. Consider more frequent follow-ups.",
                'metric': velocity['average_days_to_current_stage']
            })

        return insights

    def show_insights_report(self):
        """Display insights report"""
        print("\n" + "="*70)
        print("INSIGHTS & RECOMMENDATIONS")
        print("="*70)

        insights = self.generate_insights()

        if not insights:
            print("\n✓ No issues detected. Keep up the good work!\n")
            return

        for insight in insights:
            icon = {
                'success': '✓',
                'warning': '⚠',
                'action': '→',
                'urgent': '!'
            }.get(insight['type'], '•')

            print(f"\n{icon} {insight['title']}")
            print(f"  {insight['message']}")
            if 'metric' in insight:
                print(f"  Metric: {insight['metric']}")

        print("\n" + "="*70 + "\n")

    def show_advanced_analytics(self):
        """Show comprehensive analytics dashboard"""
        print("\n" + "="*70)
        print("ADVANCED ANALYTICS DASHBOARD")
        print("="*70)

        # Response rate
        response = self.calculate_response_rate()
        print(f"\n📧 Email Performance")
        print(f"  Total Sent: {response['total_emails_sent']}")
        print(f"  Contacts Emailed: {response['total_contacts_emailed']}")
        print(f"  Responded: {response['contacts_responded']}")
        print(f"  Response Rate: {response['response_rate']:.1f}%")

        # Conversion funnel
        funnel = self.calculate_conversion_funnel()
        print(f"\n📊 Conversion Funnel")
        print(f"  Total Contacts: {funnel['total']}")
        print(f"  Cold: {funnel['cold']}")
        print(f"  Outreach Sent: {funnel['outreach_sent']} ({funnel.get('outreach_rate', 0):.1f}%)")
        print(f"  Meetings: {funnel['meeting_scheduled']} ({funnel.get('meeting_rate', 0):.1f}%)")
        print(f"  Active Conversations: {funnel['active_conversation']}")
        print(f"  Committed: {funnel['committed']} ({funnel.get('close_rate', 0):.1f}%)")

        # Tier performance
        tier_stats = self.analyze_by_tier()
        print(f"\n🎯 Performance by Tier")
        for tier in sorted(tier_stats.keys()):
            stats = tier_stats[tier]
            print(f"  Tier {tier}: {stats['total']} total | {stats['active']} active | {stats['meetings']} meetings | {stats['committed']} committed")

        # Velocity
        velocity = self.calculate_velocity_metrics()
        print(f"\n⚡ Pipeline Velocity")
        print(f"  Avg Days to Current Stage: {velocity['average_days_to_current_stage']:.1f}")
        print(f"  Avg Interactions per Contact: {velocity['average_interactions_per_contact']:.1f}")

        # Predictions
        predictions = self.predict_week_12_outcomes()
        print(f"\n🔮 Week 12 Projections")
        print(f"  Projected Meetings: {predictions['total_meetings_projected']}")
        print(f"  Projected Commits: {predictions['total_commits_projected']}")
        print(f"  High Probability Contacts: {len(predictions['high_probability_contacts'])}")

        print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    analytics = AnalyticsEngine()
    analytics.show_advanced_analytics()
    analytics.show_insights_report()

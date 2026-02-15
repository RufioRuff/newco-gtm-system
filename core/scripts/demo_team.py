#!/usr/bin/env python3
"""
Demo Team Management Data

Creates sample team members, workload, and IC votes
"""

from team_management import TeamManager
from datetime import datetime, timedelta

def create_demo_team_data():
    """Create sample team management data"""
    team = TeamManager()

    print("Creating demo team management data...\n")

    # Team members
    print("👥 Adding team members...")

    members_data = [
        {
            'name': 'Ken Wallace',
            'title': 'CEO',
            'role': 'Leadership',
            'hire_date': '2023-01-01',
            'email': 'ken@newco.com'
        },
        {
            'name': 'Sarah Chen',
            'title': 'Senior Analyst',
            'role': 'Analyst',
            'hire_date': '2023-06-01',
            'email': 'sarah@newco.com'
        },
        {
            'name': 'Marcus Rodriguez',
            'title': 'Analyst',
            'role': 'Analyst',
            'hire_date': '2024-01-15',
            'email': 'marcus@newco.com'
        },
        {
            'name': 'Emily Park',
            'title': 'Associate',
            'role': 'Analyst',
            'hire_date': '2024-09-01',
            'email': 'emily@newco.com'
        }
    ]

    member_ids = {}
    for member_data in members_data:
        member_id = team.add_team_member(**member_data)
        member_ids[member_data['name']] = member_id

    # Workload assignments
    print("\n📋 Assigning workload...")

    workload_data = [
        {
            'member': 'Sarah Chen',
            'task_type': 'Due Diligence',
            'description': 'Kindred Ventures Fund III - Deep DD',
            'related_id': 'M003',
            'hours_estimated': 80,
            'due_date': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        },
        {
            'member': 'Sarah Chen',
            'task_type': 'IC Memo',
            'description': 'Draft IC memo for Kindred Ventures',
            'related_id': 'M003',
            'hours_estimated': 20,
            'due_date': (datetime.now() + timedelta(days=21)).strftime('%Y-%m-%d')
        },
        {
            'member': 'Marcus Rodriguez',
            'task_type': 'Reference Checks',
            'description': 'LP reference calls for Underscore VC',
            'related_id': 'M008',
            'hours_estimated': 10,
            'due_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        },
        {
            'member': 'Marcus Rodriguez',
            'task_type': 'Portfolio Review',
            'description': 'Review Q4 portfolio company updates',
            'related_id': '',
            'hours_estimated': 15,
            'due_date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        },
        {
            'member': 'Emily Park',
            'task_type': 'Market Research',
            'description': 'Climate tech sector analysis',
            'related_id': '',
            'hours_estimated': 25,
            'due_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        },
        {
            'member': 'Emily Park',
            'task_type': 'Manager Sourcing',
            'description': 'Identify 10 new seed-stage managers',
            'related_id': '',
            'hours_estimated': 20,
            'due_date': (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d')
        }
    ]

    for work in workload_data:
        member_id = member_ids[work['member']]
        team.assign_work(
            member_id=member_id,
            task_type=work['task_type'],
            description=work['description'],
            related_id=work['related_id'],
            hours_estimated=work['hours_estimated'],
            due_date=work['due_date']
        )

    # IC voting history
    print("\n🗳️  Adding IC voting history...")

    ic_votes = [
        # Acme Ventures - Approved
        {
            'member': 'Ken Wallace',
            'manager_id': 'M001',
            'vote': 'Yes',
            'rationale': 'Strong track record, clear differentiation',
            'performance': 'Good - 1.20x TVPI'
        },
        {
            'member': 'Sarah Chen',
            'manager_id': 'M001',
            'vote': 'Yes',
            'rationale': 'Impressive portfolio construction',
            'performance': 'Good - 1.20x TVPI'
        },
        # Beta Capital - Approved
        {
            'member': 'Ken Wallace',
            'manager_id': 'M002',
            'vote': 'Yes',
            'rationale': 'Established firm, good vintage timing',
            'performance': 'Good - 1.50x TVPI'
        },
        {
            'member': 'Sarah Chen',
            'manager_id': 'M002',
            'vote': 'Yes',
            'rationale': 'Consumer expertise is valuable',
            'performance': 'Good - 1.50x TVPI'
        },
        # Gamma Growth - Approved (Sarah abstained)
        {
            'member': 'Ken Wallace',
            'manager_id': 'M003',
            'vote': 'Yes',
            'rationale': 'Growth stage diversification needed',
            'performance': 'Good - 1.20x TVPI'
        },
        {
            'member': 'Sarah Chen',
            'manager_id': 'M003',
            'vote': 'Abstain',
            'rationale': 'Need more data on fintech exposure',
            'performance': 'Good - 1.20x TVPI'
        },
        # Delta Seed - Approved
        {
            'member': 'Ken Wallace',
            'manager_id': 'M004',
            'vote': 'Yes',
            'rationale': 'AI/ML thesis compelling',
            'performance': ''  # Too early
        },
        {
            'member': 'Sarah Chen',
            'manager_id': 'M004',
            'vote': 'Yes',
            'rationale': 'Strong GP backgrounds in AI',
            'performance': ''
        },
        # Epsilon Ventures - Approved
        {
            'member': 'Ken Wallace',
            'manager_id': 'M005',
            'vote': 'Yes',
            'rationale': 'Healthcare is underweight in portfolio',
            'performance': 'Good - 1.67x TVPI'
        },
        {
            'member': 'Sarah Chen',
            'manager_id': 'M005',
            'vote': 'Yes',
            'rationale': 'Best fund in pipeline',
            'performance': 'Good - 1.67x TVPI'
        },
        {
            'member': 'Marcus Rodriguez',
            'manager_id': 'M005',
            'vote': 'Yes',
            'rationale': 'Excellent reference checks',
            'performance': 'Good - 1.67x TVPI'
        }
    ]

    ic_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')

    for vote in ic_votes:
        member_id = member_ids[vote['member']]
        vote_id = team.record_ic_vote(
            ic_date=ic_date,
            manager_id=vote['manager_id'],
            member_id=member_id,
            vote=vote['vote'],
            rationale=vote['rationale']
        )

        # Update with performance if available
        if vote['performance']:
            votes = team._load_csv(team.ic_votes_file)
            for v in votes:
                if v['vote_id'] == vote_id:
                    v['fund_performance'] = vote['performance']
                    v['outcome'] = 'Approved'
            team._save_csv(team.ic_votes_file, votes)

    print(f"✓ Added {len(ic_votes)} IC votes")

    # Professional development
    print("\n📚 Adding professional development...")

    dev_activities = [
        {
            'member': 'Sarah Chen',
            'activity_type': 'Training',
            'description': 'NVCA PE/VC Fundamentals Course',
            'hours': 20,
            'competency': 'VC Fundamentals'
        },
        {
            'member': 'Sarah Chen',
            'activity_type': 'Conference',
            'description': 'Attended Emerging Manager Summit',
            'hours': 16,
            'competency': 'Industry Knowledge'
        },
        {
            'member': 'Marcus Rodriguez',
            'activity_type': 'Training',
            'description': 'Financial Modeling for VC',
            'hours': 15,
            'competency': 'Financial Analysis'
        },
        {
            'member': 'Marcus Rodriguez',
            'activity_type': 'Mentorship',
            'description': 'Weekly sessions with Sarah Chen',
            'hours': 10,
            'competency': 'Due Diligence'
        },
        {
            'member': 'Emily Park',
            'activity_type': 'Onboarding',
            'description': 'NEWCO new hire training',
            'hours': 40,
            'competency': 'Company Knowledge'
        },
        {
            'member': 'Emily Park',
            'activity_type': 'Training',
            'description': 'Pitchbook platform training',
            'hours': 8,
            'competency': 'Research Tools'
        }
    ]

    for activity in dev_activities:
        member_id = member_ids[activity['member']]
        team.log_development_activity(
            member_id=member_id,
            activity_type=activity['activity_type'],
            description=activity['description'],
            hours=activity['hours'],
            competency=activity['competency']
        )

    print(f"\n✓ Created demo team management data")
    print(f"\nTry these commands:")
    print("  ./scripts/newco_cli.py team workload")
    print("  ./scripts/newco_cli.py team ic-votes")
    print("  ./scripts/newco_cli.py team development")
    print("  ./scripts/newco_cli.py team capacity")

if __name__ == '__main__':
    create_demo_team_data()

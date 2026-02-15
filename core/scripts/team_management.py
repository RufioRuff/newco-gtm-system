#!/usr/bin/env python3
"""
Team Management - Deal Team & Professional Development

Tracks team workload, performance, and development:
- Deal team workload (who's working on what)
- IC voting history and patterns
- Professional development tracking
- Performance metrics
- Capacity planning
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from manager_crm import ManagerCRM

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TEAM_DIR = DATA_DIR / "team"


class TeamManager:
    """Team management and development tracking"""

    def __init__(self):
        self.team_members_file = TEAM_DIR / "team_members.csv"
        self.workload_file = TEAM_DIR / "workload.csv"
        self.ic_votes_file = TEAM_DIR / "ic_votes.csv"
        self.development_file = TEAM_DIR / "development.csv"
        self.performance_file = TEAM_DIR / "performance_reviews.csv"
        self.manager_crm = ManagerCRM()
        self._initialize_files()

    def _initialize_files(self):
        """Initialize team management files"""
        TEAM_DIR.mkdir(parents=True, exist_ok=True)

        if not self.team_members_file.exists():
            self.team_members_file.write_text(
                "member_id,name,title,role,hire_date,email,status,notes\n"
            )

        if not self.workload_file.exists():
            self.workload_file.write_text(
                "workload_id,member_id,task_type,related_id,description,"
                "assigned_date,due_date,status,hours_estimated,hours_actual,notes\n"
            )

        if not self.ic_votes_file.exists():
            self.ic_votes_file.write_text(
                "vote_id,ic_date,manager_id,member_id,vote,rationale,"
                "outcome,fund_performance,notes\n"
            )

        if not self.development_file.exists():
            self.development_file.write_text(
                "dev_id,member_id,activity_type,activity_date,description,"
                "hours,competency,notes\n"
            )

        if not self.performance_file.exists():
            self.performance_file.write_text(
                "review_id,member_id,review_date,reviewer,period_start,period_end,"
                "rating,strengths,areas_for_improvement,goals,notes\n"
            )

    def add_team_member(self, name, title, role='Analyst', hire_date=None, email=''):
        """Add team member"""
        members = self._load_csv(self.team_members_file)

        member_id = f"TM{len(members) + 1:03d}"

        if hire_date is None:
            hire_date = datetime.now().strftime('%Y-%m-%d')

        member = {
            'member_id': member_id,
            'name': name,
            'title': title,
            'role': role,
            'hire_date': hire_date,
            'email': email,
            'status': 'Active',
            'notes': ''
        }

        members.append(member)
        self._save_csv(self.team_members_file, members)

        print(f"✓ Added team member: {name} ({member_id})")
        return member_id

    def assign_work(self, member_id, task_type, description, related_id='',
                   due_date=None, hours_estimated=0):
        """Assign work to team member"""
        workload = self._load_csv(self.workload_file)

        workload_id = f"WL{len(workload) + 1:05d}"

        if due_date is None:
            # Default to 2 weeks from now
            due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')

        work = {
            'workload_id': workload_id,
            'member_id': member_id,
            'task_type': task_type,
            'related_id': related_id,
            'description': description,
            'assigned_date': datetime.now().strftime('%Y-%m-%d'),
            'due_date': due_date,
            'status': 'Assigned',
            'hours_estimated': str(hours_estimated),
            'hours_actual': '0',
            'notes': ''
        }

        workload.append(work)
        self._save_csv(self.workload_file, workload)

        # Get member name
        members = self._load_csv(self.team_members_file)
        member = next((m for m in members if m['member_id'] == member_id), None)
        member_name = member['name'] if member else member_id

        print(f"✓ Assigned to {member_name}: {task_type} - {description}")
        return workload_id

    def update_work_status(self, workload_id, status, hours_actual=None, notes=''):
        """Update work item status"""
        workload = self._load_csv(self.workload_file)

        for work in workload:
            if work['workload_id'] == workload_id:
                work['status'] = status
                if hours_actual is not None:
                    work['hours_actual'] = str(hours_actual)
                if notes:
                    work['notes'] = notes

                self._save_csv(self.workload_file, workload)
                print(f"✓ Updated {workload_id}: {status}")
                return True

        print(f"Work item {workload_id} not found")
        return False

    def get_team_workload(self, member_id=None):
        """Get current workload"""
        workload = self._load_csv(self.workload_file)
        members = self._load_csv(self.team_members_file)

        # Filter by member if specified
        if member_id:
            workload = [w for w in workload if w['member_id'] == member_id]

        # Organize by member
        by_member = defaultdict(lambda: {
            'name': '',
            'total_tasks': 0,
            'active_tasks': 0,
            'hours_assigned': 0,
            'hours_worked': 0,
            'tasks': []
        })

        for work in workload:
            mid = work['member_id']
            member = next((m for m in members if m['member_id'] == mid), None)

            if member:
                by_member[mid]['name'] = member['name']
                by_member[mid]['total_tasks'] += 1

                if work['status'] in ['Assigned', 'In Progress']:
                    by_member[mid]['active_tasks'] += 1

                by_member[mid]['hours_assigned'] += float(work['hours_estimated']) if work['hours_estimated'] else 0
                by_member[mid]['hours_worked'] += float(work['hours_actual']) if work['hours_actual'] else 0
                by_member[mid]['tasks'].append(work)

        return dict(by_member)

    def show_team_workload(self, member_id=None):
        """Display team workload"""
        workload_data = self.get_team_workload(member_id)

        print("\n" + "="*80)
        print("TEAM WORKLOAD")
        print("="*80)

        if not workload_data:
            print("\nNo workload data available")
            print("\n" + "="*80 + "\n")
            return

        # Summary
        print(f"\n📊 Workload Summary")
        print(f"{'Team Member':<25} {'Active Tasks':<15} {'Total Tasks':<15} {'Hours (Est/Act)'}")
        print("-"*80)

        for mid, data in sorted(workload_data.items(), key=lambda x: -x[1]['active_tasks']):
            print(f"{data['name']:<25} {data['active_tasks']:<15} "
                  f"{data['total_tasks']:<15} "
                  f"{data['hours_assigned']:.0f}/{data['hours_worked']:.0f}")

        # Detailed view for specific member
        if member_id and member_id in workload_data:
            data = workload_data[member_id]
            print(f"\n📋 {data['name']}'s Tasks:")
            print(f"{'Type':<20} {'Description':<30} {'Due':<12} {'Status':<15} {'Hours'}")
            print("-"*80)

            active_tasks = [t for t in data['tasks'] if t['status'] in ['Assigned', 'In Progress']]
            for task in sorted(active_tasks, key=lambda x: x['due_date']):
                desc = task['description'][:28] + '..' if len(task['description']) > 30 else task['description']
                hours = f"{task['hours_estimated']}/{task['hours_actual']}"
                print(f"{task['task_type']:<20} {desc:<30} {task['due_date']:<12} "
                      f"{task['status']:<15} {hours}")

        print("\n" + "="*80 + "\n")

    def record_ic_vote(self, ic_date, manager_id, member_id, vote, rationale=''):
        """Record IC member vote"""
        votes = self._load_csv(self.ic_votes_file)

        vote_id = f"ICV{len(votes) + 1:05d}"

        ic_vote = {
            'vote_id': vote_id,
            'ic_date': ic_date,
            'manager_id': manager_id,
            'member_id': member_id,
            'vote': vote,
            'rationale': rationale,
            'outcome': '',  # To be filled when decision made
            'fund_performance': '',  # To be filled after 2-3 years
            'notes': ''
        }

        votes.append(ic_vote)
        self._save_csv(self.ic_votes_file, votes)

        return vote_id

    def analyze_ic_voting_patterns(self):
        """Analyze IC member voting patterns"""
        votes = self._load_csv(self.ic_votes_file)
        members = self._load_csv(self.team_members_file)

        if not votes:
            return None

        analysis = defaultdict(lambda: {
            'name': '',
            'total_votes': 0,
            'yes_votes': 0,
            'no_votes': 0,
            'abstentions': 0,
            'yes_rate': 0,
            'correct_yes': 0,  # Yes votes where fund performed well
            'correct_no': 0,   # No votes where fund performed poorly
            'accuracy_score': 0
        })

        for vote in votes:
            mid = vote['member_id']
            member = next((m for m in members if m['member_id'] == mid), None)

            if member:
                analysis[mid]['name'] = member['name']
                analysis[mid]['total_votes'] += 1

                vote_value = vote['vote'].lower()
                if vote_value in ['yes', 'approve', 'approved']:
                    analysis[mid]['yes_votes'] += 1
                elif vote_value in ['no', 'decline', 'declined']:
                    analysis[mid]['no_votes'] += 1
                else:
                    analysis[mid]['abstentions'] += 1

                # Check accuracy (if fund performance data available)
                if vote['fund_performance']:
                    performance = vote['fund_performance'].lower()
                    if vote_value == 'yes' and 'good' in performance:
                        analysis[mid]['correct_yes'] += 1
                    elif vote_value == 'no' and 'poor' in performance:
                        analysis[mid]['correct_no'] += 1

        # Calculate rates
        for mid, data in analysis.items():
            if data['total_votes'] > 0:
                data['yes_rate'] = data['yes_votes'] / data['total_votes'] * 100

                correct_total = data['correct_yes'] + data['correct_no']
                votable_decisions = sum(1 for v in votes if v['member_id'] == mid and v['fund_performance'])

                if votable_decisions > 0:
                    data['accuracy_score'] = correct_total / votable_decisions * 100

        return dict(analysis)

    def show_ic_voting_patterns(self):
        """Display IC voting analysis"""
        analysis = self.analyze_ic_voting_patterns()

        if not analysis:
            print("\nNo IC voting data available")
            return

        print("\n" + "="*80)
        print("IC VOTING PATTERNS")
        print("="*80)

        print(f"\n📊 Voting Statistics")
        print(f"{'IC Member':<25} {'Total':<8} {'Yes':<8} {'No':<8} {'Yes Rate':<12} {'Accuracy'}")
        print("-"*80)

        for mid, data in sorted(analysis.items(), key=lambda x: -x[1]['total_votes']):
            accuracy_str = f"{data['accuracy_score']:.1f}%" if data['accuracy_score'] > 0 else "N/A"
            print(f"{data['name']:<25} {data['total_votes']:<8} {data['yes_votes']:<8} "
                  f"{data['no_votes']:<8} {data['yes_rate']:<11.1f}% {accuracy_str}")

        print("\n💡 Insights:")
        print("  • Higher yes rate = More optimistic/risk-tolerant")
        print("  • Lower yes rate = More conservative/selective")
        print("  • Accuracy = % of correct predictions (requires 2-3 year performance data)")

        print("\n" + "="*80 + "\n")

    def log_development_activity(self, member_id, activity_type, description,
                                hours=0, competency=''):
        """Log professional development activity"""
        activities = self._load_csv(self.development_file)

        dev_id = f"DEV{len(activities) + 1:05d}"

        activity = {
            'dev_id': dev_id,
            'member_id': member_id,
            'activity_type': activity_type,
            'activity_date': datetime.now().strftime('%Y-%m-%d'),
            'description': description,
            'hours': str(hours),
            'competency': competency,
            'notes': ''
        }

        activities.append(activity)
        self._save_csv(self.development_file, activities)

        print(f"✓ Logged development: {activity_type} - {description}")
        return dev_id

    def get_member_development(self, member_id):
        """Get development history for member"""
        activities = self._load_csv(self.development_file)
        member_activities = [a for a in activities if a['member_id'] == member_id]

        summary = {
            'total_activities': len(member_activities),
            'total_hours': sum(float(a['hours']) for a in member_activities if a['hours']),
            'by_type': defaultdict(int),
            'by_competency': defaultdict(int),
            'activities': member_activities
        }

        for activity in member_activities:
            summary['by_type'][activity['activity_type']] += 1
            if activity['competency']:
                summary['by_competency'][activity['competency']] += 1

        summary['by_type'] = dict(summary['by_type'])
        summary['by_competency'] = dict(summary['by_competency'])

        return summary

    def show_team_development(self, member_id=None):
        """Display team development"""
        members = self._load_csv(self.team_members_file)

        print("\n" + "="*80)
        print("PROFESSIONAL DEVELOPMENT")
        print("="*80)

        if member_id:
            # Individual view
            member = next((m for m in members if m['member_id'] == member_id), None)
            if not member:
                print(f"\nMember {member_id} not found")
                return

            dev = self.get_member_development(member_id)

            print(f"\n👤 {member['name']}")
            print(f"  Title: {member['title']}")
            print(f"  Hire Date: {member['hire_date']}")

            print(f"\n📊 Development Summary")
            print(f"  Total Activities: {dev['total_activities']}")
            print(f"  Total Hours: {dev['total_hours']:.0f}")

            if dev['by_type']:
                print(f"\n  By Activity Type:")
                for activity_type, count in sorted(dev['by_type'].items(), key=lambda x: -x[1]):
                    print(f"    • {activity_type:<30} {count:>3}")

            if dev['by_competency']:
                print(f"\n  By Competency:")
                for competency, count in sorted(dev['by_competency'].items(), key=lambda x: -x[1]):
                    print(f"    • {competency:<30} {count:>3}")

            # Recent activities
            recent = sorted(dev['activities'], key=lambda x: x['activity_date'], reverse=True)[:5]
            if recent:
                print(f"\n  Recent Activities:")
                for activity in recent:
                    print(f"    {activity['activity_date']}: {activity['activity_type']} - {activity['description'][:50]}")

        else:
            # Team-wide view
            print(f"\n📊 Team Development Summary")

            for member in members:
                if member['status'] == 'Active':
                    dev = self.get_member_development(member['member_id'])
                    print(f"\n{member['name']} ({member['title']})")
                    print(f"  Activities: {dev['total_activities']}, Hours: {dev['total_hours']:.0f}")

        print("\n" + "="*80 + "\n")

    def capacity_analysis(self):
        """Analyze team capacity"""
        members = self._load_csv(self.team_members_file)
        workload = self._load_csv(self.workload_file)

        # Assume 40 hour work week, 160 hours/month
        hours_per_month = 160

        capacity = {
            'total_team_size': len([m for m in members if m['status'] == 'Active']),
            'total_capacity': 0,
            'total_assigned': 0,
            'total_utilized': 0,
            'utilization_rate': 0,
            'by_member': {}
        }

        active_members = [m for m in members if m['status'] == 'Active']
        capacity['total_capacity'] = len(active_members) * hours_per_month

        workload_data = self.get_team_workload()

        for member in active_members:
            mid = member['member_id']
            member_workload = workload_data.get(mid, {})

            assigned = member_workload.get('hours_assigned', 0)
            utilized = member_workload.get('hours_worked', 0)

            capacity['total_assigned'] += assigned
            capacity['total_utilized'] += utilized

            capacity['by_member'][mid] = {
                'name': member['name'],
                'capacity': hours_per_month,
                'assigned': assigned,
                'utilized': utilized,
                'utilization': (assigned / hours_per_month * 100) if hours_per_month > 0 else 0
            }

        if capacity['total_capacity'] > 0:
            capacity['utilization_rate'] = capacity['total_assigned'] / capacity['total_capacity'] * 100

        return capacity

    def show_capacity_analysis(self):
        """Display capacity analysis"""
        capacity = self.capacity_analysis()

        print("\n" + "="*80)
        print("TEAM CAPACITY ANALYSIS")
        print("="*80)

        print(f"\n📊 Overall Capacity")
        print(f"  Team Size: {capacity['total_team_size']}")
        print(f"  Total Capacity: {capacity['total_capacity']:.0f} hours/month")
        print(f"  Hours Assigned: {capacity['total_assigned']:.0f}")
        print(f"  Utilization Rate: {capacity['utilization_rate']:.1f}%")

        print(f"\n👥 By Team Member:")
        print(f"{'Name':<25} {'Capacity':<12} {'Assigned':<12} {'Utilization'}")
        print("-"*80)

        for mid, data in sorted(capacity['by_member'].items(), key=lambda x: -x[1]['utilization']):
            util_icon = '⚠️ ' if data['utilization'] > 100 else '✓ '
            print(f"{data['name']:<25} {data['capacity']:<11.0f}h {data['assigned']:<11.0f}h "
                  f"{util_icon}{data['utilization']:.1f}%")

        print("\n💡 Guidelines:")
        print("  • < 80%: Under-utilized (can take on more)")
        print("  • 80-100%: Well-utilized")
        print("  • > 100%: Over-allocated (reduce workload)")

        print("\n" + "="*80 + "\n")

    def _load_csv(self, filepath):
        """Load CSV file"""
        data = []
        if filepath.exists():
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
        return data

    def _save_csv(self, filepath, data):
        """Save CSV file"""
        if not data:
            return

        fieldnames = data[0].keys()
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


if __name__ == '__main__':
    team = TeamManager()
    team.show_team_workload()

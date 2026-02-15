#!/usr/bin/env python3
"""
Institutional Governance - IC Committees & Decision Framework

Tracks institutional governance per Public Venture Infrastructure model:
- Investment Committee structure (3-5 members, bi-weekly)
- IC meeting logs with decisions
- Co-invest decision framework (Watchlist → Signal → Base → Confirmed → Conviction)
- Manager relationship tracking (8 founding managers)
- Governance reporting (quarterly IC logs, committee minutes)
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
GOV_DIR = DATA_DIR / "governance"


class InstitutionalGovernance:
    """Institutional governance and IC committee management"""

    def __init__(self):
        self.ic_members_file = GOV_DIR / "ic_members.csv"
        self.ic_meetings_file = GOV_DIR / "ic_meetings.csv"
        self.ic_decisions_file = GOV_DIR / "ic_decisions.csv"
        self.coinvest_decisions_file = GOV_DIR / "coinvest_decisions.csv"
        self.manager_contacts_file = GOV_DIR / "manager_contacts.csv"
        self.governance_calendar_file = GOV_DIR / "governance_calendar.csv"
        self._initialize_files()

    def _initialize_files(self):
        """Initialize governance files"""
        GOV_DIR.mkdir(parents=True, exist_ok=True)

        if not self.ic_members_file.exists():
            self.ic_members_file.write_text(
                "member_id,name,ic_role,voting_authority,appointed_date,term_end,status,notes\n"
            )

        if not self.ic_meetings_file.exists():
            self.ic_meetings_file.write_text(
                "meeting_id,meeting_date,meeting_type,attendees,agenda,decisions_made,notes\n"
            )

        if not self.ic_decisions_file.exists():
            self.ic_decisions_file.write_text(
                "decision_id,meeting_id,manager_id,decision_type,decision,"
                "votes_yes,votes_no,votes_abstain,rationale,follow_up,notes\n"
            )

        if not self.coinvest_decisions_file.exists():
            self.coinvest_decisions_file.write_text(
                "coinvest_id,company_name,manager_id,decision_date,tier,"
                "allocation_amount,nav_percentage,ic_vote,rationale,"
                "managers_participating,status,notes\n"
            )

        if not self.manager_contacts_file.exists():
            self.manager_contacts_file.write_text(
                "contact_id,manager_id,manager_name,contact_date,contact_type,"
                "subject,outcome,next_steps,notes\n"
            )

        if not self.governance_calendar_file.exists():
            self.governance_calendar_file.write_text(
                "event_id,event_type,scheduled_date,due_date,status,"
                "owner,description,completed_date,notes\n"
            )

    # ===== IC Committee Management =====

    def add_ic_member(self, member_id, name, ic_role='Member',
                     voting_authority='Full', appointed_date=None):
        """Add IC committee member

        Args:
            member_id: Team member ID (e.g., TM001)
            name: Full name
            ic_role: Chair, Member, Independent Member
            voting_authority: Full, Advisory, Observer
            appointed_date: Date appointed to IC
        """
        members = self._load_csv(self.ic_members_file)

        if appointed_date is None:
            appointed_date = datetime.now().strftime('%Y-%m-%d')

        ic_member = {
            'member_id': member_id,
            'name': name,
            'ic_role': ic_role,
            'voting_authority': voting_authority,
            'appointed_date': appointed_date,
            'term_end': '',
            'status': 'Active',
            'notes': ''
        }

        members.append(ic_member)
        self._save_csv(self.ic_members_file, members)

        print(f"✓ Added IC member: {name} ({ic_role})")
        return member_id

    def get_ic_committee(self):
        """Get current IC committee composition"""
        members = self._load_csv(self.ic_members_file)
        active = [m for m in members if m['status'] == 'Active']
        return active

    def show_ic_committee(self):
        """Display IC committee structure"""
        members = self.get_ic_committee()

        print("\n" + "="*80)
        print("INVESTMENT COMMITTEE COMPOSITION")
        print("="*80)

        if not members:
            print("\nNo IC members configured")
            return

        print(f"\n{'Name':<25} {'Role':<20} {'Voting':<15} {'Appointed'}")
        print("-"*80)

        for member in members:
            print(f"{member['name']:<25} {member['ic_role']:<20} "
                  f"{member['voting_authority']:<15} {member['appointed_date']}")

        chair = [m for m in members if 'Chair' in m['ic_role']]
        voting = [m for m in members if m['voting_authority'] == 'Full']
        independent = [m for m in members if 'Independent' in m['ic_role']]

        print(f"\n📊 Committee Summary:")
        print(f"  Total Members: {len(members)}")
        print(f"  Chair: {chair[0]['name'] if chair else 'Not assigned'}")
        print(f"  Voting Members: {len(voting)}")
        print(f"  Independent Members: {len(independent)}")

        print("\n" + "="*80 + "\n")

    # ===== IC Meeting Management =====

    def log_ic_meeting(self, meeting_date, meeting_type='Regular',
                       attendees='', agenda='', decisions_made=''):
        """Log IC meeting

        Args:
            meeting_date: Date of meeting
            meeting_type: Regular, Special, Emergency
            attendees: Comma-separated member IDs
            agenda: Meeting agenda
            decisions_made: Number of decisions made
        """
        meetings = self._load_csv(self.ic_meetings_file)

        meeting_id = f"ICM{len(meetings) + 1:04d}"

        meeting = {
            'meeting_id': meeting_id,
            'meeting_date': meeting_date,
            'meeting_type': meeting_type,
            'attendees': attendees,
            'agenda': agenda,
            'decisions_made': str(decisions_made),
            'notes': ''
        }

        meetings.append(meeting)
        self._save_csv(self.ic_meetings_file, meetings)

        print(f"✓ Logged IC meeting: {meeting_id} on {meeting_date}")
        return meeting_id

    def record_ic_decision(self, meeting_id, manager_id, decision_type,
                          decision, votes_yes=0, votes_no=0, votes_abstain=0,
                          rationale=''):
        """Record IC decision from meeting

        Args:
            meeting_id: IC meeting ID
            manager_id: Manager being evaluated
            decision_type: Manager Evaluation, Co-Invest Approval, Follow-On, Pass
            decision: Approved, Declined, Defer, Watchlist
            votes_yes/no/abstain: Vote counts
            rationale: Decision rationale
        """
        decisions = self._load_csv(self.ic_decisions_file)

        decision_id = f"ICD{len(decisions) + 1:05d}"

        ic_decision = {
            'decision_id': decision_id,
            'meeting_id': meeting_id,
            'manager_id': manager_id,
            'decision_type': decision_type,
            'decision': decision,
            'votes_yes': str(votes_yes),
            'votes_no': str(votes_no),
            'votes_abstain': str(votes_abstain),
            'rationale': rationale,
            'follow_up': '',
            'notes': ''
        }

        decisions.append(ic_decision)
        self._save_csv(self.ic_decisions_file, decisions)

        print(f"✓ Recorded IC decision: {decision_id} - {decision_type} - {decision}")
        return decision_id

    def show_ic_meetings(self, since_date=None):
        """Display IC meeting history"""
        meetings = self._load_csv(self.ic_meetings_file)

        if since_date:
            meetings = [m for m in meetings
                       if m['meeting_date'] >= since_date]

        print("\n" + "="*80)
        print("IC MEETING HISTORY")
        print("="*80)

        if not meetings:
            print("\nNo IC meetings logged")
            return

        for meeting in sorted(meetings, key=lambda x: x['meeting_date'], reverse=True):
            print(f"\n{meeting['meeting_date']} | {meeting['meeting_type']} | {meeting['meeting_id']}")
            if meeting['attendees']:
                print(f"  Attendees: {meeting['attendees']}")
            if meeting['agenda']:
                print(f"  Agenda: {meeting['agenda']}")
            if meeting['decisions_made']:
                print(f"  Decisions Made: {meeting['decisions_made']}")

        print("\n" + "="*80 + "\n")

    # ===== Co-Invest Decision Framework =====

    def record_coinvest_decision(self, company_name, manager_id, tier,
                                allocation_amount, nav_percentage,
                                ic_vote, rationale='', managers_participating=''):
        """Record co-invest decision per decision tree (Slide 24)

        Args:
            company_name: Portfolio company name
            manager_id: Lead manager ID
            tier: Watchlist, Signal Density, Base, Confirmed, Conviction
            allocation_amount: $ amount allocated
            nav_percentage: % of NAV (cap at 12-15%)
            ic_vote: Approved, Declined, Defer
            rationale: Investment rationale
            managers_participating: Comma-separated manager IDs
        """
        decisions = self._load_csv(self.coinvest_decisions_file)

        coinvest_id = f"CI{len(decisions) + 1:04d}"
        decision_date = datetime.now().strftime('%Y-%m-%d')

        coinvest = {
            'coinvest_id': coinvest_id,
            'company_name': company_name,
            'manager_id': manager_id,
            'decision_date': decision_date,
            'tier': tier,
            'allocation_amount': str(allocation_amount),
            'nav_percentage': str(nav_percentage),
            'ic_vote': ic_vote,
            'rationale': rationale,
            'managers_participating': managers_participating,
            'status': 'Active' if ic_vote == 'Approved' else 'Declined',
            'notes': ''
        }

        # Validate NAV cap per slide 24
        if float(nav_percentage) > 15:
            print(f"⚠️  WARNING: NAV percentage {nav_percentage}% exceeds 15% cap")
            print(f"   Requires IC override per governance policy")

        decisions.append(coinvest)
        self._save_csv(self.coinvest_decisions_file, decisions)

        print(f"✓ Recorded co-invest decision: {coinvest_id} - {company_name} - {tier}")
        return coinvest_id

    def show_coinvest_pipeline(self, tier=None):
        """Display co-invest pipeline by tier"""
        decisions = self._load_csv(self.coinvest_decisions_file)

        if tier:
            decisions = [d for d in decisions if d['tier'] == tier]

        print("\n" + "="*80)
        print("CO-INVEST DECISION PIPELINE")
        print("="*80)

        if not decisions:
            print("\nNo co-invest decisions recorded")
            return

        # Group by tier
        by_tier = defaultdict(list)
        for decision in decisions:
            by_tier[decision['tier']].append(decision)

        tier_order = ['Watchlist', 'Signal Density', 'Base', 'Confirmed', 'Conviction']

        for tier in tier_order:
            if tier in by_tier:
                print(f"\n{'='*80}")
                print(f"{tier.upper()}")
                print(f"{'='*80}")

                for d in by_tier[tier]:
                    allocation = float(d['allocation_amount']) / 1_000_000
                    nav_pct = float(d['nav_percentage'])

                    print(f"\n{d['company_name']} ({d['coinvest_id']})")
                    print(f"  Manager: {d['manager_id']}")
                    print(f"  Allocation: ${allocation:.1f}M ({nav_pct:.1f}% NAV)")
                    print(f"  IC Vote: {d['ic_vote']}")
                    if d['managers_participating']:
                        print(f"  Participating Managers: {d['managers_participating']}")
                    print(f"  Rationale: {d['rationale'][:100]}")

        # Summary
        total_allocation = sum(float(d['allocation_amount']) for d in decisions
                              if d['status'] == 'Active')
        total_nav = sum(float(d['nav_percentage']) for d in decisions
                       if d['status'] == 'Active')

        print(f"\n{'='*80}")
        print(f"SUMMARY")
        print(f"{'='*80}")
        print(f"  Active Positions: {len([d for d in decisions if d['status'] == 'Active'])}")
        print(f"  Total Allocation: ${total_allocation/1_000_000:.1f}M")
        print(f"  Total NAV%: {total_nav:.1f}%")

        if total_nav > 35:
            print(f"\n  ⚠️  WARNING: Co-invest sleeve exceeds 35% target")

        print("\n" + "="*80 + "\n")

    # ===== Manager Relationship Tracking =====

    def log_manager_contact(self, manager_id, manager_name, contact_type,
                           subject, outcome='', next_steps=''):
        """Log interaction with founding manager

        Args:
            manager_id: Manager ID (M001-M008 for founding 8)
            manager_name: Manager firm name
            contact_type: Call, Meeting, Email, Pipeline Review, Quarterly Update
            subject: Topic discussed
            outcome: Result of interaction
            next_steps: Follow-up actions
        """
        contacts = self._load_csv(self.manager_contacts_file)

        contact_id = f"MC{len(contacts) + 1:05d}"
        contact_date = datetime.now().strftime('%Y-%m-%d')

        contact = {
            'contact_id': contact_id,
            'manager_id': manager_id,
            'manager_name': manager_name,
            'contact_date': contact_date,
            'contact_type': contact_type,
            'subject': subject,
            'outcome': outcome,
            'next_steps': next_steps,
            'notes': ''
        }

        contacts.append(contact)
        self._save_csv(self.manager_contacts_file, contacts)

        print(f"✓ Logged manager contact: {manager_name} - {contact_type}")
        return contact_id

    def show_manager_contacts(self, manager_id=None, since_date=None):
        """Display manager contact history"""
        contacts = self._load_csv(self.manager_contacts_file)

        if manager_id:
            contacts = [c for c in contacts if c['manager_id'] == manager_id]

        if since_date:
            contacts = [c for c in contacts if c['contact_date'] >= since_date]

        print("\n" + "="*80)
        print("MANAGER RELATIONSHIP TRACKING")
        print("="*80)

        if not contacts:
            print("\nNo manager contacts logged")
            return

        # Group by manager
        by_manager = defaultdict(list)
        for contact in contacts:
            by_manager[contact['manager_name']].append(contact)

        for manager_name, manager_contacts in sorted(by_manager.items()):
            print(f"\n{'='*80}")
            print(f"{manager_name}")
            print(f"{'='*80}")
            print(f"  Total Contacts: {len(manager_contacts)}")

            # Recent contacts
            recent = sorted(manager_contacts, key=lambda x: x['contact_date'], reverse=True)[:5]
            for contact in recent:
                print(f"\n  {contact['contact_date']} | {contact['contact_type']}")
                print(f"    {contact['subject']}")
                if contact['outcome']:
                    print(f"    Outcome: {contact['outcome']}")

        print("\n" + "="*80 + "\n")

    # ===== Governance Reporting =====

    def schedule_governance_event(self, event_type, scheduled_date, due_date,
                                 owner, description=''):
        """Schedule governance event

        Args:
            event_type: IC Meeting, Quarterly IC Log, Semi-Annual Minutes,
                       Annual Audit, Board Meeting, Valuation Committee
            scheduled_date: When event happens
            due_date: When deliverable is due
            owner: Person responsible
            description: Event description
        """
        events = self._load_csv(self.governance_calendar_file)

        event_id = f"GE{len(events) + 1:04d}"

        event = {
            'event_id': event_id,
            'event_type': event_type,
            'scheduled_date': scheduled_date,
            'due_date': due_date,
            'status': 'Scheduled',
            'owner': owner,
            'description': description,
            'completed_date': '',
            'notes': ''
        }

        events.append(event)
        self._save_csv(self.governance_calendar_file, events)

        print(f"✓ Scheduled governance event: {event_id} - {event_type} on {scheduled_date}")
        return event_id

    def show_governance_calendar(self, upcoming_days=90):
        """Display upcoming governance events"""
        events = self._load_csv(self.governance_calendar_file)

        today = datetime.now()
        cutoff = (today + timedelta(days=upcoming_days)).strftime('%Y-%m-%d')

        upcoming = [e for e in events
                   if e['status'] != 'Completed' and e['due_date'] <= cutoff]

        print("\n" + "="*80)
        print(f"GOVERNANCE CALENDAR (Next {upcoming_days} Days)")
        print("="*80)

        if not upcoming:
            print(f"\nNo governance events due in next {upcoming_days} days")
            return

        # Group by event type
        by_type = defaultdict(list)
        for event in upcoming:
            by_type[event['event_type']].append(event)

        for event_type, type_events in sorted(by_type.items()):
            print(f"\n{event_type}:")
            for event in sorted(type_events, key=lambda x: x['due_date']):
                days_until = (datetime.strptime(event['due_date'], '%Y-%m-%d') - today).days

                if days_until < 0:
                    status_icon = "🔴"
                    status_text = f"OVERDUE by {abs(days_until)} days"
                elif days_until < 7:
                    status_icon = "🟡"
                    status_text = f"Due in {days_until} days"
                else:
                    status_icon = "🟢"
                    status_text = f"Due in {days_until} days"

                print(f"  {status_icon} {event['due_date']} - {event['description']} ({status_text})")
                print(f"     Owner: {event['owner']}")

        print("\n" + "="*80 + "\n")

    # ===== Quarterly IC Activity Report =====

    def generate_ic_activity_report(self, quarter_start, quarter_end):
        """Generate quarterly IC activity log (per Slide 11 reporting requirements)"""
        meetings = self._load_csv(self.ic_meetings_file)
        decisions = self._load_csv(self.ic_decisions_file)
        coinvests = self._load_csv(self.coinvest_decisions_file)

        quarter_meetings = [m for m in meetings
                           if quarter_start <= m['meeting_date'] <= quarter_end]
        quarter_decisions = [d for d in decisions
                            if d['meeting_id'] in [m['meeting_id'] for m in quarter_meetings]]
        quarter_coinvests = [c for c in coinvests
                            if quarter_start <= c['decision_date'] <= quarter_end]

        print("\n" + "="*80)
        print(f"IC ACTIVITY REPORT - Q{datetime.strptime(quarter_start, '%Y-%m-%d').month//3 + 1}")
        print(f"{quarter_start} to {quarter_end}")
        print("="*80)

        print(f"\n📊 Summary Metrics")
        print(f"  IC Meetings Held: {len(quarter_meetings)}")
        print(f"  Decisions Made: {len(quarter_decisions)}")
        print(f"  Co-Invest Approvals: {len([c for c in quarter_coinvests if c['ic_vote'] == 'Approved'])}")

        if quarter_meetings:
            print(f"\n📅 Meeting Schedule:")
            for meeting in quarter_meetings:
                print(f"  {meeting['meeting_date']} - {meeting['meeting_type']}")

        if quarter_decisions:
            print(f"\n✓ Decisions by Type:")
            decision_types = defaultdict(int)
            for decision in quarter_decisions:
                decision_types[decision['decision_type']] += 1

            for dec_type, count in sorted(decision_types.items()):
                print(f"  {dec_type}: {count}")

        if quarter_coinvests:
            print(f"\n💰 Co-Invest Activity:")
            approved = [c for c in quarter_coinvests if c['ic_vote'] == 'Approved']
            total_allocation = sum(float(c['allocation_amount']) for c in approved) / 1_000_000

            print(f"  Approved Investments: {len(approved)}")
            print(f"  Total Capital Deployed: ${total_allocation:.1f}M")

            print(f"\n  By Tier:")
            by_tier = defaultdict(int)
            for co in approved:
                by_tier[co['tier']] += 1

            for tier, count in sorted(by_tier.items()):
                print(f"    {tier}: {count}")

        print("\n" + "="*80 + "\n")

    # ===== Utility Methods =====

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
    gov = InstitutionalGovernance()
    gov.show_ic_committee()
    gov.show_governance_calendar()

#!/usr/bin/env python3
"""
Demo Institutional Governance Data

Creates sample IC committee, meetings, co-invest decisions, and manager contacts
based on the Public Venture Infrastructure Platform model (Slides 11, 12, 24)
"""

from governance import InstitutionalGovernance
from datetime import datetime, timedelta

def create_demo_governance_data():
    """Create sample institutional governance data"""
    gov = InstitutionalGovernance()

    print("Creating demo institutional governance data...\n")

    # IC Committee Structure (Slide 11: 3-5 members, bi-weekly)
    print("📋 Setting up Investment Committee...")

    ic_committee = [
        {
            'member_id': 'TM001',
            'name': 'Ken Wallace',
            'ic_role': 'IC Chair',
            'voting_authority': 'Full',
            'appointed_date': '2023-01-01'
        },
        {
            'member_id': 'TM002',
            'name': 'Sarah Chen',
            'ic_role': 'IC Member',
            'voting_authority': 'Full',
            'appointed_date': '2023-06-01'
        },
        {
            'member_id': 'TM003',
            'name': 'Marcus Rodriguez',
            'ic_role': 'IC Member',
            'voting_authority': 'Full',
            'appointed_date': '2024-01-15'
        }
    ]

    for member in ic_committee:
        gov.add_ic_member(**member)

    # IC Meetings (bi-weekly per Slide 11)
    print("\n📅 Logging IC meetings...")

    meetings = [
        {
            'meeting_date': '2026-01-15',
            'meeting_type': 'Regular',
            'attendees': 'TM001,TM002,TM003',
            'agenda': 'Manager pipeline review, Kindred Ventures deep DD results',
            'decisions_made': '2'
        },
        {
            'meeting_date': '2026-01-29',
            'meeting_type': 'Regular',
            'attendees': 'TM001,TM002,TM003',
            'agenda': 'Underscore VC approval, Co-invest opportunity review',
            'decisions_made': '3'
        },
        {
            'meeting_date': '2026-02-12',
            'meeting_type': 'Regular',
            'attendees': 'TM001,TM002',
            'agenda': 'Q1 portfolio review, New manager sourcing',
            'decisions_made': '1'
        }
    ]

    meeting_ids = []
    for meeting in meetings:
        meeting_id = gov.log_ic_meeting(**meeting)
        meeting_ids.append(meeting_id)

    # IC Decisions
    print("\n✅ Recording IC decisions...")

    decisions = [
        {
            'meeting_id': meeting_ids[0],
            'manager_id': 'M003',
            'decision_type': 'Manager Evaluation',
            'decision': 'Approved',
            'votes_yes': 2,
            'votes_no': 0,
            'votes_abstain': 1,
            'rationale': 'Strong consumer tech focus, solid track record'
        },
        {
            'meeting_id': meeting_ids[0],
            'manager_id': 'M009',
            'decision_type': 'Manager Evaluation',
            'decision': 'Watchlist',
            'votes_yes': 0,
            'votes_no': 0,
            'votes_abstain': 0,
            'rationale': 'Interesting thesis but need more data on fund I performance'
        },
        {
            'meeting_id': meeting_ids[1],
            'manager_id': 'M008',
            'decision_type': 'Manager Evaluation',
            'decision': 'Approved',
            'votes_yes': 3,
            'votes_no': 0,
            'votes_abstain': 0,
            'rationale': 'Excellent enterprise SaaS pipeline, strong references'
        },
        {
            'meeting_id': meeting_ids[1],
            'manager_id': 'CompanyX',
            'decision_type': 'Co-Invest Approval',
            'decision': 'Approved',
            'votes_yes': 3,
            'votes_no': 0,
            'votes_abstain': 0,
            'rationale': '2 managers participating, strong revenue inflection'
        },
        {
            'meeting_id': meeting_ids[2],
            'manager_id': 'M010',
            'decision_type': 'Manager Evaluation',
            'decision': 'Defer',
            'votes_yes': 0,
            'votes_no': 0,
            'votes_abstain': 0,
            'rationale': 'Wait for Q1 performance data'
        }
    ]

    for decision in decisions:
        gov.record_ic_decision(**decision)

    # Co-Invest Decisions (Slide 24: Watchlist → Signal → Base → Confirmed → Conviction)
    print("\n💰 Recording co-invest decisions...")

    coinvest_decisions = [
        {
            'company_name': 'Mercury (Embedded Finance)',
            'manager_id': 'M001',  # Chapter One
            'tier': 'Conviction',
            'allocation_amount': 25000000,  # $25M
            'nav_percentage': 12.0,
            'ic_vote': 'Approved',
            'rationale': '2+ managers (Chapter One, Gilroy), fintech leader, strong revenue growth',
            'managers_participating': 'M001,M008'
        },
        {
            'company_name': 'Supabase (Dev Tools)',
            'manager_id': 'M001',  # Chapter One
            'tier': 'Confirmed',
            'allocation_amount': 15000000,  # $15M
            'nav_percentage': 7.5,
            'ic_vote': 'Approved',
            'rationale': '2 managers, AI infra play, clean cap table',
            'managers_participating': 'M001,M002'
        },
        {
            'company_name': 'AI Infra Co (Seed)',
            'manager_id': 'M005',  # Caffeinated
            'tier': 'Base',
            'allocation_amount': 7000000,  # $7M
            'nav_percentage': 3.5,
            'ic_vote': 'Approved',
            'rationale': '1 manager confirmed, early AI infrastructure',
            'managers_participating': 'M005'
        },
        {
            'company_name': 'Enterprise SaaS Co',
            'manager_id': 'M004',  # Swift Ventures
            'tier': 'Signal Density',
            'allocation_amount': 3000000,  # $3M
            'nav_percentage': 1.5,
            'ic_vote': 'Approved',
            'rationale': '2+ manager interest, escalating to base tier',
            'managers_participating': 'M004,M007'
        },
        {
            'company_name': 'Consumer Tech Startup',
            'manager_id': 'M003',  # Kindred
            'tier': 'Watchlist',
            'allocation_amount': 0,
            'nav_percentage': 0,
            'ic_vote': 'Watchlist',
            'rationale': 'Backed by 1 manager, monitoring for signal convergence',
            'managers_participating': 'M003'
        },
        {
            'company_name': 'Defense Tech Co',
            'manager_id': 'M001',  # 8VC (from Slide 18)
            'tier': 'Confirmed',
            'allocation_amount': 12000000,  # $12M
            'nav_percentage': 6.0,
            'ic_vote': 'Approved',
            'rationale': 'Infrastructure + defense cluster, 8VC lead with Quiet participation',
            'managers_participating': 'M001,M006'
        }
    ]

    for coinvest in coinvest_decisions:
        gov.record_coinvest_decision(**coinvest)

    # Manager Contacts (The Founding 8 from Slides 12-17)
    print("\n🤝 Logging manager relationships...")

    manager_contacts = [
        {
            'manager_id': 'M001',
            'manager_name': '8VC',
            'contact_type': 'Pipeline Review',
            'subject': 'Q1 2026 portfolio company updates',
            'outcome': 'Reviewed 3 defense tech investments, identified 1 co-invest opportunity',
            'next_steps': 'Schedule follow-up on Epirus Series B'
        },
        {
            'manager_id': 'M002',
            'manager_name': 'Chapter One',
            'contact_type': 'Quarterly Update',
            'subject': 'Fund performance review and pipeline',
            'outcome': 'Mercury performing well, 2 new seed investments in AI infra',
            'next_steps': 'Evaluate co-invest in Together.ai Series A'
        },
        {
            'manager_id': 'M003',
            'manager_name': 'New Normal Fund (Allison Pickens)',
            'contact_type': 'Call',
            'subject': 'GTM/ARR discipline layer discussion',
            'outcome': 'Reviewed 5 portfolio companies with strong revenue metrics',
            'next_steps': 'Schedule IC presentation for Q2'
        },
        {
            'manager_id': 'M004',
            'manager_name': 'Swift Ventures',
            'contact_type': 'Meeting',
            'subject': 'Enterprise SaaS pipeline and co-invest opportunities',
            'outcome': 'Discussed 3 Series A companies with strong traction',
            'next_steps': 'Share data room access for Arize follow-on'
        },
        {
            'manager_id': 'M005',
            'manager_name': 'Caffeinated Capital',
            'contact_type': 'Pipeline Review',
            'subject': 'AI-first founders seed pipeline',
            'outcome': 'High-velocity seed pipeline, 10 new investments YTD',
            'next_steps': 'Bi-weekly co-invest review cadence'
        },
        {
            'manager_id': 'M006',
            'manager_name': 'Quiet Capital',
            'contact_type': 'Quarterly Update',
            'subject': 'Multi-sector optionality satellite review',
            'outcome': 'Broad diversification across sectors, lowest correlation profile',
            'next_steps': 'Continue quarterly reviews'
        },
        {
            'manager_id': 'M007',
            'manager_name': 'Marathon Management',
            'contact_type': 'Call',
            'subject': 'Enterprise/fintech compounder opportunities',
            'outcome': 'Reviewed DPI velocity and scaling discipline',
            'next_steps': 'Evaluate co-invest in fintech Series B'
        },
        {
            'manager_id': 'M008',
            'manager_name': 'Gilroy (Ex-Coatue GP)',
            'contact_type': 'Meeting',
            'subject': 'Embedded finance bridge opportunities',
            'outcome': 'Mercury, Arta, Melio performing well. Late seed → growth sweet spot',
            'next_steps': 'Co-invest in next embedded fintech round'
        }
    ]

    for contact in manager_contacts:
        gov.log_manager_contact(**contact)

    # Governance Calendar (Slide 11: Quarterly, Semi-Annual, Annual reporting)
    print("\n📅 Scheduling governance events...")

    today = datetime.now()

    governance_events = [
        {
            'event_type': 'IC Meeting',
            'scheduled_date': (today + timedelta(days=14)).strftime('%Y-%m-%d'),
            'due_date': (today + timedelta(days=14)).strftime('%Y-%m-%d'),
            'owner': 'Ken Wallace',
            'description': 'Bi-weekly IC meeting - Manager updates'
        },
        {
            'event_type': 'IC Meeting',
            'scheduled_date': (today + timedelta(days=28)).strftime('%Y-%m-%d'),
            'due_date': (today + timedelta(days=28)).strftime('%Y-%m-%d'),
            'owner': 'Ken Wallace',
            'description': 'Bi-weekly IC meeting - Co-invest approvals'
        },
        {
            'event_type': 'Quarterly IC Log',
            'scheduled_date': (today + timedelta(days=45)).strftime('%Y-%m-%d'),
            'due_date': (today + timedelta(days=45)).strftime('%Y-%m-%d'),
            'owner': 'Sarah Chen',
            'description': 'Q1 2026 IC activity log (per Slide 11 governance reporting)'
        },
        {
            'event_type': 'Valuation Committee',
            'scheduled_date': (today + timedelta(days=60)).strftime('%Y-%m-%d'),
            'due_date': (today + timedelta(days=60)).strftime('%Y-%m-%d'),
            'owner': 'Independent Chair',
            'description': 'Quarterly fair value determinations'
        },
        {
            'event_type': 'Board Meeting',
            'scheduled_date': (today + timedelta(days=75)).strftime('%Y-%m-%d'),
            'due_date': (today + timedelta(days=75)).strftime('%Y-%m-%d'),
            'owner': 'Ken Wallace',
            'description': 'Quarterly Board of Directors meeting'
        },
        {
            'event_type': 'Semi-Annual Minutes',
            'scheduled_date': (today + timedelta(days=150)).strftime('%Y-%m-%d'),
            'due_date': (today + timedelta(days=150)).strftime('%Y-%m-%d'),
            'owner': 'Sarah Chen',
            'description': 'Semi-annual audited financials and governance minutes'
        }
    ]

    for event in governance_events:
        gov.schedule_governance_event(**event)

    print(f"\n✓ Created demo institutional governance data")
    print(f"\nTry these commands:")
    print("  ./scripts/newco_cli.py governance ic-committee")
    print("  ./scripts/newco_cli.py governance ic-meetings")
    print("  ./scripts/newco_cli.py governance coinvest-pipeline")
    print("  ./scripts/newco_cli.py governance manager-contacts")
    print("  ./scripts/newco_cli.py governance calendar")
    print("  ./scripts/newco_cli.py governance ic-report --quarter Q1")

if __name__ == '__main__':
    create_demo_governance_data()

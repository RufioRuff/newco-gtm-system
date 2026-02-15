#!/usr/bin/env python3
"""
Demo Portfolio Data

Creates sample fund investments and manager pipeline for testing
"""

from portfolio_management import PortfolioManager
from manager_crm import ManagerCRM
from datetime import datetime, timedelta

def create_demo_portfolio():
    """Create sample portfolio for testing"""
    pm = PortfolioManager()
    crm = ManagerCRM()

    print("Creating demo portfolio and manager pipeline...")
    print()

    # Add fund investments to portfolio
    funds_data = [
        {
            'fund_name': 'Acme Ventures Fund III',
            'manager': 'Acme Ventures',
            'commitment': 3000000,
            'vintage': 2024,
            'stage': 'Seed/Series A',
            'sector': 'Enterprise Software',
            'paid_in': 600000,
            'nav': 720000,
            'distributions': 0
        },
        {
            'fund_name': 'Beta Capital Fund II',
            'manager': 'Beta Capital Partners',
            'commitment': 2500000,
            'vintage': 2023,
            'stage': 'Series A/B',
            'sector': 'Consumer Tech',
            'paid_in': 1500000,
            'nav': 1950000,
            'distributions': 300000
        },
        {
            'fund_name': 'Gamma Growth Fund I',
            'manager': 'Gamma Growth Partners',
            'commitment': 5000000,
            'vintage': 2024,
            'stage': 'Growth',
            'sector': 'Fintech',
            'paid_in': 2000000,
            'nav': 2400000,
            'distributions': 0
        },
        {
            'fund_name': 'Delta Seed Fund IV',
            'manager': 'Delta Ventures',
            'commitment': 2000000,
            'vintage': 2025,
            'stage': 'Pre-seed/Seed',
            'sector': 'AI/ML',
            'paid_in': 400000,
            'nav': 500000,
            'distributions': 0
        },
        {
            'fund_name': 'Epsilon Ventures Fund V',
            'manager': 'Epsilon Capital',
            'commitment': 4000000,
            'vintage': 2023,
            'stage': 'Series A/B',
            'sector': 'Healthcare',
            'paid_in': 2400000,
            'nav': 3200000,
            'distributions': 800000
        }
    ]

    print("📊 Adding fund investments...")
    for fund_data in funds_data:
        fund_id = pm.add_fund(
            fund_name=fund_data['fund_name'],
            manager_name=fund_data['manager'],
            commitment=fund_data['commitment'],
            vintage_year=fund_data['vintage'],
            stage_focus=fund_data['stage'],
            sector_focus=fund_data['sector']
        )

        # Add capital calls
        for i in range(0, int(fund_data['paid_in']), 500000):
            amount = min(500000, int(fund_data['paid_in']) - i)
            if amount > 0:
                call_date = (datetime.now() - timedelta(days=90*(i//500000))).strftime('%Y-%m-%d')
                call_id = pm.add_capital_call(fund_id, amount, call_date)
                # Mark as paid
                calls = pm._load_csv(pm.capital_calls_file)
                for call in calls:
                    if call['call_id'] == call_id:
                        call['status'] = 'Paid'
                        call['paid_date'] = call_date
                pm._save_csv(pm.capital_calls_file, calls)

        # Add NAV
        pm.add_fund_nav(fund_id, fund_data['nav'])

        # Add distributions if any
        if fund_data['distributions'] > 0:
            pm.add_distribution(fund_id, fund_data['distributions'], 'Capital Gain')

    print(f"\n✓ Added {len(funds_data)} fund investments")
    print(f"  Total Commitment: ${sum(f['commitment'] for f in funds_data):,.0f}")

    # Add manager pipeline
    print("\n👥 Adding manager pipeline...")

    managers_data = [
        {
            'fund_name': 'Zeta Ventures Fund I',
            'gps': 'Jane Smith, John Doe',
            'firm': 'Zeta Ventures',
            'stage': 'Seed',
            'sector': 'Climate Tech',
            'pipeline_stage': 'Sourced',
            'source': 'VC Partner Referral'
        },
        {
            'fund_name': 'Theta Capital Fund II',
            'gps': 'Alice Wong, Bob Chen',
            'firm': 'Theta Capital',
            'stage': 'Series A',
            'sector': 'Enterprise SaaS',
            'pipeline_stage': 'Screening',
            'source': 'Platform Referral'
        },
        {
            'fund_name': 'Iota Seed Fund III',
            'gps': 'Maria Garcia, Tom Wilson',
            'firm': 'Iota Partners',
            'stage': 'Seed/A',
            'sector': 'Biotech',
            'pipeline_stage': 'Deep DD',
            'source': 'Conference'
        },
        {
            'fund_name': 'Kappa Growth Fund I',
            'gps': 'Sarah Lee',
            'firm': 'Kappa Capital',
            'stage': 'Growth',
            'sector': 'Consumer',
            'pipeline_stage': 'IC Review',
            'source': 'VC Partner Referral'
        },
        {
            'fund_name': 'Lambda Ventures Fund IV',
            'gps': 'Michael Brown, Lisa Taylor',
            'firm': 'Lambda Ventures',
            'stage': 'Seed',
            'sector': 'AI/ML',
            'pipeline_stage': 'Sourced',
            'source': 'Inbound'
        }
    ]

    for manager_data in managers_data:
        manager_id = crm.add_manager(
            fund_name=manager_data['fund_name'],
            gp_names=manager_data['gps'],
            firm_name=manager_data['firm'],
            stage_focus=manager_data['stage'],
            sector_focus=manager_data['sector'],
            pipeline_stage=manager_data['pipeline_stage'],
            source=manager_data['source']
        )

        # If in Deep DD, start DD process
        if manager_data['pipeline_stage'] == 'Deep DD':
            crm.start_due_diligence(manager_id, 'Senior Analyst')

    print(f"\n✓ Added {len(managers_data)} managers to pipeline")

    print("\n✓ Demo portfolio complete!")
    print("\nTry these commands:")
    print("  ./scripts/newco_cli.py portfolio show")
    print("  ./scripts/newco_cli.py portfolio cashflow")
    print("  ./scripts/newco_cli.py managers pipeline")
    print("  ./scripts/newco_cli.py managers dd M003")


if __name__ == '__main__':
    create_demo_portfolio()

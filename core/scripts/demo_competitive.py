#!/usr/bin/env python3
"""
Demo Competitive Intelligence Data

Creates sample competitors, manager universe, and fee benchmarks
"""

from competitive_intelligence import CompetitiveIntelligence

def create_demo_competitive_data():
    """Create sample competitive intelligence data"""
    intel = CompetitiveIntelligence()

    print("Creating demo competitive intelligence data...\n")

    # Competitors - Public VC Vehicles
    print("📊 Adding competitors...")

    competitors_data = [
        {
            'name': 'Hercules Capital (HTGC)',
            'type': 'BDC - Venture Debt',
            'structure': 'Publicly Traded',
            'aum': 3500000000,
            'management_fee': 2.00,
            'incentive_fee': 20.0,
            'ticker': 'HTGC',
            'strategy': 'Venture debt and growth-stage lending'
        },
        {
            'name': 'TriplePoint Venture Growth (TPVG)',
            'type': 'BDC - Venture Debt',
            'structure': 'Publicly Traded',
            'aum': 1800000000,
            'management_fee': 2.00,
            'incentive_fee': 20.0,
            'ticker': 'TPVG',
            'strategy': 'Venture growth-stage debt financing'
        },
        {
            'name': 'Altimar Acquisition Corp',
            'type': 'SPAC',
            'structure': 'Publicly Traded',
            'aum': 500000000,
            'management_fee': 0,
            'incentive_fee': 20.0,
            'ticker': 'ATCX',
            'strategy': 'Growth equity via SPAC'
        },
        {
            'name': 'Neuberger Berman Next Gen Tech',
            'type': 'Interval Fund',
            'structure': 'Listed Fund',
            'aum': 250000000,
            'management_fee': 1.85,
            'incentive_fee': 15.0,
            'ticker': '',
            'strategy': 'Growth-stage technology investments'
        },
        {
            'name': 'Hamilton Lane Private Assets Fund',
            'type': 'Fund-of-Funds',
            'structure': 'Private Fund',
            'aum': 5000000000,
            'management_fee': 1.50,
            'incentive_fee': 10.0,
            'ticker': '',
            'strategy': 'Diversified VC fund-of-funds'
        },
        {
            'name': 'Vintage Investment Partners',
            'type': 'Fund-of-Funds',
            'structure': 'Private Fund',
            'aum': 2000000000,
            'management_fee': 1.25,
            'incentive_fee': 10.0,
            'ticker': '',
            'strategy': 'VC and growth fund-of-funds'
        },
        {
            'name': 'Industry Ventures',
            'type': 'Fund-of-Funds + Secondaries',
            'structure': 'Private Fund',
            'aum': 3000000000,
            'management_fee': 1.50,
            'incentive_fee': 15.0,
            'ticker': '',
            'strategy': 'VC secondaries and fund-of-funds'
        }
    ]

    for comp in competitors_data:
        intel.add_competitor(**comp)

    # Manager Universe - Emerging Managers
    print("\n🌐 Adding manager universe...")

    managers_data = [
        {
            'firm_name': 'Operator Collective',
            'fund_name': 'Operator Collective Fund II',
            'fund_size': 150000000,
            'vintage': 2024,
            'stage_focus': 'Seed/Series A',
            'sector_focus': 'Enterprise SaaS',
            'lead_gp': 'Mallun Yen',
            'fundraising_status': 'Closed',
            'our_status': 'Passed'
        },
        {
            'firm_name': 'Character VC',
            'fund_name': 'Character Fund II',
            'fund_size': 60000000,
            'vintage': 2024,
            'stage_focus': 'Pre-seed/Seed',
            'sector_focus': 'Consumer',
            'lead_gp': 'Masha Drokova',
            'fundraising_status': 'Open',
            'our_status': 'Screening'
        },
        {
            'firm_name': 'Kindred Ventures',
            'fund_name': 'Kindred Fund III',
            'fund_size': 100000000,
            'vintage': 2024,
            'stage_focus': 'Seed',
            'sector_focus': 'Consumer Tech',
            'lead_gp': 'Kanyi Maqubela',
            'fundraising_status': 'Open',
            'our_status': 'Deep DD'
        },
        {
            'firm_name': 'Contrary',
            'fund_name': 'Contrary Fund IV',
            'fund_size': 250000000,
            'vintage': 2025,
            'stage_focus': 'Seed/Series A',
            'sector_focus': 'Multi-sector',
            'lead_gp': 'Eric Tarczynski',
            'fundraising_status': 'First Close',
            'our_status': 'Tracking'
        },
        {
            'firm_name': 'Equal Ventures',
            'fund_name': 'Equal Fund III',
            'fund_size': 75000000,
            'vintage': 2024,
            'stage_focus': 'Seed',
            'sector_focus': 'Vertical SaaS',
            'lead_gp': 'Rick Zullo',
            'fundraising_status': 'Closed',
            'our_status': 'Committed'
        },
        {
            'firm_name': 'Playground Global',
            'fund_name': 'Playground Fund III',
            'fund_size': 200000000,
            'vintage': 2024,
            'stage_focus': 'Seed/Series A',
            'sector_focus': 'Deep Tech',
            'lead_gp': 'Bruce Leak',
            'fundraising_status': 'Open',
            'our_status': 'Tracking'
        },
        {
            'firm_name': 'Backstage Capital',
            'fund_name': 'Backstage Fund III',
            'fund_size': 50000000,
            'vintage': 2024,
            'stage_focus': 'Pre-seed/Seed',
            'sector_focus': 'Diverse Founders',
            'lead_gp': 'Arlan Hamilton',
            'fundraising_status': 'Open',
            'our_status': 'Tracking'
        },
        {
            'firm_name': 'Underscore VC',
            'fund_name': 'Underscore Fund IV',
            'fund_size': 125000000,
            'vintage': 2024,
            'stage_focus': 'Seed/Series A',
            'sector_focus': 'Enterprise',
            'lead_gp': 'Michael Skok',
            'fundraising_status': 'Open',
            'our_status': 'Screening'
        }
    ]

    for mgr in managers_data:
        intel.add_manager_to_universe(**mgr)

    # Fee Benchmarks
    print("\n💰 Adding fee benchmarks...")

    benchmarks = intel._load_csv(intel.fee_benchmarks_file)

    fee_benchmarks = [
        {
            'vehicle_type': 'Publicly Traded BDC',
            'name': 'Hercules Capital',
            'management_fee_rate': '2.00',
            'management_fee_basis': 'Total Assets',
            'carry_rate': '20.0',
            'hurdle_rate': '7.0',
            'catch_up': 'Yes',
            'gp_commitment': '',
            'fund_size': '3500000000',
            'notes': 'Industry standard for BDCs'
        },
        {
            'vehicle_type': 'Private Fund-of-Funds',
            'name': 'Hamilton Lane',
            'management_fee_rate': '1.50',
            'management_fee_basis': 'Committed Capital',
            'carry_rate': '10.0',
            'hurdle_rate': '8.0',
            'catch_up': 'Yes',
            'gp_commitment': '2.0',
            'fund_size': '1000000000',
            'notes': 'Large established FoF'
        },
        {
            'vehicle_type': 'Private Fund-of-Funds',
            'name': 'Vintage Investment Partners',
            'management_fee_rate': '1.25',
            'management_fee_basis': 'Committed Capital',
            'carry_rate': '10.0',
            'hurdle_rate': '8.0',
            'catch_up': 'Yes',
            'gp_commitment': '1.0',
            'fund_size': '500000000',
            'notes': 'Mid-size FoF'
        },
        {
            'vehicle_type': 'Publicly Traded FoF',
            'name': 'NEWCO (Our Structure)',
            'management_fee_rate': '1.25',
            'management_fee_basis': 'Committed Capital',
            'carry_rate': '0',
            'hurdle_rate': '0',
            'catch_up': 'No',
            'gp_commitment': '5.0',
            'fund_size': '50000000',
            'notes': 'No incentive fee - fee transparency'
        },
        {
            'vehicle_type': 'Interval Fund',
            'name': 'Neuberger Berman',
            'management_fee_rate': '1.85',
            'management_fee_basis': 'NAV',
            'carry_rate': '15.0',
            'hurdle_rate': '5.0',
            'catch_up': 'Yes',
            'gp_commitment': '',
            'fund_size': '250000000',
            'notes': 'Semi-liquid structure'
        }
    ]

    for benchmark in fee_benchmarks:
        benchmarks.append(benchmark)

    intel._save_csv(intel.fee_benchmarks_file, benchmarks)
    print(f"✓ Added {len(fee_benchmarks)} fee benchmarks")

    # LP Overlap Data
    print("\n👥 Adding LP overlap data...")

    lp_overlaps = intel._load_csv(intel.lp_overlap_file)

    lp_data = [
        {
            'lp_name': 'University of California',
            'lp_type': 'Endowment',
            'our_investor': 'No',
            'competitor_investors': 'Hamilton Lane,Vintage',
            'total_vc_allocation': '2000000000',
            'allocation_to_fofs': '500000000',
            'strategy_preference': 'Top-tier established managers',
            'decision_maker': 'CIO Office',
            'last_contact': '2025-12-01',
            'notes': 'Large endowment, competitive access'
        },
        {
            'lp_name': 'Massachusetts Pension Fund',
            'lp_type': 'Pension',
            'our_investor': 'Yes',
            'competitor_investors': 'Hamilton Lane',
            'total_vc_allocation': '1500000000',
            'allocation_to_fofs': '300000000',
            'strategy_preference': 'Diversified VC exposure',
            'decision_maker': 'Investment Committee',
            'last_contact': '2026-01-15',
            'notes': 'Current investor, room for more'
        },
        {
            'lp_name': 'Fidelity Strategic Advisers',
            'lp_type': 'Asset Manager',
            'our_investor': 'No',
            'competitor_investors': 'Industry Ventures,Hamilton Lane',
            'total_vc_allocation': '5000000000',
            'allocation_to_fofs': '1000000000',
            'strategy_preference': 'Scale and liquidity',
            'decision_maker': 'Alternative Investments',
            'last_contact': '2025-11-20',
            'notes': 'Large allocator, prefers established'
        },
        {
            'lp_name': 'Walton Family Office',
            'lp_type': 'Family Office',
            'our_investor': 'Yes',
            'competitor_investors': '',
            'total_vc_allocation': '500000000',
            'allocation_to_fofs': '100000000',
            'strategy_preference': 'Emerging managers',
            'decision_maker': 'Family CIO',
            'last_contact': '2026-02-01',
            'notes': 'Exclusive, mission-aligned'
        },
        {
            'lp_name': 'Princeton Endowment',
            'lp_type': 'Endowment',
            'our_investor': 'No',
            'competitor_investors': 'Vintage,Industry Ventures',
            'total_vc_allocation': '3000000000',
            'allocation_to_fofs': '400000000',
            'strategy_preference': 'Top quartile only',
            'decision_maker': 'Investment Office',
            'last_contact': '2025-10-10',
            'notes': 'Very selective, high bar'
        }
    ]

    for lp in lp_data:
        lp_overlaps.append(lp)

    intel._save_csv(intel.lp_overlap_file, lp_overlaps)
    print(f"✓ Added {len(lp_data)} LP overlap records")

    # Market Data
    print("\n📈 Adding market data...")

    market_metrics = [
        ('VC Fundraising (Quarterly)', 50000000000, 'Pitchbook'),
        ('Fund-of-Funds Fundraising (Quarterly)', 3000000000, 'Pitchbook'),
        ('Emerging Manager Fundraising', 12000000000, 'Pitchbook'),
        ('Average VC Fund Size', 200000000, 'Pitchbook'),
        ('Number of New VC Funds', 350, 'NVCA'),
        ('VC-Backed Exits (Quarterly)', 150, 'NVCA'),
        ('Median Seed Round Size', 3500000, 'Crunchbase'),
        ('Median Series A Size', 18000000, 'Crunchbase')
    ]

    for metric, value, source in market_metrics:
        intel.add_market_data(metric, value, source)

    print(f"\n✓ Created demo competitive intelligence data")
    print(f"\nTry these commands:")
    print("  ./scripts/newco_cli.py intel landscape")
    print("  ./scripts/newco_cli.py intel universe")
    print("  ./scripts/newco_cli.py intel fees")
    print("  ./scripts/newco_cli.py intel lp-overlap")

if __name__ == '__main__':
    create_demo_competitive_data()

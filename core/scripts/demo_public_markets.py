#!/usr/bin/env python3
"""
Demo Public Markets Data

Creates sample data for a publicly traded VC fund-of-funds
Ticker: VCFF (hypothetical)
"""

from public_markets import PublicMarketsEngine, InvestorRelations
from regulatory_compliance import RegulatoryComplianceEngine
from datetime import datetime, timedelta
import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


def create_demo_public_market_data():
    """Create sample public market data"""
    pm = PublicMarketsEngine()
    compliance = RegulatoryComplianceEngine()

    print("Creating demo public market data for NEWCO (VCFF)...")
    print()

    # Sample stock prices (last 30 days)
    today = datetime.now()
    base_price = 18.50  # $18.50 per share
    nav_per_share = 20.00  # NAV of $20/share (trading at discount)

    for i in range(30, 0, -1):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        # Simulate some price movement
        price_var = (i % 5 - 2) * 0.15  # Small daily variations
        close_price = base_price + price_var
        volume = 50000 + (i % 3) * 10000

        pm.add_stock_price(
            date=date,
            open_price=close_price - 0.10,
            high=close_price + 0.25,
            low=close_price - 0.20,
            close=close_price,
            volume=volume,
            market_cap=close_price * 10000000,  # 10M shares outstanding
            notes='Trading day'
        )

    print("✓ Added 30 days of stock price data")
    print(f"  Current Price: ${close_price:.2f}")
    print(f"  Market Cap: ${close_price * 10000000:,.0f}")

    # Add NAV data (weekly)
    for i in range(4, 0, -1):
        date = (today - timedelta(days=i*7)).strftime('%Y-%m-%d')
        pm.add_nav_data(
            date=date,
            nav_per_share=nav_per_share,
            total_nav=nav_per_share * 10000000,  # 10M shares
            shares_outstanding=10000000,
            nav_source='Portfolio valuation',
            notes='Based on latest fund NAVs'
        )

    print("✓ Added NAV history")
    print(f"  NAV per Share: ${nav_per_share:.2f}")
    print(f"  Premium/Discount: {((close_price - nav_per_share) / nav_per_share * 100):.1f}%")
    print(f"  Trading at: {'Premium' if close_price > nav_per_share else 'Discount'}")

    # Add comparable vehicles
    comparables = [
        ('PSTH', 'Pershing Square Tontine Holdings', 'SPAC/Permanent Capital', 4000, 4200, -4.8, 'N/A', 'Liquidating', 'Permanent capital vehicle', ''),
        ('HTGC', 'Hercules Capital', 'BDC - Venture Lending', 1500, 1550, -3.2, 1.75, 'Quarterly', 'Venture debt BDC', ''),
        ('MAIN', 'Main Street Capital', 'BDC - Private Equity', 3200, 3100, +3.2, 2.25, 'Monthly', 'Lower middle market BDC', ''),
        ('TPVG', 'TriplePoint Venture Growth', 'BDC - Venture Lending', 800, 850, -5.9, 2.10, 'Quarterly', 'Venture debt', ''),
        ('3IN', '3i Group (LSE)', 'Listed PE', 15000, 14500, +3.4, 1.20, 'Semi-annual', 'UK listed PE', 'LSE listed'),
        ('PTMN', 'Portman Ridge Finance', 'BDC', 250, 275, -9.1, 3.50, 'Quarterly', 'Opportunistic credit', ''),
        ('VCFND', 'Vintage Capital Fund (hypothetical)', 'VC Fund-of-Funds', 500, 550, -9.1, 1.50, 'Quarterly', 'Similar strategy', 'Hypothetical'),
    ]

    comparables_file = DATA_DIR / "public_comparables.csv"
    with open(comparables_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ticker', 'name', 'type', 'market_cap', 'nav', 'premium_discount', 'expense_ratio', 'liquidity_terms', 'strategy', 'notes'])
        writer.writerows(comparables)

    print("✓ Added 7 comparable public vehicles")

    # Add investor base
    investors = [
        ('1', 'Vanguard Group', 'Institutional', 1250000, 12.5, 'Institutional', '', '2024-01-15', 19.50, 'Index fund holdings'),
        ('2', 'BlackRock', 'Institutional', 980000, 9.8, 'Institutional', '', '2024-02-01', 18.75, 'Active + index'),
        ('3', 'State Street', 'Institutional', 650000, 6.5, 'Institutional', '', '2024-01-20', 19.25, 'Index holdings'),
        ('4', 'Wellington Management', 'Institutional', 420000, 4.2, 'Institutional', '', '2024-03-10', 18.50, 'Active manager'),
        ('5', 'Retail Shareholders', 'Retail', 3200000, 32.0, 'Retail', '', 'Various', 18.80, 'Individual investors'),
        ('6', 'Management (CEO, CFO)', 'Insiders', 850000, 8.5, 'Insiders', '', '2023-06-01', 17.00, 'Founder shares + options'),
        ('7', 'Board of Directors', 'Insiders', 180000, 1.8, 'Insiders', '', '2023-06-01', 17.00, 'Board compensation'),
        ('8', 'Strategic LP (CalPERS)', 'Strategic', 450000, 4.5, 'Strategic', '3', '2024-01-15', 19.00, 'Also invests in fund'),
        ('9', 'Strategic LP (Yale Endowment)', 'Strategic', 320000, 3.2, 'Strategic', '5', '2024-02-20', 18.90, 'Also LP in fund'),
        ('10', 'Activist Fund (Saba Capital)', 'Activists', 280000, 2.8, 'Activists', '', '2024-11-15', 17.50, 'Discount arbitrage'),
    ]

    investor_file = DATA_DIR / "investor_base.csv"
    with open(investor_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['investor_id', 'name', 'type', 'shares', 'percent_ownership', 'classification', 'contact_id', 'date_acquired', 'cost_basis', 'notes'])
        writer.writerows(investors)

    print("✓ Added investor base (10M shares across 10 holders)")

    # Add blackout period for upcoming earnings
    earnings_date = today + timedelta(days=14)
    blackout_start = (earnings_date - timedelta(days=14)).strftime('%Y-%m-%d')
    blackout_end = (earnings_date + timedelta(days=2)).strftime('%Y-%m-%d')

    compliance.add_blackout_period(
        start_date=blackout_start,
        end_date=blackout_end,
        reason='Q1 Earnings Blackout',
        affected_persons='Officers, Directors, 10%+ shareholders'
    )

    print("\n✓ Demo data complete!")
    print("\nTry these commands:")
    print("  ./scripts/newco_cli.py public show")
    print("  ./scripts/newco_cli.py public comparables")
    print("  ./scripts/newco_cli.py public investors")
    print("  ./scripts/newco_cli.py compliance status")


if __name__ == '__main__':
    create_demo_public_market_data()

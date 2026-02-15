#!/usr/bin/env python3
"""
Public Markets Integration for Publicly Traded VC Fund-of-Funds

Handles:
- Stock price tracking and analysis
- NAV (Net Asset Value) calculation
- Premium/discount to NAV monitoring
- Public comparables analysis
- Market sentiment tracking
- Liquidity and trading analysis
- Institutional vs retail investor tracking
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import json

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


class PublicMarketsEngine:
    """Public markets tools for traded VC fund-of-funds"""

    def __init__(self):
        self.stock_prices_file = DATA_DIR / "stock_prices.csv"
        self.nav_history_file = DATA_DIR / "nav_history.csv"
        self.comparables_file = DATA_DIR / "public_comparables.csv"
        self.investor_base_file = DATA_DIR / "investor_base.csv"
        self.disclosures_file = DATA_DIR / "public_disclosures.csv"

        self._initialize_files()

    def _initialize_files(self):
        """Initialize CSV files if they don't exist"""
        if not self.stock_prices_file.exists():
            self.stock_prices_file.write_text(
                "date,open,high,low,close,volume,market_cap,notes\n"
            )

        if not self.nav_history_file.exists():
            self.nav_history_file.write_text(
                "date,nav_per_share,total_nav,shares_outstanding,premium_discount,nav_source,notes\n"
            )

        if not self.comparables_file.exists():
            self.comparables_file.write_text(
                "ticker,name,type,market_cap,nav,premium_discount,expense_ratio,liquidity_terms,strategy,notes\n"
            )

        if not self.investor_base_file.exists():
            self.investor_base_file.write_text(
                "investor_id,name,type,shares,percent_ownership,classification,contact_id,date_acquired,cost_basis,notes\n"
            )

        if not self.disclosures_file.exists():
            self.disclosures_file.write_text(
                "date,disclosure_type,title,content,required_by,filed,public_url,notes\n"
            )

    def add_stock_price(self, date, open_price, high, low, close, volume, market_cap, notes=''):
        """Record daily stock price data"""
        prices = self.load_stock_prices()

        price_data = {
            'date': date,
            'open': str(open_price),
            'high': str(high),
            'low': str(low),
            'close': str(close),
            'volume': str(volume),
            'market_cap': str(market_cap),
            'notes': notes
        }

        prices.append(price_data)
        self._save_csv(self.stock_prices_file, prices)

        return True

    def add_nav_data(self, date, nav_per_share, total_nav, shares_outstanding, nav_source='calculation', notes=''):
        """Record NAV (Net Asset Value) data"""
        nav_history = self.load_nav_history()

        # Calculate premium/discount to NAV
        stock_price = self.get_stock_price(date)
        if stock_price:
            premium_discount = ((float(stock_price['close']) - float(nav_per_share)) / float(nav_per_share)) * 100
        else:
            premium_discount = 0

        nav_data = {
            'date': date,
            'nav_per_share': str(nav_per_share),
            'total_nav': str(total_nav),
            'shares_outstanding': str(shares_outstanding),
            'premium_discount': f"{premium_discount:.2f}",
            'nav_source': nav_source,
            'notes': notes
        }

        nav_history.append(nav_data)
        self._save_csv(self.nav_history_file, nav_history)

        return premium_discount

    def load_stock_prices(self):
        """Load stock price history"""
        return self._load_csv(self.stock_prices_file)

    def load_nav_history(self):
        """Load NAV history"""
        return self._load_csv(self.nav_history_file)

    def load_comparables(self):
        """Load comparable public vehicles"""
        return self._load_csv(self.comparables_file)

    def load_investor_base(self):
        """Load public investor base"""
        return self._load_csv(self.investor_base_file)

    def get_stock_price(self, date):
        """Get stock price for specific date"""
        prices = self.load_stock_prices()
        for price in prices:
            if price['date'] == date:
                return price
        return None

    def get_current_nav(self):
        """Get most recent NAV"""
        nav_history = self.load_nav_history()
        if nav_history:
            return nav_history[-1]
        return None

    def calculate_premium_discount(self):
        """
        Calculate current premium/discount to NAV

        Key metric for publicly traded funds:
        - Premium (positive): Stock trades ABOVE NAV (market optimism)
        - Discount (negative): Stock trades BELOW NAV (market pessimism)

        Typical ranges:
        - CEFs: -10% to +5%
        - BDCs: -20% to +10%
        - Interval funds: -5% to +5%
        """
        prices = self.load_stock_prices()
        nav_history = self.load_nav_history()

        if not prices or not nav_history:
            return None

        latest_price = prices[-1]
        latest_nav = nav_history[-1]

        stock_price = float(latest_price['close'])
        nav_per_share = float(latest_nav['nav_per_share'])

        premium_discount = ((stock_price - nav_per_share) / nav_per_share) * 100

        return {
            'date': latest_price['date'],
            'stock_price': stock_price,
            'nav_per_share': nav_per_share,
            'premium_discount': premium_discount,
            'interpretation': self._interpret_premium_discount(premium_discount)
        }

    def _interpret_premium_discount(self, pct):
        """Interpret premium/discount percentage"""
        if pct > 15:
            return "Significant premium - market very bullish on strategy"
        elif pct > 5:
            return "Modest premium - positive market sentiment"
        elif pct > -5:
            return "Trading near NAV - fair value"
        elif pct > -15:
            return "Modest discount - market skepticism or liquidity concerns"
        else:
            return "Significant discount - market very bearish or major liquidity issues"

    def analyze_comparables(self):
        """
        Analyze comparable public VC vehicles

        Examples:
        - Permanent capital vehicles (e.g., Pershing Square Holdings)
        - BDCs focused on VC (e.g., Hercules Capital)
        - Listed PE funds (e.g., 3i Group, Partners Group)
        - Interval funds with VC exposure
        """
        comparables = self.load_comparables()

        if not comparables:
            return {
                'message': 'No comparables data. Add with: add_comparable()',
                'comparables': []
            }

        # Calculate statistics
        premiums = []
        for comp in comparables:
            if comp.get('premium_discount'):
                try:
                    premiums.append(float(comp['premium_discount']))
                except:
                    pass

        analysis = {
            'total_comps': len(comparables),
            'avg_premium_discount': sum(premiums) / len(premiums) if premiums else 0,
            'median_premium_discount': sorted(premiums)[len(premiums)//2] if premiums else 0,
            'comparables': comparables
        }

        return analysis

    def track_investor_base(self):
        """
        Track public investor base composition

        Categories:
        - Institutional (mutual funds, pension funds, endowments)
        - Retail (individual investors)
        - Strategic (LPs who also invest in fund)
        - Insiders (management, board)
        - Activists (hedge funds, activist investors)
        """
        investors = self.load_investor_base()

        composition = {
            'Institutional': {'count': 0, 'shares': 0, 'percent': 0},
            'Retail': {'count': 0, 'shares': 0, 'percent': 0},
            'Strategic': {'count': 0, 'shares': 0, 'percent': 0},
            'Insiders': {'count': 0, 'shares': 0, 'percent': 0},
            'Activists': {'count': 0, 'shares': 0, 'percent': 0}
        }

        total_shares = 0

        for investor in investors:
            inv_type = investor.get('classification', 'Retail')
            shares = int(investor.get('shares', 0))

            if inv_type in composition:
                composition[inv_type]['count'] += 1
                composition[inv_type]['shares'] += shares
                total_shares += shares

        # Calculate percentages
        for inv_type in composition:
            if total_shares > 0:
                composition[inv_type]['percent'] = (composition[inv_type]['shares'] / total_shares) * 100

        return {
            'total_shareholders': len(investors),
            'total_shares': total_shares,
            'composition': composition,
            'concentration': self._calculate_concentration(investors)
        }

    def _calculate_concentration(self, investors):
        """Calculate ownership concentration (top 10 holders)"""
        sorted_investors = sorted(investors, key=lambda x: int(x.get('shares', 0)), reverse=True)
        top_10_shares = sum(int(inv.get('shares', 0)) for inv in sorted_investors[:10])
        total_shares = sum(int(inv.get('shares', 0)) for inv in investors)

        if total_shares > 0:
            concentration = (top_10_shares / total_shares) * 100
        else:
            concentration = 0

        return {
            'top_10_ownership': concentration,
            'top_holders': sorted_investors[:10]
        }

    def calculate_liquidity_metrics(self):
        """
        Calculate liquidity metrics for the stock

        Key metrics:
        - Average daily volume
        - Volume as % of float
        - Bid-ask spread (proxy via volatility)
        - Days to liquidate (for institutional positions)
        """
        prices = self.load_stock_prices()

        if len(prices) < 20:
            return {'message': 'Insufficient data (need 20+ days)'}

        recent = prices[-20:]  # Last 20 days

        volumes = [int(p['volume']) for p in recent]
        avg_volume = sum(volumes) / len(volumes)

        # Calculate volatility (as proxy for liquidity)
        closes = [float(p['close']) for p in recent]
        returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))]
        volatility = (sum(r**2 for r in returns) / len(returns)) ** 0.5 * 100

        return {
            'avg_daily_volume': avg_volume,
            'avg_daily_value': avg_volume * closes[-1],
            'volatility_20d': volatility,
            'liquidity_score': self._calculate_liquidity_score(avg_volume, volatility)
        }

    def _calculate_liquidity_score(self, volume, volatility):
        """Calculate liquidity score (0-100)"""
        # Higher volume = more liquid
        # Lower volatility = more liquid
        volume_score = min(volume / 100000, 1) * 50  # Normalize to 50 points
        volatility_score = max(0, (5 - volatility) / 5) * 50  # Lower vol = higher score

        return volume_score + volatility_score

    def generate_public_market_report(self):
        """Generate comprehensive public market report"""
        print("\n" + "="*80)
        print("PUBLIC MARKET ANALYSIS - NEWCO (Publicly Traded VC Fund-of-Funds)")
        print("="*80)

        # Current position
        prem_disc = self.calculate_premium_discount()
        if prem_disc:
            print(f"\n📊 CURRENT TRADING")
            print(f"  Stock Price:        ${prem_disc['stock_price']:.2f}")
            print(f"  NAV per Share:      ${prem_disc['nav_per_share']:.2f}")
            print(f"  Premium/Discount:   {prem_disc['premium_discount']:+.2f}%")
            print(f"  Interpretation:     {prem_disc['interpretation']}")
        else:
            print("\n⚠ No pricing data available")

        # Comparables
        print(f"\n📈 COMPARABLE VEHICLES")
        comps = self.analyze_comparables()
        if comps.get('comparables'):
            print(f"  Peer Group Size:    {comps['total_comps']}")
            print(f"  Avg Premium/Disc:   {comps['avg_premium_discount']:+.2f}%")
            print(f"  Median Premium/Disc: {comps['median_premium_discount']:+.2f}%")
            print(f"\n  Top Comparables:")
            for comp in comps['comparables'][:5]:
                print(f"    • {comp['ticker']:<6} {comp['name']:<30} {comp.get('premium_discount', 'N/A'):>8}")
        else:
            print("  No comparables data. Add peers for benchmarking.")

        # Investor base
        print(f"\n👥 INVESTOR BASE")
        investor_data = self.track_investor_base()
        print(f"  Total Shareholders: {investor_data['total_shareholders']}")
        print(f"  Total Shares:       {investor_data['total_shares']:,}")
        print(f"\n  Composition:")
        for inv_type, data in investor_data['composition'].items():
            if data['percent'] > 0:
                print(f"    • {inv_type:<15} {data['percent']:>5.1f}%  ({data['count']} holders)")
        print(f"\n  Concentration:")
        print(f"    Top 10 holders:    {investor_data['concentration']['top_10_ownership']:.1f}%")

        # Liquidity
        print(f"\n💧 LIQUIDITY METRICS")
        liquidity = self.calculate_liquidity_metrics()
        if 'avg_daily_volume' in liquidity:
            print(f"  Avg Daily Volume:   {liquidity['avg_daily_volume']:,.0f} shares")
            print(f"  Avg Daily Value:    ${liquidity['avg_daily_value']:,.0f}")
            print(f"  20-Day Volatility:  {liquidity['volatility_20d']:.2f}%")
            print(f"  Liquidity Score:    {liquidity['liquidity_score']:.0f}/100")
        else:
            print("  Insufficient data for liquidity analysis")

        print("\n" + "="*80 + "\n")

    def identify_disclosure_requirements(self):
        """
        Identify public disclosure requirements

        For publicly traded VC fund-of-funds:
        - Quarterly earnings (10-Q)
        - Annual reports (10-K)
        - Material events (8-K)
        - Proxy statements
        - Section 16 filings (insider trading)
        - NAV disclosures (weekly/monthly)
        - Portfolio holdings (quarterly)
        - Investment restrictions compliance
        """
        requirements = [
            {
                'type': '10-Q',
                'frequency': 'Quarterly',
                'deadline': '45 days after quarter end',
                'description': 'Quarterly financial statements, MD&A, portfolio updates'
            },
            {
                'type': '10-K',
                'frequency': 'Annual',
                'deadline': '90 days after year end',
                'description': 'Annual audited financials, full portfolio disclosure, risk factors'
            },
            {
                'type': '8-K',
                'frequency': 'As needed',
                'deadline': '4 business days after event',
                'description': 'Material events: fund commitments, management changes, etc.'
            },
            {
                'type': 'DEF 14A (Proxy)',
                'frequency': 'Annual',
                'deadline': 'Before annual meeting',
                'description': 'Board elections, compensation, shareholder proposals'
            },
            {
                'type': 'NAV Disclosure',
                'frequency': 'Weekly/Monthly',
                'deadline': '5 business days',
                'description': 'Net Asset Value per share calculation'
            },
            {
                'type': 'Form 13F',
                'frequency': 'Quarterly',
                'deadline': '45 days after quarter',
                'description': 'Portfolio holdings > $100M (if applicable)'
            },
            {
                'type': 'Press Releases',
                'frequency': 'Quarterly',
                'deadline': 'Day of earnings',
                'description': 'Earnings announcements, portfolio updates, material news'
            }
        ]

        return requirements

    def calculate_nav(self, fund_commitments, cash_reserves, public_holdings, fund_expenses):
        """
        Calculate NAV for VC fund-of-funds

        Components:
        1. Fund investments (at fair value)
        2. Cash and cash equivalents
        3. Public securities (mark-to-market)
        4. Less: Accrued expenses and liabilities

        NAV = (Assets - Liabilities) / Shares Outstanding

        Valuation challenges:
        - Private fund stakes (use last reported NAV, typically quarterly)
        - Timing differences (fund NAVs lag)
        - Illiquidity discounts (may apply to large positions)
        """
        total_assets = fund_commitments + cash_reserves + public_holdings
        total_liabilities = fund_expenses

        nav = total_assets - total_liabilities

        return {
            'total_assets': total_assets,
            'fund_commitments': fund_commitments,
            'cash_reserves': cash_reserves,
            'public_holdings': public_holdings,
            'total_liabilities': total_liabilities,
            'net_asset_value': nav,
            'calculation_date': datetime.now().strftime('%Y-%m-%d'),
            'notes': 'Based on latest fund NAVs (may lag 1-3 months)'
        }

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


class InvestorRelations:
    """
    Investor Relations for Public + Private Investors

    Dual constituency:
    1. Public shareholders (retail + institutional)
    2. Private LPs (direct fund investors)
    """

    def __init__(self):
        self.ir_contacts_file = DATA_DIR / "ir_contacts.csv"
        self.ir_calendar_file = DATA_DIR / "ir_calendar.csv"
        self.shareholder_comms_file = DATA_DIR / "shareholder_comms.csv"

        self._initialize_files()

    def _initialize_files(self):
        """Initialize IR files"""
        if not self.ir_contacts_file.exists():
            self.ir_contacts_file.write_text(
                "contact_id,name,firm,type,position,coverage,last_contact,notes\n"
            )

        if not self.ir_calendar_file.exists():
            self.ir_calendar_file.write_text(
                "date,event_type,description,participants,location,materials,status\n"
            )

        if not self.shareholder_comms_file.exists():
            self.shareholder_comms_file.write_text(
                "date,communication_type,audience,subject,summary,link,response_rate\n"
            )

    def schedule_earnings_call(self, date, quarter, participants):
        """Schedule quarterly earnings call"""
        # Load calendar
        calendar = []
        if self.ir_calendar_file.exists():
            with open(self.ir_calendar_file, 'r') as f:
                reader = csv.DictReader(f)
                calendar = list(reader)

        event = {
            'date': date,
            'event_type': 'Earnings Call',
            'description': f'Q{quarter} Earnings Call',
            'participants': participants,
            'location': 'Conference Call / Webcast',
            'materials': 'Earnings release, slides, script',
            'status': 'Scheduled'
        }

        calendar.append(event)

        # Save
        with open(self.ir_calendar_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=event.keys())
            writer.writeheader()
            writer.writerows(calendar)

        return event

    def generate_ir_calendar(self):
        """Generate IR events calendar"""
        print("\n" + "="*70)
        print("INVESTOR RELATIONS CALENDAR")
        print("="*70)

        calendar = []
        if self.ir_calendar_file.exists():
            with open(self.ir_calendar_file, 'r') as f:
                reader = csv.DictReader(f)
                calendar = list(reader)

        if not calendar:
            print("\nNo events scheduled")
            print("\nTypical IR Calendar for Public VC Fund:")
            print("  • Quarterly Earnings Calls (4x per year)")
            print("  • Annual Shareholder Meeting")
            print("  • Investor conferences (2-4x per year)")
            print("  • Non-deal roadshows (as needed)")
            print("  • Analyst days (1x per year)")
        else:
            for event in calendar:
                print(f"\n{event['date']}: {event['event_type']}")
                print(f"  {event['description']}")
                print(f"  Status: {event['status']}")

        print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    pm = PublicMarketsEngine()
    pm.generate_public_market_report()

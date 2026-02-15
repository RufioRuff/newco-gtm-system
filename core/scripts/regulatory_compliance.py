#!/usr/bin/env python3
"""
Regulatory Compliance Tracker for Publicly Traded VC Fund-of-Funds

Tracks:
- SEC filing deadlines
- Trading blackout periods
- Insider trading restrictions (Section 16)
- Material non-public information (MNPI) policies
- Investment restrictions and covenants
- Fair value pricing requirements
- Disclosure obligations
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


class RegulatoryComplianceEngine:
    """Regulatory compliance tracking"""

    def __init__(self):
        self.filings_file = DATA_DIR / "sec_filings.csv"
        self.blackout_periods_file = DATA_DIR / "blackout_periods.csv"
        self.insider_trades_file = DATA_DIR / "insider_trades.csv"
        self.compliance_calendar_file = DATA_DIR / "compliance_calendar.csv"

        self._initialize_files()

    def _initialize_files(self):
        """Initialize compliance tracking files"""
        if not self.filings_file.exists():
            self.filings_file.write_text(
                "filing_type,period,due_date,filed_date,status,accession_number,notes\n"
            )

        if not self.blackout_periods_file.exists():
            self.blackout_periods_file.write_text(
                "start_date,end_date,reason,affected_persons,status,notes\n"
            )

        if not self.insider_trades_file.exists():
            self.insider_trades_file.write_text(
                "trade_date,insider_name,transaction_type,shares,price,form_type,filed_date,notes\n"
            )

        if not self.compliance_calendar_file.exists():
            self.compliance_calendar_file.write_text(
                "date,requirement,description,responsible_party,status,notes\n"
            )

    def generate_quarterly_calendar(self, quarter, year):
        """
        Generate compliance calendar for a quarter

        Q1: Jan-Mar (Due: May 15)
        Q2: Apr-Jun (Due: Aug 14)
        Q3: Jul-Sep (Due: Nov 14)
        Q4: Oct-Dec (Due: Mar 15 + 10-K on Mar 31)
        """
        quarter_end = {
            1: f'{year}-03-31',
            2: f'{year}-06-30',
            3: f'{year}-09-30',
            4: f'{year}-12-31'
        }[quarter]

        # 10-Q due 45 days after quarter end
        quarter_end_dt = datetime.strptime(quarter_end, '%Y-%m-%d')
        tenq_due = quarter_end_dt + timedelta(days=45)

        # 10-K due 90 days after year end (Q4 only)
        tenk_due = None
        if quarter == 4:
            tenk_due = quarter_end_dt + timedelta(days=90)

        # Earnings call typically 1-2 days after filing
        earnings_call = tenq_due + timedelta(days=1)

        # Blackout period: 2 weeks before earnings through 2 days after
        blackout_start = earnings_call - timedelta(days=16)
        blackout_end = earnings_call + timedelta(days=2)

        calendar = {
            'quarter': f'Q{quarter} {year}',
            'quarter_end': quarter_end,
            '10q_due': tenq_due.strftime('%Y-%m-%d') if quarter != 4 else 'N/A',
            '10k_due': tenk_due.strftime('%Y-%m-%d') if quarter == 4 else 'N/A',
            'earnings_call': earnings_call.strftime('%Y-%m-%d'),
            'blackout_start': blackout_start.strftime('%Y-%m-%d'),
            'blackout_end': blackout_end.strftime('%Y-%m-%d'),
            'nav_disclosure': f'{quarter_end} (within 5 business days)',
            'portfolio_disclosure': f'{quarter_end} (in 10-Q/K)',
            'key_dates': [
                {'date': blackout_start.strftime('%Y-%m-%d'), 'event': 'Trading Blackout Begins'},
                {'date': quarter_end, 'event': 'Quarter End - Close Books'},
                {'date': (quarter_end_dt + timedelta(days=5)).strftime('%Y-%m-%d'), 'event': 'NAV Disclosure Due'},
                {'date': tenq_due.strftime('%Y-%m-%d'), 'event': '10-Q Filing Due' if quarter != 4 else '10-Q Filed'},
                {'date': tenk_due.strftime('%Y-%m-%d') if quarter == 4 else 'N/A', 'event': '10-K Filing Due'},
                {'date': earnings_call.strftime('%Y-%m-%d'), 'event': 'Earnings Call'},
                {'date': blackout_end.strftime('%Y-%m-%d'), 'event': 'Trading Blackout Ends'}
            ]
        }

        return calendar

    def check_blackout_status(self, date=None):
        """
        Check if currently in trading blackout period

        Blackout periods:
        1. Quarterly blackout: ~2 weeks before earnings through 2 days after
        2. Ad-hoc blackout: Material non-public information
        3. Window period: Only X days per quarter when insiders can trade
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        blackouts = []
        if self.blackout_periods_file.exists():
            with open(self.blackout_periods_file, 'r') as f:
                reader = csv.DictReader(f)
                for period in reader:
                    if period['start_date'] <= date <= period['end_date']:
                        blackouts.append(period)

        if blackouts:
            return {
                'status': 'BLACKOUT',
                'can_trade': False,
                'reason': ', '.join(b['reason'] for b in blackouts),
                'end_date': max(b['end_date'] for b in blackouts),
                'affected_persons': blackouts[0]['affected_persons']
            }
        else:
            return {
                'status': 'OPEN WINDOW',
                'can_trade': True,
                'reason': 'No active blackout periods',
                'end_date': None,
                'affected_persons': None
            }

    def get_insider_trading_requirements(self):
        """
        Get Section 16 insider trading requirements

        Who is an "insider":
        - Officers (CEO, CFO, etc.)
        - Directors
        - 10%+ shareholders

        Requirements:
        - Form 3: Initial statement of beneficial ownership
        - Form 4: Changes in ownership (within 2 business days)
        - Form 5: Annual statement (within 45 days of fiscal year end)
        - Section 16(b): Short-swing profit rule (6 months)
        """
        requirements = {
            'Form 3': {
                'description': 'Initial Statement of Beneficial Ownership',
                'deadline': 'Within 10 days of becoming insider',
                'who': 'New officers, directors, 10%+ shareholders'
            },
            'Form 4': {
                'description': 'Statement of Changes in Beneficial Ownership',
                'deadline': 'Within 2 business days of transaction',
                'who': 'All insiders for each transaction'
            },
            'Form 5': {
                'description': 'Annual Statement of Beneficial Ownership',
                'deadline': 'Within 45 days of fiscal year end',
                'who': 'All insiders (for small/exempt transactions)'
            },
            'Section 16(b) Rule': {
                'description': 'Short-swing profit recapture',
                'deadline': 'Automatic',
                'who': 'Profits from buy/sell within 6 months must be returned'
            }
        }

        return requirements

    def calculate_fair_value_requirements(self):
        """
        Fair value accounting requirements for fund investments

        ASC 820 (Fair Value Measurement):
        - Level 1: Quoted prices (public stocks)
        - Level 2: Observable inputs (recent transactions)
        - Level 3: Unobservable inputs (private funds)

        For VC fund-of-funds:
        - Most holdings are Level 3 (private fund stakes)
        - Rely on fund manager NAVs (quarterly lag)
        - May need valuation adjustments for:
          - Material events since last NAV
          - Liquidity discounts (large positions)
          - Cross-checks (portfolio company valuations)
        """
        guidance = {
            'level_1': {
                'description': 'Quoted prices in active markets',
                'application': 'Public stock positions',
                'frequency': 'Daily mark-to-market',
                'reliability': 'High'
            },
            'level_2': {
                'description': 'Observable inputs (recent transactions)',
                'application': 'Recent fund sales, secondary market trades',
                'frequency': 'Updated when observable',
                'reliability': 'Medium-High'
            },
            'level_3': {
                'description': 'Unobservable inputs (models)',
                'application': 'Private fund stakes (majority of portfolio)',
                'frequency': 'Quarterly (based on fund NAVs)',
                'reliability': 'Medium (1-3 month lag)',
                'adjustments': [
                    'Material subsequent events',
                    'Liquidity discounts (if applicable)',
                    'Cross-check portfolio company valuations',
                    'Manager track record and reputation'
                ]
            }
        }

        return guidance

    def generate_compliance_dashboard(self):
        """Generate compliance status dashboard"""
        print("\n" + "="*80)
        print("REGULATORY COMPLIANCE DASHBOARD")
        print("="*80)

        # Blackout status
        print("\n🚦 TRADING STATUS")
        blackout = self.check_blackout_status()
        status_icon = "🔴" if blackout['status'] == 'BLACKOUT' else "🟢"
        print(f"  {status_icon} Status: {blackout['status']}")
        print(f"  Can Trade: {'No' if not blackout['can_trade'] else 'Yes'}")
        if not blackout['can_trade']:
            print(f"  Reason: {blackout['reason']}")
            print(f"  Ends: {blackout['end_date']}")

        # Upcoming deadlines
        print("\n📅 UPCOMING DEADLINES")
        today = datetime.now()
        current_quarter = (today.month - 1) // 3 + 1
        calendar = self.generate_quarterly_calendar(current_quarter, today.year)

        print(f"  Current Period: {calendar['quarter']}")
        print(f"\n  Key Dates:")
        for date_info in calendar['key_dates']:
            if date_info['date'] != 'N/A':
                event_date = datetime.strptime(date_info['date'], '%Y-%m-%d')
                days_until = (event_date - today).days
                if days_until >= 0:
                    print(f"    • {date_info['date']}: {date_info['event']} ({days_until} days)")

        # Insider trading requirements
        print("\n📋 SECTION 16 REQUIREMENTS")
        requirements = self.get_insider_trading_requirements()
        print("  Form 4: File within 2 business days of any trade")
        print("  Form 5: Annual filing within 45 days of year-end")
        print("  16(b) Rule: No buy/sell within 6 months (short-swing)")

        # Fair value requirements
        print("\n💎 FAIR VALUE MEASUREMENT")
        print("  Level 1 (Public): Daily mark-to-market")
        print("  Level 2 (Observable): Update when observable")
        print("  Level 3 (Private): Quarterly (fund NAVs)")
        print("  Note: Most VC fund stakes are Level 3")

        print("\n" + "="*80 + "\n")

    def add_blackout_period(self, start_date, end_date, reason, affected_persons='All insiders'):
        """Add a blackout period"""
        blackouts = []
        if self.blackout_periods_file.exists():
            with open(self.blackout_periods_file, 'r') as f:
                reader = csv.DictReader(f)
                blackouts = list(reader)

        blackout = {
            'start_date': start_date,
            'end_date': end_date,
            'reason': reason,
            'affected_persons': affected_persons,
            'status': 'Active',
            'notes': ''
        }

        blackouts.append(blackout)

        with open(self.blackout_periods_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=blackout.keys())
            writer.writeheader()
            writer.writerows(blackouts)

        print(f"✓ Blackout period added: {start_date} to {end_date}")
        print(f"  Reason: {reason}")
        print(f"  Affected: {affected_persons}")

        return blackout


if __name__ == '__main__':
    compliance = RegulatoryComplianceEngine()
    compliance.generate_compliance_dashboard()

#!/usr/bin/env python3
"""
Risk Management - Portfolio Risk Monitoring & Governance

Monitors concentration risk, correlation, vintage year exposure, and liquidity.
Critical for governance compliance and board reporting.

Key Risks:
1. Concentration Risk - Any single fund/sector/vintage too large
2. Correlation Risk - Funds that overlap in portfolio companies
3. Vintage Year Risk - Over-exposure to bubble or correction years
4. Liquidity Risk - Ability to meet capital calls
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from portfolio_management import PortfolioManager

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


class RiskManager:
    """Portfolio risk monitoring and governance compliance"""

    # Risk limits from investment policy
    LIMITS = {
        'single_fund_max': 0.15,      # 15% max in any single fund
        'vintage_year_max': 0.30,     # 30% max in any vintage year
        'sector_max': 0.40,           # 40% max in any sector
        'top_3_funds_max': 0.40,      # 40% max in top 3 funds
        'cash_reserve_min': 0.10,     # 10% min cash reserves
        'min_fund_count': 10          # Minimum 10 fund investments
    }

    def __init__(self):
        self.pm = PortfolioManager()
        self.correlation_file = DATA_DIR / "fund_correlations.csv"
        self.risk_events_file = DATA_DIR / "risk_events.csv"
        self._initialize_files()

    def _initialize_files(self):
        """Initialize risk tracking files"""
        if not self.correlation_file.exists():
            self.correlation_file.write_text(
                "fund_id_1,fund_id_2,shared_companies,overlap_score,notes\n"
            )

        if not self.risk_events_file.exists():
            self.risk_events_file.write_text(
                "event_id,date,risk_type,severity,description,status,resolved_date,notes\n"
            )

    def check_concentration_risk(self):
        """Check portfolio concentration against limits"""
        funds = self.pm._load_csv(self.pm.funds_file)

        if not funds:
            return {
                'status': 'ALERT',
                'message': 'No funds in portfolio',
                'violations': []
            }

        # Calculate total commitment
        total_commitment = sum(float(f['commitment_amount']) for f in funds)

        if total_commitment == 0:
            return {
                'status': 'ALERT',
                'message': 'No capital committed',
                'violations': []
            }

        violations = []
        warnings = []

        # Check 1: Fund count
        fund_count = len(funds)
        if fund_count < self.LIMITS['min_fund_count']:
            violations.append({
                'type': 'MIN_FUND_COUNT',
                'severity': 'HIGH',
                'message': f"Only {fund_count} funds (minimum {self.LIMITS['min_fund_count']})",
                'limit': self.LIMITS['min_fund_count'],
                'actual': fund_count
            })

        # Check 2: Single fund concentration
        for fund in funds:
            fund_pct = float(fund['commitment_amount']) / total_commitment
            if fund_pct > self.LIMITS['single_fund_max']:
                violations.append({
                    'type': 'SINGLE_FUND',
                    'severity': 'HIGH',
                    'message': f"{fund['fund_name']}: {fund_pct:.1%} (max {self.LIMITS['single_fund_max']:.0%})",
                    'fund_name': fund['fund_name'],
                    'limit': self.LIMITS['single_fund_max'],
                    'actual': fund_pct
                })
            elif fund_pct > self.LIMITS['single_fund_max'] * 0.9:
                warnings.append({
                    'type': 'SINGLE_FUND_WARNING',
                    'severity': 'MEDIUM',
                    'message': f"{fund['fund_name']}: {fund_pct:.1%} approaching limit",
                    'fund_name': fund['fund_name'],
                    'limit': self.LIMITS['single_fund_max'],
                    'actual': fund_pct
                })

        # Check 3: Top 3 funds concentration
        sorted_funds = sorted(funds, key=lambda x: float(x['commitment_amount']), reverse=True)
        top_3_total = sum(float(f['commitment_amount']) for f in sorted_funds[:3])
        top_3_pct = top_3_total / total_commitment

        if top_3_pct > self.LIMITS['top_3_funds_max']:
            violations.append({
                'type': 'TOP_3_FUNDS',
                'severity': 'HIGH',
                'message': f"Top 3 funds: {top_3_pct:.1%} (max {self.LIMITS['top_3_funds_max']:.0%})",
                'limit': self.LIMITS['top_3_funds_max'],
                'actual': top_3_pct
            })

        # Check 4: Vintage year concentration
        vintage_totals = defaultdict(float)
        for fund in funds:
            if fund['vintage_year']:
                vintage_totals[fund['vintage_year']] += float(fund['commitment_amount'])

        for vintage, amount in vintage_totals.items():
            vintage_pct = amount / total_commitment
            if vintage_pct > self.LIMITS['vintage_year_max']:
                violations.append({
                    'type': 'VINTAGE_YEAR',
                    'severity': 'HIGH',
                    'message': f"Vintage {vintage}: {vintage_pct:.1%} (max {self.LIMITS['vintage_year_max']:.0%})",
                    'vintage': vintage,
                    'limit': self.LIMITS['vintage_year_max'],
                    'actual': vintage_pct
                })

        # Check 5: Sector concentration
        sector_totals = defaultdict(float)
        for fund in funds:
            if fund['sector_focus']:
                sector_totals[fund['sector_focus']] += float(fund['commitment_amount'])

        for sector, amount in sector_totals.items():
            sector_pct = amount / total_commitment
            if sector_pct > self.LIMITS['sector_max']:
                violations.append({
                    'type': 'SECTOR',
                    'severity': 'MEDIUM',
                    'message': f"{sector}: {sector_pct:.1%} (max {self.LIMITS['sector_max']:.0%})",
                    'sector': sector,
                    'limit': self.LIMITS['sector_max'],
                    'actual': sector_pct
                })

        # Determine overall status
        if violations:
            status = 'VIOLATION'
        elif warnings:
            status = 'WARNING'
        else:
            status = 'COMPLIANT'

        return {
            'status': status,
            'fund_count': fund_count,
            'total_commitment': total_commitment,
            'violations': violations,
            'warnings': warnings,
            'vintage_breakdown': dict(vintage_totals),
            'sector_breakdown': dict(sector_totals)
        }

    def check_liquidity_risk(self):
        """Check ability to meet capital calls"""
        funds = self.pm._load_csv(self.pm.funds_file)

        # Calculate unfunded commitments
        total_unfunded = 0
        for fund in funds:
            commitment = float(fund['commitment_amount'])
            capital_calls = self.pm._load_csv(self.pm.capital_calls_file)
            paid_in = sum(
                float(call['amount'])
                for call in capital_calls
                if call['fund_id'] == fund['fund_id'] and call['status'] == 'Paid'
            )
            total_unfunded += (commitment - paid_in)

        # Forecast capital calls
        forecast = self.pm.forecast_capital_calls(months=12)
        total_forecast_12m = sum(f['amount'] for f in forecast)

        # Assume we need to track cash separately
        # For now, use a simple heuristic: should have 25% of 12m forecast
        required_cash = total_forecast_12m * 0.25

        return {
            'unfunded_commitments': total_unfunded,
            'forecast_12m': total_forecast_12m,
            'required_cash_reserve': required_cash,
            'months_of_coverage': None,  # Would need actual cash balance
            'status': 'MONITOR',  # Would check against actual cash
            'recommendations': [
                f"Maintain ${required_cash:,.0f} cash reserve",
                "Monitor fund deployment pace",
                "Review credit facility if needed"
            ]
        }

    def check_vintage_risk(self):
        """Analyze vintage year exposure"""
        funds = self.pm._load_csv(self.pm.funds_file)

        vintage_analysis = defaultdict(lambda: {
            'commitment': 0,
            'count': 0,
            'funds': []
        })

        total_commitment = sum(float(f['commitment_amount']) for f in funds)

        for fund in funds:
            if fund['vintage_year']:
                vintage = fund['vintage_year']
                vintage_analysis[vintage]['commitment'] += float(fund['commitment_amount'])
                vintage_analysis[vintage]['count'] += 1
                vintage_analysis[vintage]['funds'].append(fund['fund_name'])

        # Add risk assessment for each vintage
        # 2020-2021 = peak bubble (high risk)
        # 2023-2024 = correction (opportunity)
        bubble_years = ['2020', '2021']
        correction_years = ['2023', '2024']

        bubble_exposure = sum(
            vintage_analysis[y]['commitment']
            for y in bubble_years
            if y in vintage_analysis
        )
        correction_exposure = sum(
            vintage_analysis[y]['commitment']
            for y in correction_years
            if y in vintage_analysis
        )

        bubble_pct = bubble_exposure / total_commitment if total_commitment > 0 else 0
        correction_pct = correction_exposure / total_commitment if total_commitment > 0 else 0

        # Convert to regular dict for display
        vintage_data = {}
        for vintage, data in sorted(vintage_analysis.items()):
            pct = data['commitment'] / total_commitment if total_commitment > 0 else 0
            risk_level = 'HIGH' if vintage in bubble_years else ('MEDIUM' if vintage in correction_years else 'LOW')

            vintage_data[vintage] = {
                'commitment': data['commitment'],
                'percentage': pct,
                'count': data['count'],
                'funds': data['funds'],
                'risk_level': risk_level
            }

        return {
            'vintage_breakdown': vintage_data,
            'bubble_exposure': bubble_pct,
            'correction_exposure': correction_pct,
            'diversification_score': len(vintage_analysis),  # More vintages = better
            'recommendations': self._generate_vintage_recommendations(vintage_data, bubble_pct)
        }

    def _generate_vintage_recommendations(self, vintage_data, bubble_pct):
        """Generate recommendations based on vintage exposure"""
        recs = []

        if bubble_pct > 0.30:
            recs.append("⚠️  High exposure to 2020-2021 vintages - monitor closely for mark-downs")

        if len(vintage_data) < 3:
            recs.append("📊 Limited vintage diversification - consider expanding across more years")

        if len(vintage_data) >= 4:
            recs.append("✓ Good vintage diversification")

        return recs

    def analyze_correlation_risk(self):
        """Analyze correlation between funds (portfolio company overlap)"""
        # This would require portfolio company data from each fund
        # For now, load any tracked correlations

        correlations = self._load_csv(self.correlation_file)

        # Calculate high overlap pairs
        high_overlap = [
            c for c in correlations
            if float(c.get('overlap_score', 0)) > 0.30
        ]

        return {
            'tracked_correlations': len(correlations),
            'high_overlap_pairs': len(high_overlap),
            'details': high_overlap,
            'status': 'HIGH' if high_overlap else 'LOW',
            'recommendations': [
                "Track portfolio company overlap across funds",
                "Avoid funds with >30% company overlap",
                "Consider syndicate patterns in manager selection"
            ]
        }

    def record_risk_event(self, risk_type, severity, description):
        """Log a risk event"""
        events = self._load_csv(self.risk_events_file)

        event_id = f"RE{len(events) + 1:04d}"

        event = {
            'event_id': event_id,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'risk_type': risk_type,
            'severity': severity,
            'description': description,
            'status': 'Open',
            'resolved_date': '',
            'notes': ''
        }

        events.append(event)
        self._save_csv(self.risk_events_file, events)

        return event_id

    def get_risk_dashboard(self):
        """Generate comprehensive risk dashboard"""
        concentration = self.check_concentration_risk()
        liquidity = self.check_liquidity_risk()
        vintage = self.check_vintage_risk()
        correlation = self.analyze_correlation_risk()

        # Calculate overall risk score
        risk_score = 0
        if concentration['status'] == 'VIOLATION':
            risk_score += 40
        elif concentration['status'] == 'WARNING':
            risk_score += 20

        if liquidity['status'] == 'ALERT':
            risk_score += 30

        if vintage['bubble_exposure'] > 0.30:
            risk_score += 20

        if correlation['status'] == 'HIGH':
            risk_score += 10

        # Risk score: 0-20 = Low, 21-50 = Medium, 51+ = High
        if risk_score <= 20:
            risk_level = 'LOW'
        elif risk_score <= 50:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'HIGH'

        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'concentration': concentration,
            'liquidity': liquidity,
            'vintage': vintage,
            'correlation': correlation,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def show_risk_dashboard(self):
        """Display comprehensive risk dashboard"""
        dashboard = self.get_risk_dashboard()

        print("\n" + "="*80)
        print("PORTFOLIO RISK DASHBOARD")
        print("="*80)

        # Overall risk score
        risk_level = dashboard['risk_level']
        risk_indicator = {
            'LOW': '🟢',
            'MEDIUM': '🟡',
            'HIGH': '🔴'
        }
        print(f"\n{risk_indicator[risk_level]} OVERALL RISK: {risk_level} (Score: {dashboard['risk_score']}/100)")

        # Concentration Risk
        print(f"\n{'='*80}")
        print("1. CONCENTRATION RISK")
        print(f"{'='*80}")

        conc = dashboard['concentration']
        print(f"Status: {conc['status']}")
        print(f"Fund Count: {conc['fund_count']} (minimum {self.LIMITS['min_fund_count']})")

        if conc['violations']:
            print(f"\n⚠️  VIOLATIONS ({len(conc['violations'])}):")
            for v in conc['violations']:
                print(f"  • {v['message']}")

        if conc['warnings']:
            print(f"\n⚡ WARNINGS ({len(conc['warnings'])}):")
            for w in conc['warnings']:
                print(f"  • {w['message']}")

        if not conc['violations'] and not conc['warnings']:
            print("\n✓ All concentration limits compliant")

        # Vintage breakdown
        if conc['vintage_breakdown']:
            print(f"\nVintage Year Exposure:")
            total = conc['total_commitment']
            for vintage, amount in sorted(conc['vintage_breakdown'].items()):
                pct = amount / total if total > 0 else 0
                bar = '█' * int(pct * 40)
                print(f"  {vintage}: {pct:>6.1%} {bar} ${amount:,.0f}")

        # Sector breakdown
        if conc['sector_breakdown']:
            print(f"\nSector Exposure:")
            total = conc['total_commitment']
            for sector, amount in sorted(conc['sector_breakdown'].items(), key=lambda x: -x[1]):
                pct = amount / total if total > 0 else 0
                bar = '█' * int(pct * 40)
                print(f"  {sector:<20}: {pct:>6.1%} {bar}")

        # Vintage Risk
        print(f"\n{'='*80}")
        print("2. VINTAGE YEAR RISK")
        print(f"{'='*80}")

        vintage = dashboard['vintage']
        print(f"Bubble Era (2020-2021): {vintage['bubble_exposure']:.1%}")
        print(f"Correction Era (2023-2024): {vintage['correction_exposure']:.1%}")
        print(f"Vintage Diversification: {vintage['diversification_score']} years")

        if vintage['recommendations']:
            print(f"\nRecommendations:")
            for rec in vintage['recommendations']:
                print(f"  {rec}")

        # Liquidity Risk
        print(f"\n{'='*80}")
        print("3. LIQUIDITY RISK")
        print(f"{'='*80}")

        liq = dashboard['liquidity']
        print(f"Unfunded Commitments: ${liq['unfunded_commitments']:,.0f}")
        print(f"12-Month Forecast: ${liq['forecast_12m']:,.0f}")
        print(f"Recommended Reserve: ${liq['required_cash_reserve']:,.0f}")

        if liq['recommendations']:
            print(f"\nRecommendations:")
            for rec in liq['recommendations']:
                print(f"  • {rec}")

        # Correlation Risk
        print(f"\n{'='*80}")
        print("4. CORRELATION RISK")
        print(f"{'='*80}")

        corr = dashboard['correlation']
        print(f"Status: {corr['status']}")
        print(f"Tracked Correlations: {corr['tracked_correlations']}")
        print(f"High Overlap Pairs: {corr['high_overlap_pairs']}")

        if corr['recommendations']:
            print(f"\nRecommendations:")
            for rec in corr['recommendations']:
                print(f"  • {rec}")

        print(f"\n{'='*80}")
        print(f"Generated: {dashboard['timestamp']}")
        print(f"{'='*80}\n")

    def generate_governance_report(self):
        """Generate governance compliance report for board"""
        dashboard = self.get_risk_dashboard()
        conc = dashboard['concentration']

        # Check all policy requirements
        compliance_checks = []

        # Check 1: Diversification requirements
        compliance_checks.append({
            'requirement': 'Minimum 10 fund investments',
            'status': '✓ PASS' if conc['fund_count'] >= self.LIMITS['min_fund_count'] else '✗ FAIL',
            'actual': f"{conc['fund_count']} funds"
        })

        compliance_checks.append({
            'requirement': 'No single fund > 15%',
            'status': '✓ PASS' if not any(v['type'] == 'SINGLE_FUND' for v in conc['violations']) else '✗ FAIL',
            'actual': 'Compliant' if not any(v['type'] == 'SINGLE_FUND' for v in conc['violations']) else 'Violation'
        })

        compliance_checks.append({
            'requirement': 'No vintage year > 30%',
            'status': '✓ PASS' if not any(v['type'] == 'VINTAGE_YEAR' for v in conc['violations']) else '✗ FAIL',
            'actual': 'Compliant' if not any(v['type'] == 'VINTAGE_YEAR' for v in conc['violations']) else 'Violation'
        })

        compliance_checks.append({
            'requirement': 'No sector > 40%',
            'status': '✓ PASS' if not any(v['type'] == 'SECTOR' for v in conc['violations']) else '✗ FAIL',
            'actual': 'Compliant' if not any(v['type'] == 'SECTOR' for v in conc['violations']) else 'Violation'
        })

        return {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'overall_compliance': 'COMPLIANT' if conc['status'] == 'COMPLIANT' else 'NON-COMPLIANT',
            'checks': compliance_checks,
            'violations': conc['violations'],
            'risk_score': dashboard['risk_score'],
            'risk_level': dashboard['risk_level']
        }

    def show_governance_report(self):
        """Display governance compliance report"""
        report = self.generate_governance_report()

        print("\n" + "="*80)
        print("GOVERNANCE COMPLIANCE REPORT")
        print("="*80)
        print(f"Report Date: {report['report_date']}")
        print(f"Overall Status: {report['overall_compliance']}")
        print(f"Risk Level: {report['risk_level']} (Score: {report['risk_score']}/100)")

        print(f"\n{'='*80}")
        print("INVESTMENT POLICY COMPLIANCE")
        print(f"{'='*80}")

        for check in report['checks']:
            print(f"{check['status']} {check['requirement']}")
            print(f"   Actual: {check['actual']}")

        if report['violations']:
            print(f"\n{'='*80}")
            print(f"⚠️  POLICY VIOLATIONS ({len(report['violations'])})")
            print(f"{'='*80}")
            for v in report['violations']:
                print(f"• [{v['severity']}] {v['message']}")

        print(f"\n{'='*80}\n")

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
    rm = RiskManager()
    rm.show_risk_dashboard()

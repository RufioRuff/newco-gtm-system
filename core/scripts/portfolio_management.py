#!/usr/bin/env python3
"""
Portfolio Management System for VC Fund-of-Funds

Tracks underlying fund investments:
- Fund commitments and capital calls
- NAV and performance metrics (TVPI, DPI, RVPI, IRR)
- Cash flow forecasting
- Portfolio construction analysis
- Risk and concentration monitoring
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import json

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


class PortfolioManager:
    """Manage portfolio of fund investments"""

    def __init__(self):
        self.funds_file = DATA_DIR / "portfolio_funds.csv"
        self.capital_calls_file = DATA_DIR / "capital_calls.csv"
        self.distributions_file = DATA_DIR / "distributions.csv"
        self.fund_navs_file = DATA_DIR / "fund_navs.csv"

        self._initialize_files()

    def _initialize_files(self):
        """Initialize portfolio tracking files"""
        if not self.funds_file.exists():
            self.funds_file.write_text(
                "fund_id,fund_name,manager_name,commitment_amount,commitment_date,vintage_year,"
                "stage_focus,sector_focus,geography,status,manager_contact_id,notes\n"
            )

        if not self.capital_calls_file.exists():
            self.capital_calls_file.write_text(
                "call_id,fund_id,call_date,amount,due_date,paid_date,status,notes\n"
            )

        if not self.distributions_file.exists():
            self.distributions_file.write_text(
                "dist_id,fund_id,dist_date,amount,type,notes\n"
            )

        if not self.fund_navs_file.exists():
            self.fund_navs_file.write_text(
                "nav_id,fund_id,nav_date,nav_value,notes\n"
            )

    def add_fund(self, fund_name, manager_name, commitment, vintage_year,
                 stage_focus='', sector_focus='', geography='US', status='Active', notes=''):
        """Add a fund investment to portfolio"""
        funds = self._load_csv(self.funds_file)

        # Generate fund ID
        fund_id = f"F{len(funds) + 1:03d}"

        fund = {
            'fund_id': fund_id,
            'fund_name': fund_name,
            'manager_name': manager_name,
            'commitment_amount': str(commitment),
            'commitment_date': datetime.now().strftime('%Y-%m-%d'),
            'vintage_year': str(vintage_year),
            'stage_focus': stage_focus,
            'sector_focus': sector_focus,
            'geography': geography,
            'status': status,
            'manager_contact_id': '',
            'notes': notes
        }

        funds.append(fund)
        self._save_csv(self.funds_file, funds)

        print(f"✓ Added fund: {fund_name} ({fund_id})")
        print(f"  Manager: {manager_name}")
        print(f"  Commitment: ${commitment:,.0f}")
        print(f"  Vintage: {vintage_year}")

        return fund_id

    def add_capital_call(self, fund_id, amount, due_date, notes=''):
        """Record a capital call from a fund"""
        calls = self._load_csv(self.capital_calls_file)

        call_id = f"CC{len(calls) + 1:04d}"

        call = {
            'call_id': call_id,
            'fund_id': fund_id,
            'call_date': datetime.now().strftime('%Y-%m-%d'),
            'amount': str(amount),
            'due_date': due_date,
            'paid_date': '',
            'status': 'Pending',
            'notes': notes
        }

        calls.append(call)
        self._save_csv(self.capital_calls_file, calls)

        return call_id

    def add_distribution(self, fund_id, amount, dist_type='Return of Capital', notes=''):
        """Record a distribution from a fund"""
        dists = self._load_csv(self.distributions_file)

        dist_id = f"D{len(dists) + 1:04d}"

        dist = {
            'dist_id': dist_id,
            'fund_id': fund_id,
            'dist_date': datetime.now().strftime('%Y-%m-%d'),
            'amount': str(amount),
            'type': dist_type,
            'notes': notes
        }

        dists.append(dist)
        self._save_csv(self.distributions_file, dists)

        return dist_id

    def add_fund_nav(self, fund_id, nav_value, nav_date=None, notes=''):
        """Update fund NAV"""
        navs = self._load_csv(self.fund_navs_file)

        if nav_date is None:
            nav_date = datetime.now().strftime('%Y-%m-%d')

        nav_id = f"NAV{len(navs) + 1:05d}"

        nav = {
            'nav_id': nav_id,
            'fund_id': fund_id,
            'nav_date': nav_date,
            'nav_value': str(nav_value),
            'notes': notes
        }

        navs.append(nav)
        self._save_csv(self.fund_navs_file, navs)

        return nav_id

    def get_fund_metrics(self, fund_id):
        """
        Calculate key metrics for a fund

        Metrics:
        - TVPI (Total Value / Paid In): Total value created
        - DPI (Distributions / Paid In): Cash returned
        - RVPI (Residual Value / Paid In): Unrealized value remaining
        - IRR: Internal Rate of Return

        Formula: TVPI = DPI + RVPI
        """
        funds = self._load_csv(self.funds_file)
        fund = next((f for f in funds if f['fund_id'] == fund_id), None)

        if not fund:
            return None

        # Get capital calls (paid in capital)
        calls = self._load_csv(self.capital_calls_file)
        fund_calls = [c for c in calls if c['fund_id'] == fund_id and c['status'] == 'Paid']
        paid_in = sum(float(c['amount']) for c in fund_calls)

        # Get distributions
        dists = self._load_csv(self.distributions_file)
        fund_dists = [d for d in dists if d['fund_id'] == fund_id]
        distributions = sum(float(d['amount']) for d in fund_dists)

        # Get current NAV (most recent)
        navs = self._load_csv(self.fund_navs_file)
        fund_navs = [n for n in navs if n['fund_id'] == fund_id]
        if fund_navs:
            fund_navs_sorted = sorted(fund_navs, key=lambda x: x['nav_date'], reverse=True)
            current_nav = float(fund_navs_sorted[0]['nav_value'])
        else:
            current_nav = paid_in  # Default to cost basis if no NAV

        # Calculate metrics
        if paid_in > 0:
            dpi = distributions / paid_in
            rvpi = current_nav / paid_in
            tvpi = dpi + rvpi

            # Simple IRR approximation (need cash flow timing for real IRR)
            # Using holding period return as proxy
            years_held = (datetime.now() - datetime.strptime(fund['commitment_date'], '%Y-%m-%d')).days / 365.25
            if years_held > 0:
                irr_approx = ((distributions + current_nav) / paid_in) ** (1 / years_held) - 1
            else:
                irr_approx = 0
        else:
            dpi = rvpi = tvpi = irr_approx = 0

        return {
            'fund_id': fund_id,
            'fund_name': fund['fund_name'],
            'manager': fund['manager_name'],
            'commitment': float(fund['commitment_amount']),
            'paid_in': paid_in,
            'unfunded': float(fund['commitment_amount']) - paid_in,
            'distributions': distributions,
            'current_nav': current_nav,
            'tvpi': tvpi,
            'dpi': dpi,
            'rvpi': rvpi,
            'irr': irr_approx * 100,  # as percentage
            'vintage_year': fund['vintage_year'],
            'stage': fund['stage_focus'],
            'sector': fund['sector_focus']
        }

    def get_portfolio_summary(self):
        """Get summary of entire portfolio"""
        funds = self._load_csv(self.funds_file)

        summary = {
            'total_funds': len(funds),
            'total_commitment': 0,
            'total_paid_in': 0,
            'total_unfunded': 0,
            'total_distributions': 0,
            'total_nav': 0,
            'portfolio_tvpi': 0,
            'portfolio_dpi': 0,
            'portfolio_rvpi': 0,
            'weighted_irr': 0,
            'funds': []
        }

        for fund in funds:
            metrics = self.get_fund_metrics(fund['fund_id'])
            if metrics:
                summary['total_commitment'] += metrics['commitment']
                summary['total_paid_in'] += metrics['paid_in']
                summary['total_unfunded'] += metrics['unfunded']
                summary['total_distributions'] += metrics['distributions']
                summary['total_nav'] += metrics['current_nav']
                summary['funds'].append(metrics)

        # Portfolio-level metrics
        if summary['total_paid_in'] > 0:
            summary['portfolio_dpi'] = summary['total_distributions'] / summary['total_paid_in']
            summary['portfolio_rvpi'] = summary['total_nav'] / summary['total_paid_in']
            summary['portfolio_tvpi'] = summary['portfolio_dpi'] + summary['portfolio_rvpi']

        return summary

    def forecast_capital_calls(self, months=12):
        """
        Forecast capital calls for next N months

        Uses industry standard deployment curves:
        - Year 1: 20-30% of commitment
        - Year 2: 30-40% of commitment
        - Year 3: 20-30% of commitment
        - Year 4+: 10-20% of commitment
        """
        funds = self._load_csv(self.funds_file)

        forecast = []
        today = datetime.now()

        for fund in funds:
            if fund['status'] != 'Active':
                continue

            commitment = float(fund['commitment_amount'])
            metrics = self.get_fund_metrics(fund['fund_id'])
            unfunded = metrics['unfunded'] if metrics else commitment

            if unfunded <= 0:
                continue  # Fully deployed

            # Calculate fund age
            commitment_date = datetime.strptime(fund['commitment_date'], '%Y-%m-%d')
            age_years = (today - commitment_date).days / 365.25

            # Estimate remaining deployment pace
            if age_years < 1:
                monthly_rate = 0.025  # 2.5% per month (30% in year 1)
            elif age_years < 2:
                monthly_rate = 0.030  # 3% per month (36% in year 2)
            elif age_years < 3:
                monthly_rate = 0.020  # 2% per month (24% in year 3)
            else:
                monthly_rate = 0.010  # 1% per month (12% in year 4+)

            # Generate monthly forecasts
            remaining = unfunded
            for month in range(1, months + 1):
                if remaining <= 0:
                    break

                call_amount = min(remaining, commitment * monthly_rate)
                call_date = today + timedelta(days=30 * month)

                forecast.append({
                    'fund_id': fund['fund_id'],
                    'fund_name': fund['fund_name'],
                    'month': month,
                    'call_date': call_date.strftime('%Y-%m-%d'),
                    'amount': call_amount
                })

                remaining -= call_amount

        return sorted(forecast, key=lambda x: x['call_date'])

    def analyze_portfolio_construction(self):
        """
        Analyze portfolio construction and diversification

        Best practices for VC fund-of-funds:
        - No single fund > 15% of portfolio
        - No vintage year > 30% of portfolio
        - No sector > 40% of portfolio
        - Minimum 10 funds (preferably 15-20)
        - Diversified across stages and geographies
        """
        funds = self._load_csv(self.funds_file)
        summary = self.get_portfolio_summary()

        analysis = {
            'total_funds': len(funds),
            'diversification_score': 0,
            'warnings': [],
            'by_vintage': defaultdict(lambda: {'count': 0, 'commitment': 0}),
            'by_stage': defaultdict(lambda: {'count': 0, 'commitment': 0}),
            'by_sector': defaultdict(lambda: {'count': 0, 'commitment': 0}),
            'by_geography': defaultdict(lambda: {'count': 0, 'commitment': 0}),
            'largest_positions': []
        }

        total_commitment = summary['total_commitment']

        # Analyze each fund
        for fund in funds:
            commitment = float(fund['commitment_amount'])
            pct = (commitment / total_commitment * 100) if total_commitment > 0 else 0

            # Check single fund concentration
            if pct > 15:
                analysis['warnings'].append(
                    f"⚠️  {fund['fund_name']}: {pct:.1f}% (exceeds 15% limit)"
                )

            # Aggregate by dimensions
            analysis['by_vintage'][fund['vintage_year']]['count'] += 1
            analysis['by_vintage'][fund['vintage_year']]['commitment'] += commitment

            if fund['stage_focus']:
                analysis['by_stage'][fund['stage_focus']]['count'] += 1
                analysis['by_stage'][fund['stage_focus']]['commitment'] += commitment

            if fund['sector_focus']:
                analysis['by_sector'][fund['sector_focus']]['count'] += 1
                analysis['by_sector'][fund['sector_focus']]['commitment'] += commitment

            analysis['by_geography'][fund['geography']]['count'] += 1
            analysis['by_geography'][fund['geography']]['commitment'] += commitment

            analysis['largest_positions'].append({
                'fund_name': fund['fund_name'],
                'commitment': commitment,
                'percent': pct
            })

        # Check vintage year concentration
        for vintage, data in analysis['by_vintage'].items():
            pct = (data['commitment'] / total_commitment * 100) if total_commitment > 0 else 0
            if pct > 30:
                analysis['warnings'].append(
                    f"⚠️  Vintage {vintage}: {pct:.1f}% (exceeds 30% limit)"
                )

        # Check sector concentration
        for sector, data in analysis['by_sector'].items():
            pct = (data['commitment'] / total_commitment * 100) if total_commitment > 0 else 0
            if pct > 40:
                analysis['warnings'].append(
                    f"⚠️  Sector {sector}: {pct:.1f}% (exceeds 40% limit)"
                )

        # Check minimum fund count
        if len(funds) < 10:
            analysis['warnings'].append(
                f"⚠️  Only {len(funds)} funds (minimum 10 recommended)"
            )

        # Sort largest positions
        analysis['largest_positions'] = sorted(
            analysis['largest_positions'],
            key=lambda x: x['commitment'],
            reverse=True
        )[:10]

        # Calculate diversification score (0-100)
        score = 100
        if len(funds) < 10:
            score -= (10 - len(funds)) * 5  # -5 points per missing fund
        score -= len(analysis['warnings']) * 10  # -10 points per warning
        analysis['diversification_score'] = max(0, score)

        return analysis

    def show_portfolio_dashboard(self):
        """Display comprehensive portfolio dashboard"""
        summary = self.get_portfolio_summary()

        print("\n" + "="*80)
        print("PORTFOLIO DASHBOARD")
        print("="*80)

        print(f"\n💼 PORTFOLIO SUMMARY")
        print(f"  Total Funds:        {summary['total_funds']}")
        print(f"  Total Commitment:   ${summary['total_commitment']:,.0f}")
        print(f"  Capital Paid In:    ${summary['total_paid_in']:,.0f}")
        print(f"  Unfunded:           ${summary['total_unfunded']:,.0f}")
        print(f"  Current NAV:        ${summary['total_nav']:,.0f}")
        print(f"  Distributions:      ${summary['total_distributions']:,.0f}")

        print(f"\n📊 PORTFOLIO PERFORMANCE")
        print(f"  TVPI (Total Value / Paid In):  {summary['portfolio_tvpi']:.2f}x")
        print(f"  DPI (Distributions / Paid In): {summary['portfolio_dpi']:.2f}x")
        print(f"  RVPI (Residual / Paid In):     {summary['portfolio_rvpi']:.2f}x")

        # Top performers
        if summary['funds']:
            top_performers = sorted(summary['funds'], key=lambda x: x['tvpi'], reverse=True)[:5]
            print(f"\n⭐ TOP 5 PERFORMERS")
            for i, fund in enumerate(top_performers, 1):
                print(f"  {i}. {fund['fund_name']:<30} TVPI: {fund['tvpi']:.2f}x  IRR: {fund['irr']:.1f}%")

        print("\n" + "="*80 + "\n")

    def show_cashflow_forecast(self, months=12):
        """Display cash flow forecast"""
        forecast = self.forecast_capital_calls(months)

        # Aggregate by month
        by_month = defaultdict(float)
        for item in forecast:
            month_key = item['call_date'][:7]  # YYYY-MM
            by_month[month_key] += item['amount']

        print(f"\n💰 CAPITAL CALL FORECAST ({months} months)")
        print("="*60)

        total_forecast = 0
        for month in sorted(by_month.keys()):
            amount = by_month[month]
            total_forecast += amount
            print(f"  {month}:  ${amount:>12,.0f}")

        print("  " + "-"*56)
        print(f"  Total:     ${total_forecast:>12,.0f}")
        print()

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
    pm = PortfolioManager()
    pm.show_portfolio_dashboard()

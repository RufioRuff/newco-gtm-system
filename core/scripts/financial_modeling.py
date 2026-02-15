#!/usr/bin/env python3
"""
Financial Modeling - Cash Flow Projections & Scenario Analysis

Models portfolio financials over 3-5 year horizon:
- Cash flow projections (capital calls, distributions, expenses)
- Scenario analysis (bull, base, bear cases)
- Budget vs actual tracking
- Fundraising modeling (when to raise more capital)
- What-if analysis
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import json
from portfolio_management import PortfolioManager
from public_markets import PublicMarketsEngine

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"


class FinancialModeler:
    """Financial modeling and forecasting"""

    def __init__(self):
        self.portfolio = PortfolioManager()
        self.public_markets = PublicMarketsEngine()
        self.budget_file = DATA_DIR / "annual_budget.csv"
        self.actuals_file = DATA_DIR / "monthly_actuals.csv"
        self.assumptions_file = MODELS_DIR / "model_assumptions.json"
        self._initialize_files()

    def _initialize_files(self):
        """Initialize financial modeling files"""
        MODELS_DIR.mkdir(parents=True, exist_ok=True)

        if not self.budget_file.exists():
            self.budget_file.write_text(
                "year,category,budgeted_amount,notes\n"
            )

        if not self.actuals_file.exists():
            self.actuals_file.write_text(
                "month,year,category,actual_amount,notes\n"
            )

        if not self.assumptions_file.exists():
            # Default assumptions
            default_assumptions = {
                "deployment_rates": {
                    "year_1": 0.30,  # 30% of commitment in year 1
                    "year_2": 0.36,  # 36% in year 2
                    "year_3": 0.24,  # 24% in year 3
                    "year_4_plus": 0.10  # 10% in year 4+
                },
                "distribution_timing": {
                    "years_to_first_distribution": 3,
                    "distribution_acceleration": 0.15  # 15% increase per year
                },
                "management_fees": {
                    "fee_rate": 0.0125,  # 1.25% annual
                    "on_commitment": True  # Fee on commitment vs NAV
                },
                "operating_expenses": {
                    "annual_base": 500000,  # $500K base
                    "per_fund": 50000,  # $50K per fund
                    "inflation": 0.03  # 3% annual increase
                },
                "scenarios": {
                    "bull": {
                        "multiple_markup": 1.5,  # NAVs grow 50%
                        "distribution_acceleration": 1.3,  # 30% faster
                        "new_commitments_per_year": 4
                    },
                    "base": {
                        "multiple_markup": 1.0,  # NAVs stable
                        "distribution_acceleration": 1.0,  # On schedule
                        "new_commitments_per_year": 3
                    },
                    "bear": {
                        "multiple_markup": 0.7,  # 30% mark-down
                        "distribution_acceleration": 0.7,  # 30% slower
                        "new_commitments_per_year": 2
                    }
                },
                "new_commitments": {
                    "avg_commitment_size": 3000000,  # $3M per fund
                    "commitments_per_year": 3
                }
            }

            with open(self.assumptions_file, 'w') as f:
                json.dump(default_assumptions, f, indent=2)

    def load_assumptions(self):
        """Load modeling assumptions"""
        with open(self.assumptions_file, 'r') as f:
            return json.load(f)

    def save_assumptions(self, assumptions):
        """Save modeling assumptions"""
        with open(self.assumptions_file, 'w') as f:
            json.dump(assumptions, f, indent=2)

    def project_cashflow(self, years=3, scenario='base'):
        """
        Project cash flows over N years

        Args:
            years: Number of years to project
            scenario: 'bull', 'base', or 'bear'

        Returns:
            Dictionary with annual projections
        """
        assumptions = self.load_assumptions()
        scenario_params = assumptions['scenarios'][scenario]

        # Get current portfolio
        portfolio_summary = self.portfolio.get_portfolio_summary()
        current_year = datetime.now().year

        projections = []

        for year_offset in range(years):
            year = current_year + year_offset
            projection = {
                'year': year,
                'scenario': scenario,
                'capital_calls': 0,
                'distributions': 0,
                'management_fees': 0,
                'operating_expenses': 0,
                'new_commitments': 0,
                'net_cashflow': 0,
                'nav_estimate': 0
            }

            # Existing funds - capital calls
            for fund in portfolio_summary['funds']:
                fund_age = year - int(fund['vintage_year'])
                unfunded = fund['unfunded']

                if unfunded > 0 and fund_age < 5:
                    # Apply deployment curve
                    if fund_age == 0:
                        call_rate = assumptions['deployment_rates']['year_1']
                    elif fund_age == 1:
                        call_rate = assumptions['deployment_rates']['year_2']
                    elif fund_age == 2:
                        call_rate = assumptions['deployment_rates']['year_3']
                    else:
                        call_rate = assumptions['deployment_rates']['year_4_plus']

                    annual_call = min(unfunded, fund['commitment'] * call_rate)
                    projection['capital_calls'] += annual_call

            # Existing funds - distributions
            for fund in portfolio_summary['funds']:
                fund_age = year - int(fund['vintage_year'])
                years_to_first = assumptions['distribution_timing']['years_to_first_distribution']

                if fund_age >= years_to_first:
                    # Estimate distributions based on fund maturity
                    years_distributing = fund_age - years_to_first + 1
                    base_distribution_rate = 0.15 * years_distributing  # 15% per year

                    # Apply scenario
                    distribution_rate = base_distribution_rate * scenario_params['distribution_acceleration']
                    distribution_rate = min(distribution_rate, 0.40)  # Cap at 40% per year

                    estimated_dist = fund['current_nav'] * distribution_rate
                    projection['distributions'] += estimated_dist

            # New commitments (scenario dependent)
            new_commits_count = scenario_params['new_commitments_per_year']
            avg_size = assumptions['new_commitments']['avg_commitment_size']
            projection['new_commitments'] = new_commits_count * avg_size

            # Management fees
            if assumptions['management_fees']['on_commitment']:
                fee_base = portfolio_summary['total_commitment'] + projection['new_commitments']
            else:
                fee_base = portfolio_summary['total_nav']

            projection['management_fees'] = fee_base * assumptions['management_fees']['fee_rate']

            # Operating expenses
            base_opex = assumptions['operating_expenses']['annual_base']
            per_fund_opex = assumptions['operating_expenses']['per_fund'] * portfolio_summary['total_funds']
            inflation_factor = (1 + assumptions['operating_expenses']['inflation']) ** year_offset
            projection['operating_expenses'] = (base_opex + per_fund_opex) * inflation_factor

            # Net cash flow
            projection['net_cashflow'] = (
                projection['distributions']
                - projection['capital_calls']
                - projection['new_commitments']
                - projection['management_fees']
                - projection['operating_expenses']
            )

            # NAV estimate (simplified)
            if year_offset == 0:
                projection['nav_estimate'] = portfolio_summary['total_nav']
            else:
                prev_nav = projections[-1]['nav_estimate']
                nav_growth = scenario_params['multiple_markup'] - 1.0
                projection['nav_estimate'] = prev_nav * (1 + nav_growth / years)

            projections.append(projection)

        return projections

    def scenario_analysis(self, years=3):
        """
        Run bull, base, bear scenarios

        Returns:
            Dictionary with all three scenarios
        """
        return {
            'bull': self.project_cashflow(years=years, scenario='bull'),
            'base': self.project_cashflow(years=years, scenario='base'),
            'bear': self.project_cashflow(years=years, scenario='bear')
        }

    def show_scenario_comparison(self, years=3):
        """Display scenario comparison table"""
        scenarios = self.scenario_analysis(years=years)

        print("\n" + "="*100)
        print("SCENARIO ANALYSIS - CASH FLOW PROJECTIONS")
        print("="*100)

        for year_idx in range(years):
            year = scenarios['base'][year_idx]['year']

            print(f"\n{'='*100}")
            print(f"YEAR {year}")
            print(f"{'='*100}")

            print(f"\n{'Metric':<30} {'Bull':<20} {'Base':<20} {'Bear':<20}")
            print("-"*100)

            metrics = [
                ('Capital Calls', 'capital_calls'),
                ('Distributions', 'distributions'),
                ('New Commitments', 'new_commitments'),
                ('Management Fees', 'management_fees'),
                ('Operating Expenses', 'operating_expenses'),
                ('Net Cash Flow', 'net_cashflow'),
                ('Estimated NAV', 'nav_estimate')
            ]

            for label, key in metrics:
                bull_val = scenarios['bull'][year_idx][key]
                base_val = scenarios['base'][year_idx][key]
                bear_val = scenarios['bear'][year_idx][key]

                print(f"{label:<30} ${bull_val:>18,.0f} ${base_val:>18,.0f} ${bear_val:>18,.0f}")

        # Summary statistics
        print(f"\n{'='*100}")
        print(f"CUMULATIVE {years}-YEAR TOTALS")
        print(f"{'='*100}\n")

        print(f"{'Metric':<30} {'Bull':<20} {'Base':<20} {'Bear':<20}")
        print("-"*100)

        for label, key in metrics[:-1]:  # Exclude NAV estimate
            bull_total = sum(s[key] for s in scenarios['bull'])
            base_total = sum(s[key] for s in scenarios['base'])
            bear_total = sum(s[key] for s in scenarios['bear'])

            print(f"{label:<30} ${bull_total:>18,.0f} ${base_total:>18,.0f} ${bear_total:>18,.0f}")

        print("\n" + "="*100 + "\n")

    def budget_variance_analysis(self, year=None):
        """
        Compare budget vs actual spending

        Args:
            year: Year to analyze (defaults to current year)

        Returns:
            Dictionary with variance analysis
        """
        if year is None:
            year = datetime.now().year

        # Load budget
        budgets = self._load_csv(self.budget_file)
        year_budget = [b for b in budgets if int(b['year']) == year]

        # Load actuals
        actuals = self._load_csv(self.actuals_file)
        year_actuals = [a for a in actuals if int(a['year']) == year]

        # Group by category
        budget_by_category = defaultdict(float)
        actuals_by_category = defaultdict(float)

        for budget in year_budget:
            budget_by_category[budget['category']] += float(budget['budgeted_amount'])

        for actual in year_actuals:
            actuals_by_category[actual['category']] += float(actual['actual_amount'])

        # Calculate variances
        variances = {}
        all_categories = set(budget_by_category.keys()) | set(actuals_by_category.keys())

        for category in all_categories:
            budgeted = budget_by_category.get(category, 0)
            actual = actuals_by_category.get(category, 0)
            variance = actual - budgeted
            variance_pct = (variance / budgeted * 100) if budgeted > 0 else 0

            variances[category] = {
                'budgeted': budgeted,
                'actual': actual,
                'variance': variance,
                'variance_pct': variance_pct,
                'status': 'Over' if variance > 0 else 'Under' if variance < 0 else 'On Target'
            }

        return {
            'year': year,
            'variances': variances,
            'total_budgeted': sum(budget_by_category.values()),
            'total_actual': sum(actuals_by_category.values()),
            'total_variance': sum(actuals_by_category.values()) - sum(budget_by_category.values())
        }

    def show_budget_variance(self, year=None):
        """Display budget variance report"""
        analysis = self.budget_variance_analysis(year)

        print("\n" + "="*80)
        print(f"BUDGET VARIANCE ANALYSIS - {analysis['year']}")
        print("="*80)

        print(f"\n{'Category':<25} {'Budget':<15} {'Actual':<15} {'Variance':<15} {'%':<10} {'Status'}")
        print("-"*80)

        for category, data in sorted(analysis['variances'].items()):
            status_icon = '⚠️ ' if abs(data['variance_pct']) > 10 else '✓ '
            print(f"{category:<25} ${data['budgeted']:>13,.0f} ${data['actual']:>13,.0f} "
                  f"${data['variance']:>13,.0f} {data['variance_pct']:>8.1f}% {status_icon}{data['status']}")

        print("-"*80)
        print(f"{'TOTAL':<25} ${analysis['total_budgeted']:>13,.0f} ${analysis['total_actual']:>13,.0f} "
              f"${analysis['total_variance']:>13,.0f}")

        print("\n" + "="*80 + "\n")

    def fundraising_model(self, current_cash, runway_months=24):
        """
        Model when to raise additional capital

        Args:
            current_cash: Current cash position
            runway_months: Desired cash runway in months

        Returns:
            Fundraising recommendation
        """
        # Project cash flows
        projections = self.project_cashflow(years=3, scenario='base')

        # Calculate monthly cash flow
        monthly_cashflows = []
        for annual in projections:
            monthly_burn = (
                annual['capital_calls'] / 12 +
                annual['new_commitments'] / 12 +
                annual['management_fees'] / 12 +
                annual['operating_expenses'] / 12 -
                annual['distributions'] / 12
            )
            for month in range(12):
                monthly_cashflows.append(monthly_burn)

        # Calculate runway
        cumulative_cash = current_cash
        months_until_zero = 0

        for month_idx, monthly_burn in enumerate(monthly_cashflows):
            cumulative_cash -= monthly_burn
            if cumulative_cash <= 0:
                months_until_zero = month_idx
                break

        # Recommendation
        if months_until_zero == 0:
            recommendation = "URGENT: Negative cash position. Raise capital immediately."
            target_raise = sum(monthly_cashflows[:runway_months])
        elif months_until_zero < runway_months:
            recommendation = f"SOON: Only {months_until_zero} months of runway. Begin fundraising process."
            shortfall = sum(monthly_cashflows[:runway_months]) - current_cash
            target_raise = max(shortfall, sum(monthly_cashflows[:24]))  # At least 24 months
        else:
            recommendation = f"HEALTHY: {months_until_zero} months of runway. Monitor quarterly."
            target_raise = 0

        return {
            'current_cash': current_cash,
            'runway_months': months_until_zero if months_until_zero > 0 else 0,
            'desired_runway': runway_months,
            'recommendation': recommendation,
            'target_raise': target_raise,
            'monthly_cashflows': monthly_cashflows[:12]  # Next 12 months
        }

    def show_fundraising_analysis(self, current_cash):
        """Display fundraising analysis"""
        analysis = self.fundraising_model(current_cash)

        print("\n" + "="*80)
        print("FUNDRAISING ANALYSIS")
        print("="*80)

        print(f"\n💰 Current Cash Position: ${analysis['current_cash']:,.0f}")
        print(f"📅 Current Runway: {analysis['runway_months']} months")
        print(f"🎯 Target Runway: {analysis['desired_runway']} months")

        print(f"\n📊 Recommendation:")
        print(f"   {analysis['recommendation']}")

        if analysis['target_raise'] > 0:
            print(f"\n💵 Target Raise Amount: ${analysis['target_raise']:,.0f}")

        print(f"\n📈 Next 12 Months Cash Flow:")
        print(f"{'Month':<10} {'Net Cash Flow':<20}")
        print("-"*30)

        for month_idx, cashflow in enumerate(analysis['monthly_cashflows'], 1):
            print(f"Month {month_idx:<4} ${cashflow:>18,.0f}")

        print("\n" + "="*80 + "\n")

    def what_if_analysis(self, parameter, values):
        """
        What-if analysis for a specific parameter

        Args:
            parameter: Parameter to vary (e.g., 'new_commitments_per_year')
            values: List of values to test

        Returns:
            List of projections for each value
        """
        assumptions = self.load_assumptions()
        results = []

        for value in values:
            # Modify assumption
            modified_assumptions = assumptions.copy()

            # Navigate nested dict structure
            if '.' in parameter:
                parts = parameter.split('.')
                target = modified_assumptions
                for part in parts[:-1]:
                    target = target[part]
                target[parts[-1]] = value
            else:
                modified_assumptions[parameter] = value

            # Temporarily save modified assumptions
            original_assumptions = assumptions
            self.save_assumptions(modified_assumptions)

            # Run projection
            projection = self.project_cashflow(years=3, scenario='base')

            # Calculate summary metrics
            total_calls = sum(p['capital_calls'] for p in projection)
            total_distributions = sum(p['distributions'] for p in projection)
            net_cashflow = sum(p['net_cashflow'] for p in projection)

            results.append({
                'parameter_value': value,
                'total_capital_calls': total_calls,
                'total_distributions': total_distributions,
                'net_cashflow': net_cashflow,
                'ending_nav': projection[-1]['nav_estimate']
            })

            # Restore original assumptions
            self.save_assumptions(original_assumptions)

        return results

    def add_budget(self, year, category, amount, notes=''):
        """Add budget line item"""
        budgets = self._load_csv(self.budget_file)

        budgets.append({
            'year': str(year),
            'category': category,
            'budgeted_amount': str(amount),
            'notes': notes
        })

        self._save_csv(self.budget_file, budgets)
        print(f"✓ Added budget: {year} {category} ${amount:,.0f}")

    def add_actual(self, month, year, category, amount, notes=''):
        """Log actual spending"""
        actuals = self._load_csv(self.actuals_file)

        actuals.append({
            'month': str(month),
            'year': str(year),
            'category': category,
            'actual_amount': str(amount),
            'notes': notes
        })

        self._save_csv(self.actuals_file, actuals)
        print(f"✓ Logged actual: {year}-{month:02d} {category} ${amount:,.0f}")

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
    # Demo scenario analysis
    modeler = FinancialModeler()
    modeler.show_scenario_comparison(years=3)

#!/usr/bin/env python3
"""
Board Reporting - Automated Board Materials Generation

Generates quarterly board meeting materials:
- Executive summary
- Portfolio overview
- Performance metrics
- Risk dashboard
- Pipeline status
- Public market performance
- Action items tracking
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from portfolio_management import PortfolioManager
from manager_crm import ManagerCRM
from risk_management import RiskManager
from public_markets import PublicMarketsEngine

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports" / "board"


class BoardReportGenerator:
    """Generate automated board meeting materials"""

    def __init__(self):
        self.portfolio = PortfolioManager()
        self.manager_crm = ManagerCRM()
        self.risk = RiskManager()
        self.public_markets = PublicMarketsEngine()
        self.action_items_file = DATA_DIR / "board_action_items.csv"
        self._initialize_files()

    def _initialize_files(self):
        """Initialize board tracking files"""
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        if not self.action_items_file.exists():
            self.action_items_file.write_text(
                "item_id,meeting_date,item,owner,due_date,status,completed_date,notes\n"
            )

    def generate_board_deck(self, meeting_date=None, output_format='markdown'):
        """
        Generate complete board deck

        Args:
            meeting_date: Date of board meeting (defaults to today)
            output_format: 'markdown' or 'text'

        Returns:
            Path to generated report file
        """
        if meeting_date is None:
            meeting_date = datetime.now()
        elif isinstance(meeting_date, str):
            meeting_date = datetime.strptime(meeting_date, '%Y-%m-%d')

        quarter = self._get_quarter(meeting_date)
        year = meeting_date.year

        # Generate all sections
        sections = {
            'cover': self._generate_cover_slide(quarter, year),
            'executive_summary': self._generate_executive_summary(),
            'portfolio_overview': self._generate_portfolio_overview(),
            'performance': self._generate_performance_slide(),
            'capital_deployment': self._generate_capital_deployment(),
            'pipeline': self._generate_pipeline_slide(),
            'public_markets': self._generate_public_markets_slide(),
            'risk_dashboard': self._generate_risk_slide(),
            'action_items': self._generate_action_items_slide()
        }

        # Compile report
        if output_format == 'markdown':
            report = self._compile_markdown_report(sections, quarter, year)
        else:
            report = self._compile_text_report(sections, quarter, year)

        # Save to file
        filename = f"board_deck_Q{quarter}_{year}.md" if output_format == 'markdown' else f"board_deck_Q{quarter}_{year}.txt"
        output_path = REPORTS_DIR / filename

        with open(output_path, 'w') as f:
            f.write(report)

        return output_path

    def _get_quarter(self, date):
        """Get quarter from date (1-4)"""
        return (date.month - 1) // 3 + 1

    def _generate_cover_slide(self, quarter, year):
        """Generate cover slide"""
        return {
            'title': f'NEWCO Board Meeting',
            'subtitle': f'Q{quarter} {year}',
            'date': datetime.now().strftime('%B %d, %Y')
        }

    def _generate_executive_summary(self):
        """Generate executive summary with key metrics"""
        portfolio_summary = self.portfolio.get_portfolio_summary()
        risk_dashboard = self.risk.get_risk_dashboard()
        manager_summary = self.manager_crm.get_pipeline_summary()

        # Get public markets data
        try:
            nav_data = self.public_markets._load_csv(self.public_markets.nav_file)
            latest_nav = nav_data[-1] if nav_data else None
            premium_discount = self.public_markets.calculate_premium_discount()
        except:
            latest_nav = None
            premium_discount = None

        return {
            'portfolio_nav': portfolio_summary['total_nav'],
            'portfolio_tvpi': portfolio_summary.get('portfolio_tvpi', 0),
            'fund_count': portfolio_summary['total_funds'],
            'unfunded_commitments': sum(f['unfunded'] for f in portfolio_summary['funds']),
            'risk_level': risk_dashboard['risk_level'],
            'risk_score': risk_dashboard['risk_score'],
            'managers_active_dd': len([m for m in manager_summary['by_stage_list'].get('Deep DD', [])]),
            'managers_ic_review': len(manager_summary['by_stage_list'].get('IC Review', [])),
            'premium_discount': premium_discount.get('premium_discount_pct') if premium_discount else None,
            'nav_per_share': latest_nav.get('nav_per_share') if latest_nav else None
        }

    def _generate_portfolio_overview(self):
        """Generate portfolio overview slide"""
        summary = self.portfolio.get_portfolio_summary()
        analysis = self.portfolio.analyze_portfolio_construction()

        # Calculate key metrics
        total_commitment = summary['total_commitment']
        total_paid_in = summary['total_paid_in']
        total_nav = summary['total_nav']
        total_distributions = summary['total_distributions']

        return {
            'fund_count': summary['total_funds'],
            'total_commitment': total_commitment,
            'total_paid_in': total_paid_in,
            'total_nav': total_nav,
            'total_distributions': total_distributions,
            'unfunded_commitments': total_commitment - total_paid_in,
            'deployment_pct': (total_paid_in / total_commitment * 100) if total_commitment > 0 else 0,
            'by_vintage': analysis['by_vintage'],
            'by_stage': analysis['by_stage'],
            'by_sector': dict(analysis['by_sector']),
            'diversification_score': analysis['diversification_score']
        }

    def _generate_performance_slide(self):
        """Generate performance metrics slide"""
        summary = self.portfolio.get_portfolio_summary()

        # Sort funds by performance
        top_performers = sorted(summary['funds'], key=lambda x: x.get('tvpi', 0), reverse=True)[:5]
        bottom_performers = sorted(summary['funds'], key=lambda x: x.get('tvpi', 0))[:3]

        # Calculate quartile positioning
        all_tvpis = [f.get('tvpi', 0) for f in summary['funds'] if f.get('tvpi', 0) > 0]
        avg_tvpi = sum(all_tvpis) / len(all_tvpis) if all_tvpis else 0

        return {
            'portfolio_tvpi': summary.get('portfolio_tvpi', 0),
            'portfolio_dpi': summary.get('portfolio_dpi', 0),
            'portfolio_rvpi': summary.get('portfolio_rvpi', 0),
            'avg_fund_tvpi': avg_tvpi,
            'top_performers': top_performers,
            'bottom_performers': bottom_performers,
            'funds_above_1x': len([f for f in summary['funds'] if f.get('tvpi', 0) > 1.0]),
            'funds_above_2x': len([f for f in summary['funds'] if f.get('tvpi', 0) > 2.0]),
            'total_funds': len(summary['funds'])
        }

    def _generate_capital_deployment(self):
        """Generate capital deployment slide"""
        summary = self.portfolio.get_portfolio_summary()
        forecast = self.portfolio.forecast_capital_calls(months=12)

        # Group forecast by quarter
        quarterly_forecast = defaultdict(float)
        for call in forecast:
            call_date = datetime.strptime(call['call_date'], '%Y-%m-%d')
            quarter_key = f"Q{self._get_quarter(call_date)} {call_date.year}"
            quarterly_forecast[quarter_key] += call['amount']

        # Calculate deployment pace
        total_commitment = summary['total_commitment']
        total_paid_in = summary['total_paid_in']
        deployment_rate = (total_paid_in / total_commitment) if total_commitment > 0 else 0

        return {
            'total_commitment': total_commitment,
            'paid_in': total_paid_in,
            'unfunded': total_commitment - total_paid_in,
            'deployment_rate': deployment_rate * 100,
            'quarterly_forecast': dict(quarterly_forecast),
            'twelve_month_forecast': sum(quarterly_forecast.values()),
            'capital_calls_ytd': self._calculate_capital_calls_ytd()
        }

    def _calculate_capital_calls_ytd(self):
        """Calculate capital calls year-to-date"""
        calls = self.portfolio._load_csv(self.portfolio.capital_calls_file)
        current_year = datetime.now().year

        ytd_calls = sum(
            float(call['amount'])
            for call in calls
            if call['status'] == 'Paid' and
            datetime.strptime(call['call_date'], '%Y-%m-%d').year == current_year
        )

        return ytd_calls

    def _generate_pipeline_slide(self):
        """Generate manager pipeline slide"""
        summary = self.manager_crm.get_pipeline_summary()

        # Get detailed stage information
        pipeline = {
            'total': summary['total'],
            'by_stage': dict(summary['by_stage']),
            'sourced': summary['by_stage'].get('Sourced', 0),
            'screening': summary['by_stage'].get('Screening', 0),
            'deep_dd': summary['by_stage'].get('Deep DD', 0),
            'ic_review': summary['by_stage'].get('IC Review', 0),
            'committed': summary['by_stage'].get('Committed', 0),
            'passed': summary['by_stage'].get('Passed', 0)
        }

        # Get active DD details
        dd_items = self.manager_crm._load_csv(self.manager_crm.due_diligence_file)
        active_dd = [dd for dd in dd_items if dd['status'] == 'In Progress']

        # Get IC review details
        ic_managers = summary['by_stage_list'].get('IC Review', [])

        return {
            'pipeline': pipeline,
            'active_dd_count': len(active_dd),
            'active_dd_details': active_dd,
            'ic_review_count': len(ic_managers),
            'ic_review_details': ic_managers,
            'conversion_rate': (pipeline['committed'] / pipeline['total'] * 100) if pipeline['total'] > 0 else 0
        }

    def _generate_public_markets_slide(self):
        """Generate public markets performance slide"""
        try:
            prices = self.public_markets._load_csv(self.public_markets.prices_file)
            nav_data = self.public_markets._load_csv(self.public_markets.nav_file)

            if not prices or not nav_data:
                return {'available': False}

            latest_price = prices[-1]
            latest_nav = nav_data[-1]

            # Calculate premium/discount
            premium_discount = self.public_markets.calculate_premium_discount()

            # Calculate returns
            if len(prices) >= 90:
                price_90_days_ago = next((p for p in reversed(prices[:-90]) if p), prices[0])
                qtd_return = (float(latest_price['close']) - float(price_90_days_ago['close'])) / float(price_90_days_ago['close']) * 100
            else:
                qtd_return = 0

            # Get investor composition
            investor_base = self.public_markets.analyze_investor_base()

            return {
                'available': True,
                'stock_price': float(latest_price['close']),
                'nav_per_share': float(latest_nav['nav_per_share']),
                'premium_discount': premium_discount.get('premium_discount_pct', 0),
                'qtd_return': qtd_return,
                'ytd_return': premium_discount.get('ytd_return', 0),
                'market_cap': float(latest_price['close']) * float(latest_nav.get('shares_outstanding', 0)),
                'avg_daily_volume': premium_discount.get('avg_daily_volume', 0),
                'investor_composition': investor_base.get('composition', {})
            }
        except:
            return {'available': False}

    def _generate_risk_slide(self):
        """Generate risk dashboard slide"""
        dashboard = self.risk.get_risk_dashboard()

        concentration = dashboard['concentration']
        vintage = dashboard['vintage']
        liquidity = dashboard['liquidity']

        return {
            'risk_level': dashboard['risk_level'],
            'risk_score': dashboard['risk_score'],
            'violations_count': len(concentration['violations']),
            'violations': concentration['violations'],
            'fund_count': concentration['fund_count'],
            'vintage_diversification': vintage['diversification_score'],
            'bubble_exposure': vintage['bubble_exposure'],
            'liquidity_12m_forecast': liquidity['forecast_12m'],
            'liquidity_reserve_needed': liquidity['required_cash_reserve'],
            'compliance_status': 'COMPLIANT' if concentration['status'] == 'COMPLIANT' else 'NON-COMPLIANT'
        }

    def _generate_action_items_slide(self):
        """Generate action items tracking slide"""
        action_items = self._load_csv(self.action_items_file)

        # Filter open items
        open_items = [item for item in action_items if item['status'] != 'Completed']
        overdue_items = []

        today = datetime.now()
        for item in open_items:
            if item['due_date']:
                due_date = datetime.strptime(item['due_date'], '%Y-%m-%d')
                if due_date < today:
                    overdue_items.append(item)

        # Recently completed items
        completed_items = [
            item for item in action_items
            if item['status'] == 'Completed' and item.get('completed_date')
        ]

        # Sort by completion date, most recent first
        if completed_items:
            completed_items.sort(key=lambda x: x['completed_date'], reverse=True)
            recent_completed = completed_items[:5]
        else:
            recent_completed = []

        return {
            'total_open': len(open_items),
            'overdue': len(overdue_items),
            'open_items': open_items,
            'overdue_items': overdue_items,
            'recent_completed': recent_completed
        }

    def _compile_markdown_report(self, sections, quarter, year):
        """Compile sections into markdown report"""
        md = f"""# NEWCO Board Meeting
## Q{quarter} {year} Board Deck
**Generated:** {datetime.now().strftime('%B %d, %Y')}

---

## Slide 1: Executive Summary

### Key Metrics

| Metric | Value |
|--------|-------|
| Portfolio NAV | ${sections['executive_summary']['portfolio_nav']:,.0f} |
| Portfolio TVPI | {sections['executive_summary']['portfolio_tvpi']:.2f}x |
| Fund Count | {sections['executive_summary']['fund_count']} |
| Unfunded Commitments | ${sections['executive_summary']['unfunded_commitments']:,.0f} |
| Risk Level | {sections['executive_summary']['risk_level']} ({sections['executive_summary']['risk_score']}/100) |

### Pipeline Activity

- **Active Due Diligence:** {sections['executive_summary']['managers_active_dd']} managers
- **IC Review:** {sections['executive_summary']['managers_ic_review']} managers

"""

        if sections['executive_summary']['premium_discount'] is not None:
            md += f"""### Public Market Performance

- **Stock Premium/Discount to NAV:** {sections['executive_summary']['premium_discount']:.1f}%
- **NAV per Share:** ${sections['executive_summary']['nav_per_share']:.2f}

"""

        md += """---

## Slide 2: Portfolio Overview

"""

        portfolio = sections['portfolio_overview']
        md += f"""### Portfolio Summary

- **Total Funds:** {portfolio['fund_count']}
- **Total Commitment:** ${portfolio['total_commitment']:,.0f}
- **Paid In:** ${portfolio['total_paid_in']:,.0f} ({portfolio['deployment_pct']:.1f}% deployed)
- **Current NAV:** ${portfolio['total_nav']:,.0f}
- **Distributions:** ${portfolio['total_distributions']:,.0f}
- **Unfunded:** ${portfolio['unfunded_commitments']:,.0f}

### Diversification

**By Vintage Year:**

"""
        for vintage, data in sorted(portfolio['by_vintage'].items()):
            pct = data['commitment'] / portfolio['total_commitment'] * 100 if portfolio['total_commitment'] > 0 else 0
            md += f"- **{vintage}:** {data['count']} funds, ${data['commitment']:,.0f} ({pct:.1f}%)\n"

        md += "\n**By Stage:**\n\n"
        for stage, data in sorted(portfolio['by_stage'].items()):
            if data['commitment'] > 0:
                pct = data['commitment'] / portfolio['total_commitment'] * 100 if portfolio['total_commitment'] > 0 else 0
                md += f"- **{stage}:** {data['count']} funds, ${data['commitment']:,.0f} ({pct:.1f}%)\n"

        md += f"\n**Diversification Score:** {portfolio['diversification_score']}/100\n"

        md += """

---

## Slide 3: Performance Metrics

"""

        perf = sections['performance']
        md += f"""### Portfolio Performance

- **Portfolio TVPI:** {perf['portfolio_tvpi']:.2f}x
- **Portfolio DPI:** {perf['portfolio_dpi']:.2f}x (cash returned)
- **Portfolio RVPI:** {perf['portfolio_rvpi']:.2f}x (unrealized)

### Fund Performance Distribution

- **Funds > 1.0x:** {perf['funds_above_1x']} of {perf['total_funds']} ({perf['funds_above_1x']/perf['total_funds']*100:.0f}%)
- **Funds > 2.0x:** {perf['funds_above_2x']} of {perf['total_funds']} ({perf['funds_above_2x']/perf['total_funds']*100:.0f}%)
- **Average Fund TVPI:** {perf['avg_fund_tvpi']:.2f}x

### Top Performers

"""
        for i, fund in enumerate(perf['top_performers'], 1):
            md += f"{i}. **{fund['fund_name']}** - {fund['tvpi']:.2f}x TVPI\n"

        md += """

---

## Slide 4: Capital Deployment

"""

        deploy = sections['capital_deployment']
        md += f"""### Deployment Status

- **Total Commitment:** ${deploy['total_commitment']:,.0f}
- **Paid In:** ${deploy['paid_in']:,.0f} ({deploy['deployment_rate']:.1f}%)
- **Unfunded:** ${deploy['unfunded']:,.0f}

### Capital Calls

- **YTD Capital Calls:** ${deploy['capital_calls_ytd']:,.0f}
- **12-Month Forecast:** ${deploy['twelve_month_forecast']:,.0f}

### Quarterly Forecast

"""
        for quarter_key, amount in sorted(deploy['quarterly_forecast'].items()):
            md += f"- **{quarter_key}:** ${amount:,.0f}\n"

        md += """

---

## Slide 5: Manager Pipeline

"""

        pipeline = sections['pipeline']
        md += f"""### Pipeline Summary

- **Total Managers:** {pipeline['pipeline']['total']}
- **Conversion Rate:** {pipeline['conversion_rate']:.1f}%

### By Stage

- **Sourced:** {pipeline['pipeline']['sourced']}
- **Screening:** {pipeline['pipeline']['screening']}
- **Deep DD:** {pipeline['pipeline']['deep_dd']} (🔍 {pipeline['active_dd_count']} active)
- **IC Review:** {pipeline['pipeline']['ic_review']}
- **Committed:** {pipeline['pipeline']['committed']}
- **Passed:** {pipeline['pipeline']['passed']}

"""

        if pipeline['ic_review_details']:
            md += "### Managers in IC Review\n\n"
            for mgr in pipeline['ic_review_details']:
                md += f"- **{mgr['fund_name']}** - {mgr['gp_names']}\n"
                md += f"  - Stage: {mgr['stage_focus']}, Sector: {mgr['sector_focus']}\n"

        md += """

---

"""

        # Public Markets Slide
        public = sections['public_markets']
        if public['available']:
            md += f"""## Slide 6: Public Market Performance

### Stock Performance

- **Current Price:** ${public['stock_price']:.2f}
- **NAV per Share:** ${public['nav_per_share']:.2f}
- **Premium/(Discount):** {public['premium_discount']:.1f}%

### Returns

- **QTD Return:** {public['qtd_return']:.1f}%
- **YTD Return:** {public['ytd_return']:.1f}%

### Trading Metrics

- **Market Cap:** ${public['market_cap']:,.0f}
- **Avg Daily Volume:** {public['avg_daily_volume']:,.0f} shares

### Investor Composition

"""
            for investor_type, pct in public['investor_composition'].items():
                md += f"- **{investor_type}:** {pct:.1f}%\n"

            md += "\n---\n\n"
        else:
            md += "## Slide 6: Public Market Performance\n\n*Data not available*\n\n---\n\n"

        # Risk Slide
        risk = sections['risk_dashboard']
        md += f"""## Slide 7: Risk Dashboard

### Overall Risk Assessment

- **Risk Level:** {risk['risk_level']} ({risk['risk_score']}/100)
- **Compliance Status:** {risk['compliance_status']}
- **Policy Violations:** {risk['violations_count']}

### Key Risk Metrics

- **Fund Count:** {risk['fund_count']} (minimum 10)
- **Vintage Diversification:** {risk['vintage_diversification']} years
- **Bubble Era Exposure:** {risk['bubble_exposure']:.1f}%

### Liquidity

- **12-Month Forecast:** ${risk['liquidity_12m_forecast']:,.0f}
- **Cash Reserve Needed:** ${risk['liquidity_reserve_needed']:,.0f}

"""

        if risk['violations']:
            md += "### Policy Violations\n\n"
            for v in risk['violations']:
                md += f"- **[{v['severity']}]** {v['message']}\n"

        md += """

---

## Slide 8: Action Items

"""

        actions = sections['action_items']
        md += f"""### Action Items Status

- **Open Items:** {actions['total_open']}
- **Overdue:** {actions['overdue']}

"""

        if actions['overdue_items']:
            md += "### ⚠️ Overdue Items\n\n"
            for item in actions['overdue_items']:
                md += f"- **{item['item']}** (Owner: {item['owner']}, Due: {item['due_date']})\n"

        if actions['open_items']:
            md += "\n### Open Action Items\n\n"
            for item in actions['open_items']:
                if item not in actions['overdue_items']:
                    md += f"- **{item['item']}** (Owner: {item['owner']}, Due: {item.get('due_date', 'TBD')})\n"

        if actions['recent_completed']:
            md += "\n### ✅ Recently Completed\n\n"
            for item in actions['recent_completed']:
                md += f"- **{item['item']}** (Completed: {item['completed_date']})\n"

        md += """

---

## Appendix: Contact Information

**Management Team:**
- Ken Wallace, CEO
- [CFO Name]
- [COO Name]

**Board Members:**
- [List board members]

**Next Meeting:** [Date]

---

*This board deck was automatically generated by the NEWCO management system.*
"""

        return md

    def _compile_text_report(self, sections, quarter, year):
        """Compile sections into plain text report"""
        # Simplified text version for quick review
        txt = f"""
NEWCO BOARD MEETING - Q{quarter} {year}
{'='*80}
Generated: {datetime.now().strftime('%B %d, %Y')}

EXECUTIVE SUMMARY
{'='*80}
Portfolio NAV:           ${sections['executive_summary']['portfolio_nav']:,.0f}
Portfolio TVPI:          {sections['executive_summary']['portfolio_tvpi']:.2f}x
Fund Count:              {sections['executive_summary']['fund_count']}
Risk Level:              {sections['executive_summary']['risk_level']} ({sections['executive_summary']['risk_score']}/100)
Active DD:               {sections['executive_summary']['managers_active_dd']} managers
IC Review:               {sections['executive_summary']['managers_ic_review']} managers

PORTFOLIO OVERVIEW
{'='*80}
Total Commitment:        ${sections['portfolio_overview']['total_commitment']:,.0f}
Paid In:                 ${sections['portfolio_overview']['total_paid_in']:,.0f} ({sections['portfolio_overview']['deployment_pct']:.1f}%)
Current NAV:             ${sections['portfolio_overview']['total_nav']:,.0f}
Distributions:           ${sections['portfolio_overview']['total_distributions']:,.0f}
Diversification Score:   {sections['portfolio_overview']['diversification_score']}/100

PERFORMANCE METRICS
{'='*80}
Portfolio TVPI:          {sections['performance']['portfolio_tvpi']:.2f}x
Portfolio DPI:           {sections['performance']['portfolio_dpi']:.2f}x
Portfolio RVPI:          {sections['performance']['portfolio_rvpi']:.2f}x
Funds > 1.0x:            {sections['performance']['funds_above_1x']} of {sections['performance']['total_funds']}
Funds > 2.0x:            {sections['performance']['funds_above_2x']} of {sections['performance']['total_funds']}

RISK DASHBOARD
{'='*80}
Risk Level:              {sections['risk_dashboard']['risk_level']} ({sections['risk_dashboard']['risk_score']}/100)
Compliance:              {sections['risk_dashboard']['compliance_status']}
Violations:              {sections['risk_dashboard']['violations_count']}
12-Month Forecast:       ${sections['risk_dashboard']['liquidity_12m_forecast']:,.0f}

ACTION ITEMS
{'='*80}
Open Items:              {sections['action_items']['total_open']}
Overdue:                 {sections['action_items']['overdue']}

{'='*80}
End of Report
"""
        return txt

    def add_action_item(self, item, owner, due_date, meeting_date=None):
        """Add action item from board meeting"""
        action_items = self._load_csv(self.action_items_file)

        if meeting_date is None:
            meeting_date = datetime.now().strftime('%Y-%m-%d')

        item_id = f"AI{len(action_items) + 1:04d}"

        action = {
            'item_id': item_id,
            'meeting_date': meeting_date,
            'item': item,
            'owner': owner,
            'due_date': due_date,
            'status': 'Open',
            'completed_date': '',
            'notes': ''
        }

        action_items.append(action)
        self._save_csv(self.action_items_file, action_items)

        print(f"✓ Added action item: {item_id}")
        print(f"  Owner: {owner}")
        print(f"  Due: {due_date}")

        return item_id

    def update_action_item(self, item_id, status=None, notes=None):
        """Update action item status"""
        action_items = self._load_csv(self.action_items_file)

        for item in action_items:
            if item['item_id'] == item_id:
                if status:
                    item['status'] = status
                    if status == 'Completed':
                        item['completed_date'] = datetime.now().strftime('%Y-%m-%d')
                if notes:
                    item['notes'] = notes

                self._save_csv(self.action_items_file, action_items)
                print(f"✓ Updated action item: {item_id}")
                return True

        print(f"Action item {item_id} not found")
        return False

    def list_action_items(self, status_filter=None):
        """List action items"""
        action_items = self._load_csv(self.action_items_file)

        if status_filter:
            action_items = [item for item in action_items if item['status'] == status_filter]

        return action_items

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
    # Generate board deck
    generator = BoardReportGenerator()
    output_path = generator.generate_board_deck()
    print(f"\n✓ Board deck generated: {output_path}")

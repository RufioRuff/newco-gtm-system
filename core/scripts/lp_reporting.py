#!/usr/bin/env python3
"""
LP Reporting - Quarterly LP Letter Generation

Automates LP reporting:
- Quarterly investor letters
- Capital call notices
- Distribution notices
- Portfolio updates
- Performance reports
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
REPORTS_DIR = BASE_DIR / "reports" / "lp"
TEMPLATES_DIR = BASE_DIR / "templates" / "lp"


class LPReportGenerator:
    """Generate LP communications and reports"""

    def __init__(self):
        self.portfolio = PortfolioManager()
        self.manager_crm = ManagerCRM()
        self.risk = RiskManager()
        self.public_markets = PublicMarketsEngine()
        self._initialize_dirs()

    def _initialize_dirs(self):
        """Initialize directories"""
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    def generate_quarterly_letter(self, quarter=None, year=None, ceo_message='', market_commentary=''):
        """
        Generate quarterly LP letter

        Args:
            quarter: Quarter number (1-4), defaults to current
            year: Year, defaults to current
            ceo_message: CEO's opening message (paragraph)
            market_commentary: Market commentary section (paragraphs)

        Returns:
            Path to generated letter
        """
        if quarter is None or year is None:
            today = datetime.now()
            quarter = (today.month - 1) // 3 + 1
            year = today.year

        # Generate letter sections
        letter = self._compile_quarterly_letter(quarter, year, ceo_message, market_commentary)

        # Save to file
        filename = f"quarterly_letter_Q{quarter}_{year}.md"
        output_path = REPORTS_DIR / filename

        with open(output_path, 'w') as f:
            f.write(letter)

        return output_path

    def _compile_quarterly_letter(self, quarter, year, ceo_message, market_commentary):
        """Compile quarterly letter"""
        letter = f"""# NEWCO
## Quarterly Investor Letter
### Q{quarter} {year}

---

Dear Limited Partners,

"""

        # CEO Message
        if ceo_message:
            letter += f"{ceo_message}\n\n"
        else:
            letter += f"""I am pleased to share our Q{quarter} {year} update. This quarter demonstrated continued progress across our portfolio, with strong performance from several of our fund managers and solid execution on our investment strategy.\n\n"""

        letter += "---\n\n## Executive Summary\n\n"

        # Executive summary with key metrics
        portfolio_summary = self.portfolio.get_portfolio_summary()
        risk_dashboard = self.risk.get_risk_dashboard()

        letter += f"""**Portfolio Snapshot:**

- **Total Funds:** {portfolio_summary['total_funds']} active fund investments
- **Total Commitment:** ${portfolio_summary['total_commitment']:,.0f}
- **Paid-In Capital:** ${portfolio_summary['total_paid_in']:,.0f}
- **Current NAV:** ${portfolio_summary['total_nav']:,.0f}
- **Distributions Received:** ${portfolio_summary['total_distributions']:,.0f}

**Performance:**

- **Portfolio TVPI:** {portfolio_summary.get('portfolio_tvpi', 0):.2f}x
- **Portfolio DPI:** {portfolio_summary.get('portfolio_dpi', 0):.2f}x (cash returned)
- **Portfolio RVPI:** {portfolio_summary.get('portfolio_rvpi', 0):.2f}x (unrealized value)

"""

        # Public market performance if available
        try:
            premium_discount = self.public_markets.calculate_premium_discount()
            if premium_discount:
                letter += f"""**Public Market Performance:**

- **Premium/(Discount) to NAV:** {premium_discount['premium_discount_pct']:.1f}%
- **Shares Outstanding:** {premium_discount['shares_outstanding']:,.0f}
- **Market Capitalization:** ${premium_discount['market_cap']:,.0f}

"""
        except:
            pass

        letter += "---\n\n## Portfolio Review\n\n"

        # Portfolio construction
        analysis = self.portfolio.analyze_portfolio_construction()

        letter += "### Diversification\n\n"
        letter += "Our portfolio maintains strong diversification across vintage years, stages, and sectors.\n\n"

        letter += "**By Vintage Year:**\n\n"
        for vintage, data in sorted(analysis['by_vintage'].items()):
            pct = data['commitment'] / portfolio_summary['total_commitment'] * 100 if portfolio_summary['total_commitment'] > 0 else 0
            letter += f"- **{vintage}:** {data['count']} funds ({pct:.0f}%)\n"

        letter += "\n**By Stage:**\n\n"
        for stage, data in sorted(analysis['by_stage'].items()):
            if data['commitment'] > 0:
                pct = data['commitment'] / portfolio_summary['total_commitment'] * 100 if portfolio_summary['total_commitment'] > 0 else 0
                letter += f"- **{stage}:** {data['count']} funds ({pct:.0f}%)\n"

        letter += "\n**By Sector:**\n\n"
        for sector, data in sorted(analysis['by_sector'].items(), key=lambda x: x[1]['commitment'], reverse=True):
            if data['commitment'] > 0:
                pct = data['commitment'] / portfolio_summary['total_commitment'] * 100 if portfolio_summary['total_commitment'] > 0 else 0
                letter += f"- **{sector}:** {data['count']} funds ({pct:.0f}%)\n"

        # Performance highlights
        letter += "\n### Performance Highlights\n\n"

        top_performers = sorted(portfolio_summary['funds'], key=lambda x: x.get('tvpi', 0), reverse=True)[:3]

        letter += "Our top performing funds this quarter:\n\n"
        for i, fund in enumerate(top_performers, 1):
            letter += f"{i}. **{fund['fund_name']}** (Vintage {fund['vintage_year']})\n"
            letter += f"   - TVPI: {fund['tvpi']:.2f}x\n"
            letter += f"   - DPI: {fund['dpi']:.2f}x | RVPI: {fund['rvpi']:.2f}x\n"
            letter += f"   - Manager: {fund['manager']}\n\n"

        # Portfolio metrics
        funds_above_1x = len([f for f in portfolio_summary['funds'] if f.get('tvpi', 0) > 1.0])
        funds_above_2x = len([f for f in portfolio_summary['funds'] if f.get('tvpi', 0) > 2.0])

        letter += f"**Portfolio Distribution:**\n\n"
        letter += f"- **{funds_above_1x}** of {portfolio_summary['total_funds']} funds ({funds_above_1x/portfolio_summary['total_funds']*100:.0f}%) are above 1.0x\n"
        letter += f"- **{funds_above_2x}** of {portfolio_summary['total_funds']} funds ({funds_above_2x/portfolio_summary['total_funds']*100:.0f}%) are above 2.0x\n"

        # Manager updates
        letter += "\n---\n\n## Manager Updates\n\n"
        letter += f"""### New Commitments

This quarter, we completed due diligence and committed capital to the following managers:

"""

        # Get recently committed managers
        managers = self.manager_crm._load_csv(self.manager_crm.managers_file)
        recent_commits = [m for m in managers if m['pipeline_stage'] == 'Committed']

        if recent_commits:
            for mgr in recent_commits[:3]:
                letter += f"**{mgr['fund_name']}**\n"
                letter += f"- GPs: {mgr['gp_names']}\n"
                letter += f"- Strategy: {mgr['stage_focus']} stage, {mgr['sector_focus']}\n\n"
        else:
            letter += "*No new commitments this quarter. Current pipeline remains robust.*\n\n"

        # Pipeline status
        pipeline_summary = self.manager_crm.get_pipeline_summary()
        letter += "### Pipeline Activity\n\n"
        letter += f"We continue to maintain a healthy manager pipeline with **{pipeline_summary['total']} managers** across various stages:\n\n"
        letter += f"- **Deep Due Diligence:** {pipeline_summary['by_stage'].get('Deep DD', 0)} managers\n"
        letter += f"- **IC Review:** {pipeline_summary['by_stage'].get('IC Review', 0)} managers\n"
        letter += f"- **Screening:** {pipeline_summary['by_stage'].get('Screening', 0)} managers\n"

        # Market commentary
        if market_commentary:
            letter += f"\n---\n\n## Market Commentary\n\n{market_commentary}\n"
        else:
            letter += f"""

---

## Market Commentary

The venture capital market in Q{quarter} {year} continued to show signs of stabilization following the correction of 2022-2023. While fundraising remains challenging for many managers, we believe this environment creates opportunities for disciplined investors to access high-quality funds at more attractive terms.

Key market themes:

- **Valuation Discipline:** Fund managers are applying more rigorous valuation standards
- **Extended Hold Periods:** Exit timelines have lengthened, requiring patient capital
- **AI Investment:** Significant capital flowing to AI/ML infrastructure and applications
- **Sector Rotation:** Continued strength in enterprise software, healthcare IT, and climate tech

We remain focused on our core strategy of investing in emerging managers with differentiated approaches and strong track records.

"""

        # Capital deployment
        letter += "---\n\n## Capital Deployment & Liquidity\n\n"

        deploy_summary = portfolio_summary
        letter += f"""### Deployment Status

- **Total Commitments:** ${deploy_summary['total_commitment']:,.0f}
- **Paid-In Capital:** ${deploy_summary['total_paid_in']:,.0f} ({deploy_summary['total_paid_in']/deploy_summary['total_commitment']*100:.0f}% deployed)
- **Unfunded Commitments:** ${deploy_summary['total_commitment'] - deploy_summary['total_paid_in']:,.0f}

"""

        # Forecast capital calls
        forecast = self.portfolio.forecast_capital_calls(months=12)
        quarterly_forecast = defaultdict(float)

        for call in forecast:
            call_date = datetime.strptime(call['call_date'], '%Y-%m-%d')
            quarter_key = f"Q{(call_date.month - 1) // 3 + 1} {call_date.year}"
            quarterly_forecast[quarter_key] += call['amount']

        letter += "### Capital Call Forecast (Next 12 Months)\n\n"
        letter += "Based on fund deployment pace and remaining commitments, we forecast the following capital calls:\n\n"

        for quarter_key, amount in sorted(quarterly_forecast.items())[:4]:
            letter += f"- **{quarter_key}:** ${amount:,.0f}\n"

        total_12m = sum(quarterly_forecast.values())
        letter += f"\n**Total 12-Month Forecast:** ${total_12m:,.0f}\n"

        # Distribution forecast
        letter += "\n### Distribution Outlook\n\n"
        letter += "We expect distributions to increase as our portfolio funds mature. "
        letter += f"Year-to-date, we have received ${portfolio_summary['total_distributions']:,.0f} in distributions. "
        letter += "Several of our funds are reaching vintage years where distribution activity typically accelerates.\n"

        # Risk management
        letter += "\n---\n\n## Risk Management & Governance\n\n"

        letter += "### Portfolio Risk Overview\n\n"
        letter += f"Our risk management framework monitors concentration, vintage year exposure, liquidity, and correlation risk. "
        letter += f"Current risk assessment:\n\n"
        letter += f"- **Overall Risk Level:** {risk_dashboard['risk_level']}\n"
        letter += f"- **Compliance Status:** {'Compliant' if risk_dashboard['concentration']['status'] == 'COMPLIANT' else 'Monitoring'}\n"
        letter += f"- **Vintage Diversification:** {risk_dashboard['vintage']['diversification_score']} years\n"
        letter += f"- **Liquidity Position:** Strong\n\n"

        if risk_dashboard['concentration']['warnings']:
            letter += "We continue to monitor portfolio concentration and maintain compliance with our investment policy guidelines.\n\n"

        # Looking ahead
        letter += "---\n\n## Looking Ahead\n\n"
        letter += f"""Our priorities for the coming quarter include:

1. **Portfolio Management:** Continue active monitoring of fund performance and manager relationships
2. **New Commitments:** Target 2-3 new fund commitments from our current pipeline
3. **LP Base Growth:** Expand our shareholder base through strategic investor outreach
4. **Value Creation:** Work with portfolio managers on exit preparation and value maximization

We remain confident in our investment strategy and the quality of our manager relationships. The current market environment, while challenging, creates opportunities for disciplined capital deployment at attractive entry points.

Thank you for your continued partnership. As always, please don't hesitate to reach out with questions or to discuss our portfolio in more detail.

---

**Best regards,**

Ken Wallace
Chief Executive Officer
NEWCO

---

## Appendix: Detailed Portfolio Metrics

### Fund-by-Fund Performance

"""

        # Add detailed fund table
        letter += "| Fund Name | Vintage | Stage | Commitment | Paid In | NAV | TVPI | DPI |\n"
        letter += "|-----------|---------|-------|------------|---------|-----|------|-----|\n"

        for fund in sorted(portfolio_summary['funds'], key=lambda x: x['fund_name']):
            letter += f"| {fund['fund_name'][:30]} | {fund['vintage_year']} | {fund['stage'][:8]} | "
            letter += f"${fund['commitment']/1000:.0f}K | ${fund['paid_in']/1000:.0f}K | "
            letter += f"${fund['current_nav']/1000:.0f}K | {fund['tvpi']:.2f}x | {fund['dpi']:.2f}x |\n"

        letter += "\n---\n\n"
        letter += f"*This quarterly letter was generated on {datetime.now().strftime('%B %d, %Y')}.*\n"
        letter += "*For questions or additional information, please contact: investors@newco.com*\n"

        return letter

    def generate_capital_call_notice(self, fund_id, amount, due_date, notes=''):
        """
        Generate capital call notice to LPs

        Args:
            fund_id: Fund making the capital call
            amount: Total amount being called
            due_date: Payment due date
            notes: Additional notes

        Returns:
            Path to generated notice
        """
        # Get fund details
        funds = self.portfolio._load_csv(self.portfolio.funds_file)
        fund = next((f for f in funds if f['fund_id'] == fund_id), None)

        if not fund:
            raise ValueError(f"Fund {fund_id} not found")

        notice = f"""# NEWCO Capital Call Notice

**Date:** {datetime.now().strftime('%B %d, %Y')}
**Fund:** {fund['fund_name']}
**Call Amount:** ${amount:,.2f}
**Due Date:** {due_date}

---

Dear Limited Partners,

This notice is to inform you of a capital call from **{fund['fund_name']}** (the "Fund").

## Call Details

- **Fund Name:** {fund['fund_name']}
- **Manager:** {fund['manager_name']}
- **Vintage Year:** {fund['vintage_year']}
- **Total Call Amount:** ${amount:,.2f}
- **Payment Due Date:** {due_date}

## Your Commitment

Based on your pro-rata share of NEWCO's commitment to this fund, no action is required on your part. NEWCO will fund this capital call from existing cash reserves and credit facilities.

## Fund Update

"""

        # Add fund metrics
        metrics = self.portfolio.get_fund_metrics(fund_id)
        if metrics:
            notice += f"""**Current Fund Metrics:**

- **Total Commitment:** ${metrics['commitment']:,.0f}
- **Paid-In to Date:** ${metrics['paid_in']:,.0f} ({metrics['paid_in']/metrics['commitment']*100:.0f}%)
- **Current NAV:** ${metrics['current_nav']:,.0f}
- **TVPI:** {metrics['tvpi']:.2f}x
- **Distributions:** ${metrics['distributions']:,.0f}

"""

        if notes:
            notice += f"**Manager Notes:**\n\n{notes}\n\n"

        notice += """## Questions?

If you have any questions about this capital call, please contact:

- **Email:** investors@newco.com
- **Phone:** [Contact Number]

---

**NEWCO Management Team**

"""

        # Save notice
        filename = f"capital_call_{fund_id}_{datetime.now().strftime('%Y%m%d')}.md"
        output_path = REPORTS_DIR / filename

        with open(output_path, 'w') as f:
            f.write(notice)

        return output_path

    def generate_distribution_notice(self, fund_id, amount, distribution_date, dist_type='Capital Gain'):
        """
        Generate distribution notice to LPs

        Args:
            fund_id: Fund making distribution
            amount: Distribution amount
            distribution_date: Distribution date
            dist_type: Type of distribution

        Returns:
            Path to generated notice
        """
        # Get fund details
        funds = self.portfolio._load_csv(self.portfolio.funds_file)
        fund = next((f for f in funds if f['fund_id'] == fund_id), None)

        if not fund:
            raise ValueError(f"Fund {fund_id} not found")

        notice = f"""# NEWCO Distribution Notice

**Date:** {datetime.now().strftime('%B %d, %Y')}
**Fund:** {fund['fund_name']}
**Distribution Amount:** ${amount:,.2f}
**Distribution Date:** {distribution_date}
**Type:** {dist_type}

---

Dear Limited Partners,

We are pleased to inform you of a distribution from **{fund['fund_name']}**.

## Distribution Details

- **Fund Name:** {fund['fund_name']}
- **Manager:** {fund['manager_name']}
- **Distribution Amount:** ${amount:,.2f}
- **Distribution Type:** {dist_type}
- **Payment Date:** {distribution_date}

## Pro-Rata Allocation

This distribution will be allocated to NEWCO shareholders on a pro-rata basis according to share ownership as of [record date].

**Per Share Distribution:** [To be calculated based on shares outstanding]

## Fund Performance Update

"""

        # Add fund metrics
        metrics = self.portfolio.get_fund_metrics(fund_id)
        if metrics:
            notice += f"""**Updated Fund Metrics (including this distribution):**

- **Total Paid-In:** ${metrics['paid_in']:,.0f}
- **Total Distributions:** ${metrics['distributions'] + amount:,.0f}
- **Current NAV:** ${metrics['current_nav']:,.0f}
- **Updated DPI:** {(metrics['distributions'] + amount)/metrics['paid_in']:.2f}x
- **Updated TVPI:** {((metrics['distributions'] + amount) + metrics['current_nav'])/metrics['paid_in']:.2f}x

"""

        notice += """## Tax Information

Detailed tax information regarding the character of this distribution (capital gain, return of capital, etc.) will be provided in your annual K-1 tax package.

## Questions?

For questions about this distribution, please contact:

- **Email:** investors@newco.com
- **Phone:** [Contact Number]

---

**NEWCO Management Team**

"""

        # Save notice
        filename = f"distribution_{fund_id}_{datetime.now().strftime('%Y%m%d')}.md"
        output_path = REPORTS_DIR / filename

        with open(output_path, 'w') as f:
            f.write(notice)

        return output_path

    def generate_annual_summary(self, year):
        """
        Generate annual performance summary for LPs

        Args:
            year: Year to summarize

        Returns:
            Path to generated summary
        """
        summary = f"""# NEWCO Annual Performance Summary
## Year Ended December 31, {year}

---

## Executive Summary

This annual summary provides a comprehensive overview of NEWCO's performance and activities for the year ended December 31, {year}.

"""

        portfolio_summary = self.portfolio.get_portfolio_summary()

        summary += f"""### Portfolio Overview

- **Active Fund Investments:** {portfolio_summary['total_funds']}
- **Total Commitments:** ${portfolio_summary['total_commitment']:,.0f}
- **Paid-In Capital:** ${portfolio_summary['total_paid_in']:,.0f}
- **Portfolio NAV:** ${portfolio_summary['total_nav']:,.0f}
- **Cumulative Distributions:** ${portfolio_summary['total_distributions']:,.0f}

### Performance Metrics

- **Portfolio TVPI:** {portfolio_summary.get('portfolio_tvpi', 0):.2f}x
- **Portfolio DPI:** {portfolio_summary.get('portfolio_dpi', 0):.2f}x
- **Portfolio RVPI:** {portfolio_summary.get('portfolio_rvpi', 0):.2f}x

---

## Year in Review

### Capital Activity

"""

        # Calculate year's capital calls and distributions
        calls = self.portfolio._load_csv(self.portfolio.capital_calls_file)
        distributions = self.portfolio._load_csv(self.portfolio.distributions_file)

        year_calls = sum(
            float(call['amount'])
            for call in calls
            if datetime.strptime(call['call_date'], '%Y-%m-%d').year == year and call['status'] == 'Paid'
        )

        year_distributions = sum(
            float(dist['amount'])
            for dist in distributions
            if datetime.strptime(dist['distribution_date'], '%Y-%m-%d').year == year
        )

        summary += f"""**{year} Activity:**

- **Capital Calls:** ${year_calls:,.0f}
- **Distributions Received:** ${year_distributions:,.0f}
- **Net Cash Flow:** ${year_distributions - year_calls:,.0f}

"""

        # New commitments
        ic_decisions = self.manager_crm._load_csv(self.manager_crm.ic_decisions_file)
        year_commitments = [
            ic for ic in ic_decisions
            if datetime.strptime(ic['ic_date'], '%Y-%m-%d').year == year and ic['decision'] == 'Approved'
        ]

        summary += f"### New Fund Commitments\n\n"
        summary += f"In {year}, we completed due diligence and committed capital to **{len(year_commitments)} new funds**:\n\n"

        for ic in year_commitments:
            managers = self.manager_crm._load_csv(self.manager_crm.managers_file)
            manager = next((m for m in managers if m['manager_id'] == ic['manager_id']), None)
            if manager:
                summary += f"- **{manager['fund_name']}** - ${float(ic['commitment_amount']):,.0f}\n"

        summary += f"""

---

## Looking Forward to {year + 1}

As we enter {year + 1}, we remain focused on:

1. **Portfolio Management:** Maximizing returns from our existing fund investments
2. **Strategic Commitments:** Deploying capital to 3-4 high-quality emerging managers
3. **Shareholder Value:** Maintaining strong governance and risk management
4. **Market Leadership:** Positioning NEWCO as the premier liquid access vehicle for emerging VC managers

Thank you for your continued confidence in NEWCO.

---

**Ken Wallace**
Chief Executive Officer
NEWCO

*December 31, {year}*

"""

        # Save summary
        filename = f"annual_summary_{year}.md"
        output_path = REPORTS_DIR / filename

        with open(output_path, 'w') as f:
            f.write(summary)

        return output_path


if __name__ == '__main__':
    # Generate Q1 2026 letter
    generator = LPReportGenerator()
    output_path = generator.generate_quarterly_letter(
        quarter=1,
        year=2026,
        ceo_message="Q1 2026 marked a strong start to the year with continued portfolio appreciation and successful deployment of capital to two new emerging managers.",
        market_commentary="The venture capital market showed increased optimism in Q1 2026, driven by AI infrastructure investments and renewed LP interest in top-tier funds."
    )
    print(f"\n✓ Quarterly letter generated: {output_path}")

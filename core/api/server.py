#!/usr/bin/env python3
"""
NEWCO Platform API Server

Flask REST API that exposes NEWCO CLI data to the React frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
from pathlib import Path

# Add scripts to path
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts"))

# Import all modules
from portfolio_management import PortfolioManager
from manager_crm import ManagerCRM
from public_markets import PublicMarketsEngine
from team_management import TeamManager
from governance import InstitutionalGovernance
from financial_modeling import FinancialModeler
from competitive_intelligence import CompetitiveIntelligence
from risk_management import RiskManager
from llm_service import LLMService

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize modules
portfolio = PortfolioManager()
managers = ManagerCRM()
public_markets = PublicMarketsEngine()
team = TeamManager()
governance = InstitutionalGovernance()
finance = FinancialModeler()
intel = CompetitiveIntelligence()
risk = RiskManager()
llm = LLMService()


# ═══════════════════════════════════════════════════════
# PORTFOLIO ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.route('/api/portfolio/summary', methods=['GET'])
def get_portfolio_summary():
    """Get portfolio summary metrics"""
    summary = portfolio.get_portfolio_summary()
    return jsonify(summary)


@app.route('/api/portfolio/funds', methods=['GET'])
def get_funds():
    """Get all funds"""
    funds = portfolio._load_csv(portfolio.funds_file)

    # Calculate basic performance metrics for each fund
    enriched_funds = []
    for fund in funds:
        # Calculate TVPI
        committed = float(fund.get('commitment_amount', 0))
        called = float(fund.get('total_called', 0))
        distributed = float(fund.get('total_distributed', 0))
        nav = float(fund.get('current_nav', 0))

        tvpi = (distributed + nav) / called if called > 0 else 0
        dpi = distributed / called if called > 0 else 0
        rvpi = nav / called if called > 0 else 0

        enriched_funds.append({
            **fund,
            'tvpi': f"{tvpi:.2f}",
            'dpi': f"{dpi:.2f}",
            'rvpi': f"{rvpi:.2f}"
        })

    return jsonify(enriched_funds)


@app.route('/api/portfolio/funds/<fund_id>', methods=['GET'])
def get_fund_detail(fund_id):
    """Get single fund detail"""
    funds = portfolio._load_csv(portfolio.funds_file)
    fund = next((f for f in funds if f['fund_id'] == fund_id), None)

    if not fund:
        return jsonify({'error': 'Fund not found'}), 404

    # Calculate performance metrics
    committed = float(fund.get('commitment_amount', 0))
    called = float(fund.get('total_called', 0))
    distributed = float(fund.get('total_distributed', 0))
    nav = float(fund.get('current_nav', 0))

    tvpi = (distributed + nav) / called if called > 0 else 0
    dpi = distributed / called if called > 0 else 0
    rvpi = nav / called if called > 0 else 0

    # Add capital call history (if file exists)
    fund_calls = []
    if portfolio.capital_calls_file.exists():
        calls = portfolio._load_csv(portfolio.capital_calls_file)
        fund_calls = [c for c in calls if c['fund_id'] == fund_id]

    # Add distribution history (if file exists)
    fund_distributions = []
    if portfolio.distributions_file.exists():
        distributions = portfolio._load_csv(portfolio.distributions_file)
        fund_distributions = [d for d in distributions if d['fund_id'] == fund_id]

    # Add portfolio companies (if file exists)
    fund_companies = []
    portfolio_companies_file = BASE_DIR / "data" / "portfolio_companies.csv"
    if portfolio_companies_file.exists():
        import csv
        with open(portfolio_companies_file, 'r') as f:
            reader = csv.DictReader(f)
            fund_companies = [c for c in reader if c['fund_id'] == fund_id]

    return jsonify({
        **fund,
        'tvpi': f"{tvpi:.2f}",
        'dpi': f"{dpi:.2f}",
        'rvpi': f"{rvpi:.2f}",
        'capital_calls': fund_calls,
        'distributions': fund_distributions,
        'portfolio_companies': fund_companies
    })


@app.route('/api/portfolio/performance', methods=['GET'])
def get_portfolio_performance():
    """Get portfolio-level performance"""
    summary = portfolio.get_portfolio_summary()
    return jsonify(summary)


# ═══════════════════════════════════════════════════════
# MANAGER ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.route('/api/managers', methods=['GET'])
def get_managers():
    """Get all managers"""
    managers_list = managers._load_csv(managers.managers_file)

    # Optionally filter by status
    status = request.args.get('status')
    if status:
        managers_list = [m for m in managers_list if m['status'] == status]

    return jsonify(managers_list)


@app.route('/api/managers/<manager_id>', methods=['GET'])
def get_manager_detail(manager_id):
    """Get manager detail"""
    mgr_data = managers._load_csv(managers.managers_file)
    manager = next((m for m in mgr_data if m['manager_id'] == manager_id), None)

    if not manager:
        return jsonify({'error': 'Manager not found'}), 404

    # Add interactions
    interactions = managers._load_csv(managers.interactions_file)
    mgr_interactions = [i for i in interactions if i['manager_id'] == manager_id]

    # Add portfolio companies
    portfolio_cos = managers._load_csv(managers.portfolio_cos_file)
    mgr_cos = [pc for pc in portfolio_cos if pc['manager_id'] == manager_id]

    return jsonify({
        **manager,
        'interactions': mgr_interactions,
        'portfolio_companies': mgr_cos
    })


@app.route('/api/managers/pipeline', methods=['GET'])
def get_manager_pipeline():
    """Get manager pipeline"""
    pipeline_stats = managers.get_pipeline_summary()
    return jsonify(pipeline_stats)


# ═══════════════════════════════════════════════════════
# PUBLIC MARKETS ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.route('/api/public/ticker', methods=['GET'])
def get_ticker_status():
    """Get current ticker status"""
    ticker_data = public_markets._load_csv(public_markets.ticker_file)
    latest = ticker_data[-1] if ticker_data else {}

    nav_data = public_markets._load_csv(public_markets.nav_file)
    latest_nav = nav_data[-1] if nav_data else {}

    return jsonify({
        'ticker': 'NEWCO',
        'price': float(latest.get('close', 0)),
        'volume': int(latest.get('volume', 0)),
        'nav': float(latest_nav.get('nav_per_share', 0)),
        'premium_discount': float(latest_nav.get('premium_discount_pct', 0)),
        'date': latest.get('date', '')
    })


@app.route('/api/public/nav-history', methods=['GET'])
def get_nav_history():
    """Get NAV history"""
    nav_data = public_markets._load_csv(public_markets.nav_file)
    return jsonify(nav_data)


@app.route('/api/public/shareholders', methods=['GET'])
def get_shareholders():
    """Get shareholder list"""
    shareholders = public_markets._load_csv(public_markets.shareholders_file)
    return jsonify(shareholders)


# ═══════════════════════════════════════════════════════
# TEAM ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.route('/api/team/members', methods=['GET'])
def get_team_members():
    """Get team members"""
    members = team._load_csv(team.team_members_file)
    return jsonify(members)


@app.route('/api/team/workload', methods=['GET'])
def get_team_workload():
    """Get team workload"""
    workload_data = team.get_team_workload()
    return jsonify(workload_data)


@app.route('/api/team/capacity', methods=['GET'])
def get_team_capacity():
    """Get team capacity analysis"""
    capacity = team.capacity_analysis()
    return jsonify(capacity)


@app.route('/api/team/ic-votes', methods=['GET'])
def get_ic_votes():
    """Get IC voting history"""
    votes = team._load_csv(team.ic_votes_file)

    # Enrich with member names
    members = team._load_csv(team.team_members_file)
    for vote in votes:
        member = next((m for m in members if m['member_id'] == vote['member_id']), None)
        if member:
            vote['member_name'] = member['name']

    return jsonify(votes)


# ═══════════════════════════════════════════════════════
# GOVERNANCE ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.route('/api/governance/ic-committee', methods=['GET'])
def get_ic_committee():
    """Get IC committee composition"""
    ic_members = governance.get_ic_committee()
    return jsonify(ic_members)


@app.route('/api/governance/ic-meetings', methods=['GET'])
def get_ic_meetings():
    """Get IC meeting history"""
    meetings = governance._load_csv(governance.ic_meetings_file)
    return jsonify(meetings)


@app.route('/api/governance/coinvest-pipeline', methods=['GET'])
def get_coinvest_pipeline():
    """Get co-invest pipeline"""
    coinvest = governance._load_csv(governance.coinvest_decisions_file)

    # Optionally filter by tier
    tier = request.args.get('tier')
    if tier:
        coinvest = [c for c in coinvest if c['tier'] == tier]

    return jsonify(coinvest)


@app.route('/api/governance/manager-contacts', methods=['GET'])
def get_manager_contacts():
    """Get manager relationship tracking"""
    contacts = governance._load_csv(governance.manager_contacts_file)

    # Optionally filter by manager
    manager_id = request.args.get('manager_id')
    if manager_id:
        contacts = [c for c in contacts if c['manager_id'] == manager_id]

    return jsonify(contacts)


@app.route('/api/governance/calendar', methods=['GET'])
def get_governance_calendar():
    """Get governance calendar"""
    events = governance._load_csv(governance.governance_calendar_file)

    # Filter for upcoming events
    days = int(request.args.get('days', 90))
    # TODO: Add date filtering logic

    return jsonify(events)


# ═══════════════════════════════════════════════════════
# FINANCIAL MODELING ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.route('/api/finance/scenarios', methods=['GET'])
def get_scenarios():
    """Get scenario analysis"""
    scenarios = finance.scenario_analysis()
    return jsonify(scenarios)


@app.route('/api/finance/projections', methods=['GET'])
def get_cash_flow_projections():
    """Get cash flow projections"""
    years = int(request.args.get('years', 5))
    projections = finance.project_cashflow(years=years)
    return jsonify(projections)


@app.route('/api/finance/budget', methods=['GET'])
def get_budget():
    """Get budget data"""
    budget = finance._load_csv(finance.budget_file)
    return jsonify(budget)


@app.route('/api/finance/actuals', methods=['GET'])
def get_actuals():
    """Get actual spending"""
    actuals = finance._load_csv(finance.actuals_file)
    return jsonify(actuals)


@app.route('/api/finance/variance', methods=['GET'])
def get_variance_analysis():
    """Get budget variance analysis"""
    month = request.args.get('month')
    if not month:
        return jsonify({'error': 'Month parameter required'}), 400

    variance = finance.budget_variance_analysis(month)
    return jsonify(variance)


# ═══════════════════════════════════════════════════════
# COMPETITIVE INTELLIGENCE ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.route('/api/intel/competitors', methods=['GET'])
def get_competitors():
    """Get competitor landscape"""
    landscape = intel.get_competitor_landscape()
    return jsonify(landscape)


@app.route('/api/intel/manager-universe', methods=['GET'])
def get_manager_universe():
    """Get manager universe"""
    universe = intel._load_csv(intel.manager_universe_file)

    # Optionally filter by status
    status = request.args.get('status')
    if status:
        universe = [m for m in universe if m['our_status'] == status]

    return jsonify(universe)


@app.route('/api/intel/fee-benchmarks', methods=['GET'])
def get_fee_benchmarks():
    """Get fee benchmarks"""
    fees = intel._load_csv(intel.fee_benchmarks_file)
    return jsonify(fees)


@app.route('/api/intel/lp-overlap', methods=['GET'])
def get_lp_overlap():
    """Get LP overlap analysis"""
    overlap = intel._load_csv(intel.lp_overlap_file)
    return jsonify(overlap)


# ═══════════════════════════════════════════════════════
# RISK MANAGEMENT ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.route('/api/risk/dashboard', methods=['GET'])
def get_risk_dashboard():
    """Get risk dashboard"""
    dashboard = risk.get_risk_dashboard()
    return jsonify(dashboard)


@app.route('/api/risk/concentration', methods=['GET'])
def get_concentration_risk():
    """Get concentration risk analysis"""
    concentration = risk.analyze_concentration_risk()
    return jsonify(concentration)


@app.route('/api/risk/liquidity', methods=['GET'])
def get_liquidity_risk():
    """Get liquidity risk analysis"""
    liquidity = risk.check_liquidity_risk()
    return jsonify(liquidity)


# ═══════════════════════════════════════════════════════
# PORTFOLIO COMPANIES ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.route('/api/portfolio-companies', methods=['GET'])
def get_portfolio_companies():
    """Get all portfolio companies"""
    from pathlib import Path
    import csv

    portfolio_companies_file = BASE_DIR / "data" / "portfolio_companies.csv"

    if not portfolio_companies_file.exists():
        return jsonify([])

    companies = []
    with open(portfolio_companies_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(row)

    # Optional filters
    fund_id = request.args.get('fund_id')
    sector = request.args.get('sector')
    status = request.args.get('status')

    if fund_id:
        companies = [c for c in companies if c['fund_id'] == fund_id]
    if sector:
        companies = [c for c in companies if c['sector'] == sector]
    if status:
        companies = [c for c in companies if c['status'] == status]

    return jsonify(companies)


@app.route('/api/portfolio-companies/<company_id>', methods=['GET'])
def get_portfolio_company_detail(company_id):
    """Get single portfolio company detail"""
    from pathlib import Path
    import csv

    portfolio_companies_file = BASE_DIR / "data" / "portfolio_companies.csv"

    if not portfolio_companies_file.exists():
        return jsonify({'error': 'Portfolio companies file not found'}), 404

    with open(portfolio_companies_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['company_id'] == company_id:
                return jsonify(row)

    return jsonify({'error': 'Company not found'}), 404


@app.route('/api/portfolio-companies/fund/<fund_id>', methods=['GET'])
def get_fund_portfolio_companies(fund_id):
    """Get all portfolio companies for a specific fund"""
    from pathlib import Path
    import csv

    portfolio_companies_file = BASE_DIR / "data" / "portfolio_companies.csv"

    if not portfolio_companies_file.exists():
        return jsonify([])

    companies = []
    with open(portfolio_companies_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['fund_id'] == fund_id:
                companies.append(row)

    return jsonify(companies)


@app.route('/api/portfolio-companies/stats', methods=['GET'])
def get_portfolio_companies_stats():
    """Get portfolio companies statistics"""
    from pathlib import Path
    import csv
    from collections import Counter

    portfolio_companies_file = BASE_DIR / "data" / "portfolio_companies.csv"

    if not portfolio_companies_file.exists():
        return jsonify({'error': 'Portfolio companies file not found'}), 404

    companies = []
    with open(portfolio_companies_file, 'r') as f:
        reader = csv.DictReader(f)
        companies = list(reader)

    # Calculate statistics
    total_companies = len(companies)
    by_sector = Counter(c['sector'] for c in companies)
    by_stage = Counter(c['stage'] for c in companies)
    by_status = Counter(c['status'] for c in companies)

    # Count exits
    exits = [c for c in companies if c['exit_date']]
    total_exit_value = sum(float(c['valuation_estimate']) for c in exits if c['valuation_estimate'])

    # Count by fund
    by_fund = Counter(c['fund_id'] for c in companies)

    return jsonify({
        'total_companies': total_companies,
        'by_sector': dict(by_sector),
        'by_stage': dict(by_stage),
        'by_status': dict(by_status),
        'total_exits': len(exits),
        'total_exit_value': total_exit_value,
        'companies_per_fund': dict(by_fund)
    })


# ═══════════════════════════════════════════════════════
# LLM / AI ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.route('/api/llm/models', methods=['GET'])
def get_llm_models():
    """Get available LLM models"""
    models = llm.list_models()
    return jsonify({
        'success': True,
        'models': models,
        'default_model': llm.config.get('default_model', 'deepseek-r1')
    })


@app.route('/api/llm/chat', methods=['POST'])
def llm_chat():
    """Chat with LLM model"""
    data = request.json
    prompt = data.get('prompt')
    model = data.get('model')
    context = data.get('context')

    if not prompt:
        return jsonify({'success': False, 'error': 'Prompt is required'}), 400

    result = llm.chat(prompt=prompt, model=model, context=context)
    return jsonify(result)


@app.route('/api/llm/analyze/investment', methods=['POST'])
def analyze_investment():
    """Analyze an investment opportunity"""
    data = request.json
    company_name = data.get('company_name')
    company_data = data.get('company_data', {})
    model = data.get('model', 'deepseek-r1')

    if not company_name:
        return jsonify({'success': False, 'error': 'company_name is required'}), 400

    result = llm.analyze_investment(company_name, company_data, model)
    return jsonify(result)


@app.route('/api/llm/analyze/manager', methods=['POST'])
def analyze_manager():
    """Analyze a fund manager"""
    data = request.json
    manager_name = data.get('manager_name')
    manager_data = data.get('manager_data', {})
    model = data.get('model', 'deepseek-r1')

    if not manager_name:
        return jsonify({'success': False, 'error': 'manager_name is required'}), 400

    result = llm.analyze_manager(manager_name, manager_data, model)
    return jsonify(result)


@app.route('/api/llm/generate/email', methods=['POST'])
def generate_email():
    """Generate an email"""
    data = request.json
    contact_data = data.get('contact_data', {})
    email_type = data.get('email_type', 'general')
    context = data.get('context')
    model = data.get('model', 'phi4')

    result = llm.generate_email(contact_data, email_type, context, model)
    return jsonify(result)


@app.route('/api/llm/summarize/market', methods=['POST'])
def summarize_market():
    """Summarize market data"""
    data = request.json
    market_data = data.get('market_data', {})
    model = data.get('model', 'qwen2.5')

    result = llm.summarize_market_data(market_data, model)
    return jsonify(result)


@app.route('/api/llm/extract/insights', methods=['POST'])
def extract_insights():
    """Extract insights from text"""
    data = request.json
    text = data.get('text')
    task_type = data.get('task_type', 'general')
    model = data.get('model', 'mistral')

    if not text:
        return jsonify({'success': False, 'error': 'text is required'}), 400

    result = llm.extract_insights_from_text(text, task_type, model)
    return jsonify(result)


# ═══════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.1.0',
        'modules': {
            'portfolio': True,
            'managers': True,
            'public_markets': True,
            'team': True,
            'governance': True,
            'finance': True,
            'intel': True,
            'risk': True,
            'llm': True
        },
        'llm_models': len(llm.AVAILABLE_MODELS),
        'default_llm': llm.config.get('default_model', 'deepseek-r1')
    })


# ═══════════════════════════════════════════════════════
# RUN SERVER
# ═══════════════════════════════════════════════════════

if __name__ == '__main__':
    print("Starting NEWCO Platform API Server...")
    print("API available at: http://localhost:5001")
    print("Health check: http://localhost:5001/api/health")
    app.run(host='0.0.0.0', port=5001, debug=True)

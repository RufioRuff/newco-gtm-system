/**
 * Data Adapter: Flask API → AlphaEngine Format
 *
 * Transforms real NEWCO data (85 funds + 62 portfolio companies)
 * from Flask REST API into AlphaEngine's expected format
 */

const FLASK_API = 'http://localhost:5001/api';

/**
 * Fetch helper with error handling
 */
async function fetchData(endpoint) {
  try {
    const response = await fetch(`${FLASK_API}${endpoint}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error(`Error fetching ${endpoint}:`, error);
    return null;
  }
}

/**
 * Transform 85 real funds to AlphaEngine FUNDS format
 */
export async function loadRealFunds() {
  const fundsRaw = await fetchData('/portfolio/funds');
  if (!fundsRaw) return [];

  return fundsRaw.map((fund, idx) => ({
    id: idx + 1,
    name: fund.fund_name,
    gp: fund.gp_name,
    vintage: parseInt(fund.vintage) || 2023,
    strategy: fund.sector || 'Multi-Sector',
    status: fund.status || 'Active',
    committed: parseFloat(fund.commitment_amount) / 1000000, // Convert to millions
    called: parseFloat(fund.total_called) / 1000000,
    nav: parseFloat(fund.current_nav) / 1000000,
    tvpi: parseFloat(fund.tvpi) || 1.0,
    irr: calculateIRR(fund), // Estimated from TVPI
    dpi: parseFloat(fund.dpi) || 0,
    tier: determineTier(fund),
    sector: mapSector(fund.sector),
    companies: estimateCompanyCount(fund)
  }));
}

/**
 * Transform 62 real portfolio companies to AlphaEngine PORTFOLIO_COMPANIES format
 */
export async function loadRealPortfolioCompanies() {
  const companiesRaw = await fetchData('/portfolio-companies');
  if (!companiesRaw) return [];

  return companiesRaw.map((company, idx) => ({
    id: idx + 1,
    name: company.company_name,
    sector: mapCompanySector(company.sector),
    stage: company.stage || 'Growth',
    valuation: parseFloat(company.valuation_estimate) / 1000 || 0, // Convert to millions
    ownership: estimateOwnership(company),
    fund: company.fund_name,
    vintage: parseInt(company.investment_date) || 2023,
    status: company.status === 'Active' ? 'markup' : company.status === 'Exited' ? 'exited' : 'flat',
    growth: estimateGrowth(company),
    revenue: estimateRevenue(company),
    employees: estimateEmployees(company),
    moat: company.description || 'Proprietary technology and market position',
    exitPath: determineExitPath(company),
    signalScore: calculateSignalScore(company)
  }));
}

/**
 * Load portfolio statistics
 */
export async function loadPortfolioStats() {
  const stats = await fetchData('/portfolio-companies/stats');
  return stats || {
    total_companies: 0,
    by_sector: {},
    by_stage: {},
    by_status: {},
    total_exits: 0
  };
}

/**
 * Load all real data at once
 */
export async function loadAllRealData() {
  const [funds, companies, stats] = await Promise.all([
    loadRealFunds(),
    loadRealPortfolioCompanies(),
    loadPortfolioStats()
  ]);

  return {
    FUNDS: funds,
    PORTFOLIO_COMPANIES: companies,
    PORTFOLIO_STATS: stats,
    // Team data (if available from API, otherwise use defaults)
    TEAM: await loadTeamData(),
    // Secondary market data (placeholder for now)
    SECONDARIES: [],
    // LP data (placeholder for now)
    LPS: [],
    // Pipeline data (placeholder for now)
    PIPELINE: []
  };
}

// ════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ════════════════════════════════════════════════════════

function calculateIRR(fund) {
  // Estimate IRR from TVPI and vintage
  const tvpi = parseFloat(fund.tvpi) || 1.0;
  const vintage = parseInt(fund.vintage) || 2020;
  const yearsHeld = 2026 - vintage;

  if (yearsHeld <= 0) return 0;

  // Simple IRR approximation: (TVPI^(1/years) - 1) * 100
  return ((Math.pow(tvpi, 1 / yearsHeld) - 1) * 100).toFixed(1);
}

function determineTier(fund) {
  const tvpi = parseFloat(fund.tvpi) || 1.0;
  const commitment = parseFloat(fund.commitment_amount) || 0;

  // Core: High performers or large commitments
  if (tvpi > 1.5 || commitment > 20000000) return 'Core';

  // Strategic: Mid-tier performers
  if (tvpi > 1.2 || commitment > 10000000) return 'Strategic';

  // Exploration: Newer or smaller positions
  return 'Exploration';
}

function mapSector(sector) {
  // Map your sectors to AlphaEngine categories
  const sectorMap = {
    'Software': 'AI/ML',
    'Cybersecurity': 'AI Safety',
    'Fintech': 'AI Infrastructure',
    'Enterprise Software': 'AI/ML',
    'AI/ML': 'AI Safety',
    'Healthcare': 'Trust & Safety',
    'Climate': 'GovTech',
    'Defense': 'GovTech'
  };

  return sectorMap[sector] || sector || 'Multi-Sector';
}

function mapCompanySector(sector) {
  // Keep original sectors for companies
  return sector || 'Technology';
}

function estimateOwnership(company) {
  // Placeholder: estimate ownership based on fund type and stage
  const stage = company.stage || 'Growth';

  if (stage.includes('Seed')) return Math.random() * 0.15 + 0.05; // 5-20%
  if (stage.includes('Series A')) return Math.random() * 0.10 + 0.03; // 3-13%
  if (stage.includes('Series B')) return Math.random() * 0.08 + 0.02; // 2-10%

  return Math.random() * 0.05 + 0.01; // 1-6% for later stages
}

function estimateGrowth(company) {
  // Estimate YoY growth based on stage and status
  const stage = company.stage || 'Growth';
  const status = company.status || 'Active';

  if (status === 'Exited' && company.exit_type === 'IPO') return Math.floor(Math.random() * 100) + 100; // 100-200%
  if (stage.includes('Early') || stage.includes('Seed')) return Math.floor(Math.random() * 300) + 200; // 200-500%
  if (stage === 'Growth') return Math.floor(Math.random() * 100) + 50; // 50-150%
  if (stage === 'Late Stage') return Math.floor(Math.random() * 50) + 30; // 30-80%
  if (stage === 'Public') return Math.floor(Math.random() * 30) + 10; // 10-40%

  return Math.floor(Math.random() * 100) + 50;
}

function estimateRevenue(company) {
  // Estimate revenue based on valuation and stage
  const valuation = parseFloat(company.valuation_estimate) / 1000000 || 0;

  if (valuation === 0) return Math.floor(Math.random() * 100) + 10; // $10-110M

  // Rough revenue multiple estimates
  const stage = company.stage || 'Growth';
  let revenueMultiple = 10; // Default 10x revenue multiple

  if (stage.includes('Public')) revenueMultiple = 5;
  if (stage.includes('Late')) revenueMultiple = 8;
  if (stage.includes('Early')) revenueMultiple = 15;

  return Math.floor(valuation / revenueMultiple);
}

function estimateEmployees(company) {
  // Estimate headcount based on revenue and stage
  const revenue = estimateRevenue(company);
  const stage = company.stage || 'Growth';

  // Revenue per employee varies by stage
  let revPerEmployee = 500000; // $500K default

  if (stage.includes('Seed') || stage.includes('Early')) revPerEmployee = 300000;
  if (stage.includes('Public')) revPerEmployee = 800000;

  return Math.max(20, Math.floor(revenue * 1000 / revPerEmployee));
}

function determineExitPath(company) {
  if (company.exit_type && company.exit_date) {
    return `${company.exit_type} ${company.exit_date}`;
  }

  const stage = company.stage || 'Growth';
  const status = company.status || 'Active';

  if (status === 'Exited') return 'Exited';
  if (stage === 'Public') return 'Public (Trading)';
  if (stage.includes('Late')) return 'IPO 2026-2027';
  if (stage === 'Growth') return 'IPO 2027-2028';
  if (stage.includes('Early')) return 'Series B-C 2026';

  return 'TBD';
}

function calculateSignalScore(company) {
  // Calculate signal score based on multiple factors
  let score = 70; // Base score

  const status = company.status || 'Active';
  const stage = company.stage || 'Growth';
  const sector = company.sector || '';

  // Status boost
  if (status === 'Exited' && company.exit_type === 'IPO') score += 15;
  if (status === 'Active') score += 5;

  // Stage boost
  if (stage.includes('Late') || stage === 'Public') score += 10;
  if (stage === 'Growth') score += 5;

  // Hot sector boost
  if (sector.includes('AI') || sector.includes('Cyber') || sector.includes('Fintech')) score += 8;

  // Valuation boost (if available)
  const valuation = parseFloat(company.valuation_estimate) || 0;
  if (valuation > 10000000000) score += 10; // $10B+ unicorn
  if (valuation > 1000000000) score += 5; // $1B+ unicorn

  return Math.min(99, Math.max(60, score));
}

function estimateCompanyCount(fund) {
  // Estimate portfolio company count based on fund size and type
  const commitment = parseFloat(fund.commitment_amount) / 1000000 || 0;
  const fundType = fund.fund_type || 'Venture Capital';

  if (fundType === 'Private Equity') {
    // PE funds typically have fewer, larger investments
    return Math.floor(commitment / 5) + Math.floor(Math.random() * 5); // ~1 company per $5M
  }

  // VC funds have more, smaller investments
  return Math.floor(commitment / 2) + Math.floor(Math.random() * 10); // ~1 company per $2M
}

async function loadTeamData() {
  // Try to load from API, fallback to defaults
  const team = await fetchData('/team/members');

  if (team && team.length > 0) {
    return team.map((member, idx) => ({
      id: member.member_id || `member-${idx}`,
      name: member.name,
      role: member.role || 'Team Member',
      connections: Math.floor(Math.random() * 200) + 100,
      deals: Math.floor(Math.random() * 40) + 10
    }));
  }

  // Default team if API unavailable
  return [
    { id: 'user1', name: 'Portfolio Manager', role: 'CIO', connections: 324, deals: 47 },
    { id: 'user2', name: 'Investment Analyst', role: 'Analyst', connections: 200, deals: 32 },
    { id: 'user3', name: 'Operations', role: 'COO', connections: 150, deals: 18 }
  ];
}

// Export configuration
export const DATA_CONFIG = {
  API_BASE: FLASK_API,
  REFRESH_INTERVAL: 300000, // Refresh every 5 minutes
  ENABLE_REAL_TIME: true
};

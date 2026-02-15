#!/usr/bin/env node

// ════════════════════════════════════════════════════════
// Load Data from Flask API to Supabase
// ════════════════════════════════════════════════════════

const { createClient } = require('@supabase/supabase-js');
// Using native fetch (Node 18+)

// Configuration
const SUPABASE_URL = process.env.SUPABASE_URL || 'YOUR_SUPABASE_URL';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || 'YOUR_SERVICE_KEY';
const FLASK_API_URL = process.env.FLASK_API_URL || 'http://localhost:5001/api';

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

async function fetchFromFlask(endpoint) {
    try {
        const response = await fetch(`${FLASK_API_URL}${endpoint}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error.message);
        return null;
    }
}

function determineTier(fund) {
    const tvpi = parseFloat(fund.tvpi) || 0;
    const commitment = parseFloat(fund.commitment_amount) || 0;
    if (tvpi > 1.5 || commitment > 20000000) return 'Core';
    if (tvpi > 1.2 || commitment > 10000000) return 'Strategic';
    return 'Exploration';
}

async function loadFunds() {
    console.log('\n📊 Loading funds from Flask API...');

    const fundsData = await fetchFromFlask('/portfolio/funds');
    if (!fundsData) {
        console.error('❌ Failed to fetch funds');
        return;
    }

    console.log(`Found ${fundsData.length} funds`);

    // Transform and insert
    const fundsToInsert = fundsData.map(fund => ({
        fund_name: fund.fund_name,
        gp_name: fund.gp_name,
        vintage: parseInt(fund.vintage) || new Date().getFullYear(),
        fund_type: fund.fund_type,
        sector: fund.sector,
        status: fund.status || 'Active',
        commitment_amount: parseFloat(fund.commitment_amount) || 0,
        total_called: parseFloat(fund.total_called) || 0,
        total_distributed: parseFloat(fund.total_distributed) || 0,
        current_nav: parseFloat(fund.current_nav) || 0,
        tvpi: parseFloat(fund.tvpi) || 1.0,
        dpi: parseFloat(fund.dpi) || 0.0,
        rvpi: parseFloat(fund.rvpi) || 1.0,
        irr: parseFloat(fund.irr) || null,
        tier: determineTier(fund),
        relationship_strength: Math.floor(Math.random() * 40) + 60, // 60-100
        last_contact_date: new Date().toISOString().split('T')[0]
    }));

    const { data, error } = await supabase
        .from('funds')
        .insert(fundsToInsert)
        .select();

    if (error) {
        console.error('❌ Error inserting funds:', error.message);
    } else {
        console.log(`✅ Successfully loaded ${data.length} funds`);
    }

    return data;
}

async function loadPortfolioCompanies(fundIdMap) {
    console.log('\n🏢 Loading portfolio companies from Flask API...');

    const companiesData = await fetchFromFlask('/portfolio-companies');
    if (!companiesData) {
        console.error('❌ Failed to fetch companies');
        return;
    }

    console.log(`Found ${companiesData.length} companies`);

    // Transform and insert
    const companiesToInsert = companiesData.map(company => ({
        company_name: company.company_name,
        fund_id: fundIdMap[company.fund_name] || null,
        fund_name: company.fund_name,
        gp_name: company.gp_name,
        sector: company.sector,
        stage: company.stage,
        status: company.status === 'Active' ? 'Active' : 'Exited',
        investment_date: company.investment_date || null,
        exit_date: company.exit_date || null,
        exit_type: company.exit_type || null,
        valuation_estimate: parseFloat(company.valuation_estimate) || null,
        ownership_pct: Math.random() * 0.15,
        signal_score: Math.floor(Math.random() * 40) + 60, // 60-100
        momentum: Math.random() > 0.6 ? 'up' : Math.random() > 0.5 ? 'flat' : 'down',
        employees: Math.floor(Math.random() * 2000) + 100,
        revenue_estimate: Math.floor(Math.random() * 1000) + 50,
        exit_timeline_months: company.status === 'Active' ? Math.floor(Math.random() * 36) + 6 : null,
        description: company.description || ''
    }));

    const { data, error } = await supabase
        .from('portfolio_companies')
        .insert(companiesToInsert)
        .select();

    if (error) {
        console.error('❌ Error inserting companies:', error.message);
    } else {
        console.log(`✅ Successfully loaded ${data.length} portfolio companies`);
    }
}

async function generateMockDealFlow(fundIdMap) {
    console.log('\n💼 Generating sample deal flow...');

    const sectors = ['AI/ML', 'Cybersecurity', 'Fintech', 'Climate Tech', 'Enterprise SaaS'];
    const stages = ['Series A', 'Series B', 'Series C', 'Growth'];
    const gps = Object.keys(fundIdMap).slice(0, 10);

    const deals = Array.from({ length: 15 }, (_, i) => ({
        company_name: `${['Quantum', 'Nexus', 'Apex', 'Zenith', 'Vertex', 'Helix', 'Prism'][i % 7]} ${['AI', 'Security', 'Labs', 'Technologies', 'Systems'][Math.floor(i / 2) % 5]}`,
        sector: sectors[Math.floor(Math.random() * sectors.length)],
        stage: stages[Math.floor(Math.random() * stages.length)],
        check_size: Math.floor(Math.random() * 5) + 1,
        gp_name: gps[Math.floor(Math.random() * gps.length)],
        fund_id: Object.values(fundIdMap)[Math.floor(Math.random() * 10)],
        timeline_days: Math.floor(Math.random() * 45) + 7,
        co_invest_rights: Math.random() > 0.5,
        deal_score: Math.floor(Math.random() * 30) + 70,
        date_shared: new Date(Date.now() - Math.random() * 14 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        status: 'Active'
    }));

    const { data, error } = await supabase
        .from('deal_flow')
        .insert(deals)
        .select();

    if (error) {
        console.error('❌ Error inserting deal flow:', error.message);
    } else {
        console.log(`✅ Successfully generated ${data.length} deal flow opportunities`);
    }
}

async function main() {
    console.log('🚀 Starting data load to Supabase...\n');
    console.log(`Flask API: ${FLASK_API_URL}`);
    console.log(`Supabase URL: ${SUPABASE_URL}\n`);

    // Load funds first
    const funds = await loadFunds();

    if (!funds || funds.length === 0) {
        console.error('\n❌ No funds loaded. Aborting.');
        process.exit(1);
    }

    // Create fund name -> ID map for companies
    const fundIdMap = {};
    funds.forEach(fund => {
        fundIdMap[fund.fund_name] = fund.id;
    });

    // Load companies
    await loadPortfolioCompanies(fundIdMap);

    // Generate sample deal flow
    await generateMockDealFlow(fundIdMap);

    console.log('\n✅ Data load complete!\n');
    console.log('📊 Summary:');
    console.log(`   - Funds: ${funds.length}`);
    console.log(`   - Portfolio companies: loaded from Flask API`);
    console.log(`   - Deal flow: 15 sample opportunities`);
    console.log('\n🎉 Your Intelligence LP Platform is ready!');
}

// Run
main().catch(error => {
    console.error('\n❌ Fatal error:', error);
    process.exit(1);
});

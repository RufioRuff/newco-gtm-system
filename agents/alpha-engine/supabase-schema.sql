-- ════════════════════════════════════════════════════════
-- NEWCO V10 Intelligence LP Platform - Supabase Schema
-- ════════════════════════════════════════════════════════

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ════════════════════════════════════════════════════════
-- FUNDS TABLE
-- ════════════════════════════════════════════════════════
CREATE TABLE public.funds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fund_name TEXT NOT NULL,
    gp_name TEXT NOT NULL,
    vintage INTEGER NOT NULL,
    fund_type TEXT,
    sector TEXT,
    status TEXT DEFAULT 'Active',
    commitment_amount DECIMAL(15,2) NOT NULL,
    total_called DECIMAL(15,2) DEFAULT 0,
    total_distributed DECIMAL(15,2) DEFAULT 0,
    current_nav DECIMAL(15,2) DEFAULT 0,
    tvpi DECIMAL(8,4) DEFAULT 1.0,
    dpi DECIMAL(8,4) DEFAULT 0.0,
    rvpi DECIMAL(8,4) DEFAULT 1.0,
    irr DECIMAL(6,2),
    tier TEXT CHECK (tier IN ('Core', 'Strategic', 'Exploration')),
    relationship_strength INTEGER DEFAULT 50 CHECK (relationship_strength >= 0 AND relationship_strength <= 100),
    last_contact_date DATE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ════════════════════════════════════════════════════════
-- PORTFOLIO COMPANIES TABLE
-- ════════════════════════════════════════════════════════
CREATE TABLE public.portfolio_companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name TEXT NOT NULL,
    fund_id UUID REFERENCES public.funds(id) ON DELETE CASCADE,
    fund_name TEXT NOT NULL,
    gp_name TEXT NOT NULL,
    sector TEXT NOT NULL,
    stage TEXT NOT NULL,
    status TEXT DEFAULT 'Active' CHECK (status IN ('Active', 'Exited')),
    investment_date DATE,
    exit_date DATE,
    exit_type TEXT,
    valuation_estimate DECIMAL(15,2),
    ownership_pct DECIMAL(5,4),
    signal_score INTEGER DEFAULT 70 CHECK (signal_score >= 0 AND signal_score <= 100),
    momentum TEXT CHECK (momentum IN ('up', 'flat', 'down')),
    employees INTEGER,
    revenue_estimate DECIMAL(15,2),
    exit_timeline_months INTEGER,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ════════════════════════════════════════════════════════
-- DEAL FLOW TABLE
-- ════════════════════════════════════════════════════════
CREATE TABLE public.deal_flow (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name TEXT NOT NULL,
    sector TEXT NOT NULL,
    stage TEXT NOT NULL,
    check_size DECIMAL(10,2),
    gp_name TEXT NOT NULL,
    fund_id UUID REFERENCES public.funds(id),
    timeline_days INTEGER,
    co_invest_rights BOOLEAN DEFAULT false,
    deal_score INTEGER DEFAULT 70 CHECK (deal_score >= 0 AND deal_score <= 100),
    date_shared DATE DEFAULT CURRENT_DATE,
    status TEXT DEFAULT 'Active' CHECK (status IN ('Active', 'Passed', 'Committed')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ════════════════════════════════════════════════════════
-- CAPITAL CALLS & DISTRIBUTIONS TABLE
-- ════════════════════════════════════════════════════════
CREATE TABLE public.capital_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fund_id UUID REFERENCES public.funds(id) ON DELETE CASCADE,
    fund_name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('call', 'distribution')),
    amount DECIMAL(15,2) NOT NULL,
    date DATE NOT NULL,
    notice_date DATE,
    due_date DATE,
    description TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ════════════════════════════════════════════════════════
-- MEETING NOTES TABLE
-- ════════════════════════════════════════════════════════
CREATE TABLE public.meeting_notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fund_id UUID REFERENCES public.funds(id),
    gp_name TEXT NOT NULL,
    meeting_date DATE NOT NULL,
    attendees TEXT[],
    discussion_points TEXT,
    action_items TEXT,
    next_steps TEXT,
    relationship_quality INTEGER CHECK (relationship_quality >= 0 AND relationship_quality <= 100),
    created_by TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ════════════════════════════════════════════════════════
-- LP OVERLAP / COMPETITIVE ANALYSIS TABLE
-- ════════════════════════════════════════════════════════
CREATE TABLE public.lp_overlap (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fund_id UUID REFERENCES public.funds(id),
    fund_name TEXT NOT NULL,
    known_lps TEXT[],
    overlap_count INTEGER DEFAULT 0,
    unique_access BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ════════════════════════════════════════════════════════
-- INDEXES FOR PERFORMANCE
-- ════════════════════════════════════════════════════════
CREATE INDEX idx_funds_gp ON public.funds(gp_name);
CREATE INDEX idx_funds_vintage ON public.funds(vintage);
CREATE INDEX idx_funds_tvpi ON public.funds(tvpi DESC);
CREATE INDEX idx_funds_status ON public.funds(status);

CREATE INDEX idx_companies_fund ON public.portfolio_companies(fund_id);
CREATE INDEX idx_companies_sector ON public.portfolio_companies(sector);
CREATE INDEX idx_companies_status ON public.portfolio_companies(status);
CREATE INDEX idx_companies_signal ON public.portfolio_companies(signal_score DESC);

CREATE INDEX idx_dealflow_gp ON public.deal_flow(gp_name);
CREATE INDEX idx_dealflow_status ON public.deal_flow(status);
CREATE INDEX idx_dealflow_score ON public.deal_flow(deal_score DESC);

CREATE INDEX idx_capital_fund ON public.capital_activity(fund_id);
CREATE INDEX idx_capital_date ON public.capital_activity(date DESC);
CREATE INDEX idx_capital_type ON public.capital_activity(type);

-- ════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY (RLS)
-- ════════════════════════════════════════════════════════

-- Enable RLS on all tables
ALTER TABLE public.funds ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.portfolio_companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.deal_flow ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.capital_activity ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.meeting_notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lp_overlap ENABLE ROW LEVEL SECURITY;

-- Create policies (Allow all for authenticated users - refine later)
CREATE POLICY "Allow all for authenticated users" ON public.funds
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON public.portfolio_companies
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON public.deal_flow
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON public.capital_activity
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON public.meeting_notes
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON public.lp_overlap
    FOR ALL USING (auth.role() = 'authenticated');

-- ════════════════════════════════════════════════════════
-- FUNCTIONS FOR AUTO-UPDATING TIMESTAMPS
-- ════════════════════════════════════════════════════════
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for all tables
CREATE TRIGGER update_funds_updated_at BEFORE UPDATE ON public.funds
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON public.portfolio_companies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dealflow_updated_at BEFORE UPDATE ON public.deal_flow
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_capital_updated_at BEFORE UPDATE ON public.capital_activity
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_meetings_updated_at BEFORE UPDATE ON public.meeting_notes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_lp_overlap_updated_at BEFORE UPDATE ON public.lp_overlap
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ════════════════════════════════════════════════════════
-- HELPFUL VIEWS
-- ════════════════════════════════════════════════════════

-- Top performing funds view
CREATE VIEW top_performing_funds AS
SELECT
    fund_name,
    gp_name,
    vintage,
    tvpi,
    dpi,
    irr,
    current_nav,
    tier
FROM public.funds
WHERE status = 'Active'
ORDER BY tvpi DESC
LIMIT 20;

-- Portfolio summary view
CREATE VIEW portfolio_summary AS
SELECT
    COUNT(*) as total_funds,
    SUM(commitment_amount) as total_commitments,
    SUM(total_called) as total_called,
    SUM(total_distributed) as total_distributed,
    SUM(current_nav) as total_nav,
    AVG(tvpi) as avg_tvpi,
    AVG(dpi) as avg_dpi,
    AVG(irr) as avg_irr
FROM public.funds
WHERE status = 'Active';

-- Companies by sector view
CREATE VIEW companies_by_sector AS
SELECT
    sector,
    COUNT(*) as company_count,
    COUNT(CASE WHEN status = 'Active' THEN 1 END) as active_count,
    COUNT(CASE WHEN status = 'Exited' THEN 1 END) as exited_count,
    AVG(signal_score) as avg_signal_score
FROM public.portfolio_companies
GROUP BY sector
ORDER BY company_count DESC;

-- ════════════════════════════════════════════════════════
-- SUCCESS MESSAGE
-- ════════════════════════════════════════════════════════
SELECT 'NEWCO V10 Database Schema Created Successfully!' as message;

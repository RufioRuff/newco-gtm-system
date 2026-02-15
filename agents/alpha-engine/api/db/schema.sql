-- ╔══════════════════════════════════════════════════════════════════════════╗
-- ║  NEWCO V10 — SUPABASE DATABASE SCHEMA                                  ║
-- ║  AI Safety & Trust VC Fund-of-Funds Intelligence Platform              ║
-- ║  PostgreSQL 15+ / Supabase / Row Level Security                        ║
-- ╚══════════════════════════════════════════════════════════════════════════╝

-- ═══════════════════════════════════════════════════════════════
-- EXTENSIONS
-- ═══════════════════════════════════════════════════════════════
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";        -- fuzzy text search
CREATE EXTENSION IF NOT EXISTS "btree_gist";     -- exclusion constraints

-- ═══════════════════════════════════════════════════════════════
-- ENUMS
-- ═══════════════════════════════════════════════════════════════
CREATE TYPE fund_strategy AS ENUM (
  'venture', 'growth', 'buyout', 'secondaries', 'co_invest',
  'real_assets', 'credit', 'fund_of_funds', 'direct', 'spv'
);

CREATE TYPE fund_status AS ENUM (
  'prospecting', 'diligence', 'ic_review', 'committed',
  'invested', 'harvesting', 'fully_realized', 'declined', 'watchlist'
);

CREATE TYPE deal_signal AS ENUM (
  'strong_buy', 'buy', 'hold', 'reduce', 'sell', 'pass'
);

CREATE TYPE deal_type AS ENUM (
  'fund_commitment', 'co_invest', 'secondary', 'direct', 'spv'
);

CREATE TYPE contact_tier AS ENUM ('tier1', 'tier2', 'tier3', 'tier4');

CREATE TYPE lp_status AS ENUM (
  'prospect', 'qualifying', 'due_diligence', 'commitment',
  'invested', 're_upping', 'declined', 'churned'
);

CREATE TYPE ic_vote AS ENUM ('approve', 'reject', 'abstain', 'conditional');

CREATE TYPE agent_type AS ENUM (
  'sentinel', 'persona_panel', 'living_thesis', 'dashboard',
  'pattern_hunter', 'scenario_engine', 'network_mapper', 'capital_optimizer'
);

CREATE TYPE task_status AS ENUM ('pending', 'running', 'completed', 'failed', 'cancelled');

CREATE TYPE severity_level AS ENUM ('info', 'low', 'medium', 'high', 'critical');

-- ═══════════════════════════════════════════════════════════════
-- CORE: TEAM & ORGANIZATION
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE team_members (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  auth_user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  role TEXT NOT NULL,         -- 'Managing Partner', 'Operating Partner', etc.
  title TEXT,
  phone TEXT,
  avatar_url TEXT,
  bio TEXT,
  linkedin_url TEXT,
  expertise JSONB DEFAULT '[]',
  permissions JSONB DEFAULT '{"admin": false, "ic_vote": true, "deal_create": true}',
  is_active BOOLEAN DEFAULT true,
  joined_at TIMESTAMPTZ DEFAULT now(),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- PORTFOLIO: FUNDS
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE gp_firms (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE,
  hq_city TEXT,
  hq_country TEXT DEFAULT 'US',
  founded_year INT,
  aum_millions NUMERIC(12,2),
  strategy fund_strategy,
  sector_focus JSONB DEFAULT '[]',      -- ['AI Safety', 'Trust & Safety', 'GovTech']
  team_size INT,
  website TEXT,
  pitchbook_id TEXT,
  crunchbase_id TEXT,
  logo_url TEXT,
  notes TEXT,
  health_score NUMERIC(5,2),            -- 0-100 GP health composite
  health_factors JSONB,                 -- {team_stability, aum_growth, style_drift, compliance}
  tags JSONB DEFAULT '[]',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE funds (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  gp_firm_id UUID REFERENCES gp_firms(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  vintage_year INT NOT NULL,
  strategy fund_strategy NOT NULL,
  status fund_status DEFAULT 'prospecting',
  fund_size_millions NUMERIC(12,2),
  committed_millions NUMERIC(12,2) DEFAULT 0,
  called_millions NUMERIC(12,2) DEFAULT 0,
  distributed_millions NUMERIC(12,2) DEFAULT 0,
  nav_millions NUMERIC(12,2) DEFAULT 0,
  unfunded_millions NUMERIC(12,2) GENERATED ALWAYS AS (committed_millions - called_millions) STORED,
  tvpi NUMERIC(6,3),
  dpi NUMERIC(6,3),
  irr NUMERIC(6,2),
  pme NUMERIC(6,3),                    -- public market equivalent
  quartile INT CHECK (quartile BETWEEN 1 AND 4),
  benchmark_irr NUMERIC(6,2),
  mgmt_fee_rate NUMERIC(5,4),         -- e.g., 0.0200 = 2.00%
  carry_rate NUMERIC(5,4),
  preferred_return NUMERIC(5,4),
  hurdle_rate NUMERIC(5,4),
  waterfall_type TEXT DEFAULT 'european', -- 'european' or 'american'
  commitment_date DATE,
  final_close_date DATE,
  investment_period_end DATE,
  fund_term_years INT DEFAULT 10,
  extension_years INT DEFAULT 2,
  sector_allocation JSONB,             -- {ai_safety: 0.35, trust_safety: 0.25, ...}
  geo_allocation JSONB,
  co_invest_rights BOOLEAN DEFAULT false,
  advisory_board_seat BOOLEAN DEFAULT false,
  key_person_clause JSONB,
  side_letter_terms JSONB,
  documents JSONB DEFAULT '[]',        -- [{name, url, type, uploaded_at}]
  tags JSONB DEFAULT '[]',
  notes TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- PORTFOLIO: LOOK-THROUGH COMPANIES
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE portfolio_companies (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE,
  sector TEXT,
  subsector TEXT,
  hq_city TEXT,
  hq_country TEXT DEFAULT 'US',
  founded_year INT,
  stage TEXT,                          -- 'Seed', 'Series A', etc.
  last_valuation_millions NUMERIC(14,2),
  last_round_date DATE,
  revenue_millions NUMERIC(12,2),
  revenue_growth_pct NUMERIC(6,2),
  employees INT,
  website TEXT,
  crunchbase_url TEXT,
  pitchbook_id TEXT,
  logo_url TEXT,
  description TEXT,
  thesis TEXT,                         -- why we like this company
  moat_score NUMERIC(5,2),            -- 0-100
  moat_factors JSONB,
  public_ticker TEXT,                  -- if IPO'd
  exit_date DATE,
  exit_type TEXT,                      -- 'IPO', 'M&A', 'Secondary', null
  exit_valuation_millions NUMERIC(14,2),
  tags JSONB DEFAULT '[]',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE fund_company_positions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  fund_id UUID REFERENCES funds(id) ON DELETE CASCADE,
  company_id UUID REFERENCES portfolio_companies(id) ON DELETE CASCADE,
  ownership_pct NUMERIC(8,5),
  cost_basis_millions NUMERIC(12,2),
  current_value_millions NUMERIC(12,2),
  moic NUMERIC(6,3),
  entry_date DATE,
  entry_valuation_millions NUMERIC(14,2),
  is_lead BOOLEAN DEFAULT false,
  board_seat BOOLEAN DEFAULT false,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(fund_id, company_id)
);

-- ═══════════════════════════════════════════════════════════════
-- DEAL PIPELINE
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE deals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  deal_type deal_type NOT NULL,
  signal deal_signal DEFAULT 'hold',
  fund_id UUID REFERENCES funds(id) ON DELETE SET NULL,
  gp_firm_id UUID REFERENCES gp_firms(id) ON DELETE SET NULL,
  company_id UUID REFERENCES portfolio_companies(id) ON DELETE SET NULL,
  status fund_status DEFAULT 'prospecting',
  owner_id UUID REFERENCES team_members(id) ON DELETE SET NULL,
  
  -- Sizing
  target_commitment_millions NUMERIC(12,2),
  min_commitment_millions NUMERIC(12,2),
  max_commitment_millions NUMERIC(12,2),
  kelly_optimal_millions NUMERIC(12,2),
  
  -- Scoring
  conviction_score NUMERIC(5,2),       -- 0-100 composite
  bayesian_score NUMERIC(5,2),
  market_score NUMERIC(5,2),
  timing_score NUMERIC(5,2),
  fit_score NUMERIC(5,2),
  
  -- Pricing (for secondaries)
  ask_price_pct NUMERIC(6,2),          -- % of NAV
  bid_price_pct NUMERIC(6,2),
  nav_millions NUMERIC(12,2),
  discount_pct NUMERIC(6,2),
  fair_value_pct NUMERIC(6,2),
  
  -- Returns
  irr_base NUMERIC(6,2),
  irr_bull NUMERIC(6,2),
  irr_bear NUMERIC(6,2),
  tvpi_target NUMERIC(6,3),
  
  -- Timeline
  urgency TEXT,                        -- '48hr', '2 weeks', etc.
  deadline DATE,
  expected_close_date DATE,
  
  -- Content
  thesis TEXT,
  catalysts JSONB DEFAULT '[]',
  risks JSONB DEFAULT '[]',
  comps JSONB DEFAULT '[]',
  
  -- IC
  ic_date DATE,
  ic_status TEXT,
  ic_notes TEXT,
  
  source TEXT,                         -- how we found this deal
  source_contact_id UUID,
  documents JSONB DEFAULT '[]',
  tags JSONB DEFAULT '[]',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE ic_votes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  deal_id UUID REFERENCES deals(id) ON DELETE CASCADE,
  voter_id UUID REFERENCES team_members(id) ON DELETE CASCADE,
  vote ic_vote NOT NULL,
  conviction_score INT CHECK (conviction_score BETWEEN 1 AND 10),
  rationale TEXT,
  conditions TEXT,                     -- for conditional approvals
  voted_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(deal_id, voter_id)
);

CREATE TABLE deal_activity (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  deal_id UUID REFERENCES deals(id) ON DELETE CASCADE,
  actor_id UUID REFERENCES team_members(id) ON DELETE SET NULL,
  action TEXT NOT NULL,                -- 'status_change', 'note_added', 'document_uploaded', etc.
  old_value TEXT,
  new_value TEXT,
  note TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- SECONDARIES MARKET
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE secondary_transactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  deal_id UUID REFERENCES deals(id) ON DELETE SET NULL,
  fund_id UUID REFERENCES funds(id) ON DELETE SET NULL,
  seller_type TEXT,                    -- 'Distressed LP', 'Portfolio Rebalance', etc.
  seller_name TEXT,
  buyer_name TEXT,                     -- could be us or market data
  nav_at_transaction NUMERIC(12,2),
  price_pct_of_nav NUMERIC(6,2),
  transaction_size_millions NUMERIC(12,2),
  remaining_unfunded_millions NUMERIC(12,2),
  transaction_date DATE,
  close_date DATE,
  broker TEXT,
  pricing_model JSONB,                -- Ken Wallace framework inputs
  algo_score NUMERIC(5,2),            -- algorithmic secondary score
  notes TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- LP MANAGEMENT
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE lps (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  lp_type TEXT,                        -- 'Family Office', 'RIA', 'Endowment', 'Pension', etc.
  status lp_status DEFAULT 'prospect',
  committed_millions NUMERIC(12,2) DEFAULT 0,
  called_millions NUMERIC(12,2) DEFAULT 0,
  distributions_millions NUMERIC(12,2) DEFAULT 0,
  contact_name TEXT,
  contact_email TEXT,
  contact_phone TEXT,
  firm_name TEXT,
  firm_aum_millions NUMERIC(14,2),
  channel TEXT,                        -- 'Direct', 'Platform', 'Placement Agent'
  platform_name TEXT,                  -- 'Hightower', 'Goldman', 'Mercer', etc.
  advisor_name TEXT,
  advisor_id UUID REFERENCES team_members(id),
  suitability_score NUMERIC(5,2),
  risk_tolerance TEXT,                 -- 'Conservative', 'Moderate', 'Aggressive'
  investment_horizon_years INT,
  accredited BOOLEAN DEFAULT true,
  qp_status BOOLEAN DEFAULT true,     -- qualified purchaser
  minimum_commitment_millions NUMERIC(12,2),
  side_letter_terms JSONB,
  ddq_completed BOOLEAN DEFAULT false,
  ddq_date DATE,
  kyc_aml_completed BOOLEAN DEFAULT false,
  documents JSONB DEFAULT '[]',
  notes TEXT,
  tags JSONB DEFAULT '[]',
  metadata JSONB DEFAULT '{}',
  source TEXT,
  source_detail TEXT,
  first_contact_date DATE,
  commitment_date DATE,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lp_interactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  lp_id UUID REFERENCES lps(id) ON DELETE CASCADE,
  team_member_id UUID REFERENCES team_members(id) ON DELETE SET NULL,
  interaction_type TEXT,               -- 'call', 'email', 'meeting', 'event', 'report'
  subject TEXT,
  notes TEXT,
  sentiment TEXT,                      -- 'positive', 'neutral', 'negative'
  follow_up_date DATE,
  follow_up_action TEXT,
  occurred_at TIMESTAMPTZ DEFAULT now(),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lp_reports (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  lp_id UUID REFERENCES lps(id) ON DELETE SET NULL, -- null = all LPs
  report_type TEXT,                    -- 'quarterly', 'annual', 'capital_call', 'distribution', 'ad_hoc'
  period TEXT,                         -- 'Q1 2026', '2025', etc.
  title TEXT NOT NULL,
  content JSONB,                       -- structured report data
  document_url TEXT,
  sent_at TIMESTAMPTZ,
  opened_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- NETWORK & CONTACTS
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE contacts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  email TEXT,
  phone TEXT,
  title TEXT,
  organization TEXT,
  organization_type TEXT,              -- 'GP', 'LP', 'Advisor', 'Portfolio Co', etc.
  tier contact_tier DEFAULT 'tier3',
  relationship_owner_id UUID REFERENCES team_members(id),
  linkedin_url TEXT,
  location TEXT,
  bio TEXT,
  tags JSONB DEFAULT '[]',
  
  -- Network scoring
  network_score NUMERIC(5,2),          -- 0-100
  centrality_score NUMERIC(5,2),
  influence_score NUMERIC(5,2),
  activation_potential NUMERIC(5,2),
  last_contact_date DATE,
  contact_frequency_days INT,          -- avg days between contacts
  relationship_strength TEXT,          -- 'Strong', 'Warm', 'Cold', 'Decaying'
  
  -- Source tracking
  source TEXT,                         -- 'Berkeley', 'Conference', 'Referral', etc.
  referred_by_id UUID REFERENCES contacts(id),
  
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE contact_interactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
  team_member_id UUID REFERENCES team_members(id) ON DELETE SET NULL,
  interaction_type TEXT,
  channel TEXT,                        -- 'email', 'phone', 'in_person', 'linkedin', 'event'
  subject TEXT,
  notes TEXT,
  sentiment TEXT,
  deal_id UUID REFERENCES deals(id),
  occurred_at TIMESTAMPTZ DEFAULT now(),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE contact_relationships (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  contact_a_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
  contact_b_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
  relationship_type TEXT,              -- 'colleague', 'advisor', 'investor', 'board', 'co_investor'
  strength NUMERIC(5,2),
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(contact_a_id, contact_b_id)
);

-- ═══════════════════════════════════════════════════════════════
-- CASH FLOWS & PACING
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE cash_flows (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  fund_id UUID REFERENCES funds(id) ON DELETE CASCADE,
  lp_id UUID REFERENCES lps(id) ON DELETE SET NULL,
  flow_type TEXT NOT NULL,             -- 'capital_call', 'distribution', 'mgmt_fee', 'carry'
  amount_millions NUMERIC(12,4),
  flow_date DATE NOT NULL,
  notice_date DATE,
  due_date DATE,
  description TEXT,
  is_projected BOOLEAN DEFAULT false,  -- actual vs projected
  document_url TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE pacing_models (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  description TEXT,
  target_allocation JSONB,             -- {venture: 0.40, growth: 0.25, ...}
  target_vintage_spread JSONB,         -- {2024: 0.15, 2025: 0.20, ...}
  commitment_pace_millions NUMERIC(12,2),
  total_target_aum_millions NUMERIC(12,2),
  assumptions JSONB,                   -- {call_rate, distribution_rate, growth_rate}
  projections JSONB,                   -- yearly projections array
  is_active BOOLEAN DEFAULT true,
  created_by_id UUID REFERENCES team_members(id),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- GP EVALUATION & REFERENCE CALLS
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE gp_evaluations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  gp_firm_id UUID REFERENCES gp_firms(id) ON DELETE CASCADE,
  fund_id UUID REFERENCES funds(id) ON DELETE SET NULL,
  evaluator_id UUID REFERENCES team_members(id),
  evaluation_date DATE DEFAULT CURRENT_DATE,
  
  -- Scorecard (50+ factors collapsed into categories)
  returns_score NUMERIC(5,2),          -- track record quality
  team_score NUMERIC(5,2),            -- team stability, depth, succession
  process_score NUMERIC(5,2),         -- investment process rigor
  terms_score NUMERIC(5,2),           -- LP friendliness
  strategy_score NUMERIC(5,2),        -- differentiation, edge
  operations_score NUMERIC(5,2),      -- back office, reporting
  esg_score NUMERIC(5,2),            -- ESG integration
  composite_score NUMERIC(5,2),
  
  -- Detailed factor scores
  factor_scores JSONB,                 -- {factor_name: {score, weight, notes}}
  
  strengths TEXT,
  weaknesses TEXT,
  recommendation TEXT,                 -- 'Commit', 'Pass', 'Monitor', 'Re-evaluate'
  re_up_recommendation BOOLEAN,
  
  notes TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE reference_calls (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  gp_firm_id UUID REFERENCES gp_firms(id) ON DELETE CASCADE,
  fund_id UUID REFERENCES funds(id) ON DELETE SET NULL,
  caller_id UUID REFERENCES team_members(id),
  reference_name TEXT NOT NULL,
  reference_title TEXT,
  reference_org TEXT,
  reference_type TEXT,                 -- 'LP', 'Portfolio CEO', 'Co-investor', 'Former Employee'
  call_date DATE,
  duration_minutes INT,
  
  -- Structured feedback
  overall_rating INT CHECK (overall_rating BETWEEN 1 AND 10),
  would_reinvest BOOLEAN,
  strengths JSONB DEFAULT '[]',
  concerns JSONB DEFAULT '[]',
  
  transcript TEXT,
  summary TEXT,
  sentiment TEXT,
  red_flags JSONB DEFAULT '[]',
  
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- SIGNALS & INTELLIGENCE
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE signals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  signal_type TEXT NOT NULL,           -- 'market', 'portfolio', 'team', 'regulatory', 'competitive'
  severity severity_level DEFAULT 'info',
  title TEXT NOT NULL,
  description TEXT,
  source TEXT,                         -- 'pitchbook', 'news', 'sec_filing', 'manual', 'agent'
  source_url TEXT,
  
  -- Related entities
  fund_id UUID REFERENCES funds(id) ON DELETE SET NULL,
  gp_firm_id UUID REFERENCES gp_firms(id) ON DELETE SET NULL,
  company_id UUID REFERENCES portfolio_companies(id) ON DELETE SET NULL,
  deal_id UUID REFERENCES deals(id) ON DELETE SET NULL,
  contact_id UUID REFERENCES contacts(id) ON DELETE SET NULL,
  
  -- AI analysis
  ai_summary TEXT,
  ai_impact_score NUMERIC(5,2),
  ai_action_required BOOLEAN DEFAULT false,
  ai_suggested_actions JSONB DEFAULT '[]',
  
  -- Status
  is_read BOOLEAN DEFAULT false,
  is_actioned BOOLEAN DEFAULT false,
  actioned_by_id UUID REFERENCES team_members(id),
  actioned_at TIMESTAMPTZ,
  action_taken TEXT,
  
  expires_at TIMESTAMPTZ,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- OMNISCIENT AI AGENTS
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE agent_configs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  agent_type agent_type NOT NULL UNIQUE,
  name TEXT NOT NULL,
  description TEXT,
  is_active BOOLEAN DEFAULT true,
  config JSONB DEFAULT '{}',           -- agent-specific configuration
  model TEXT DEFAULT 'claude-sonnet-4-5-20250929',
  max_tokens INT DEFAULT 4096,
  temperature NUMERIC(3,2) DEFAULT 0.7,
  system_prompt TEXT,
  tools JSONB DEFAULT '[]',            -- available tools/functions
  schedule TEXT,                       -- cron expression for scheduled runs
  last_run_at TIMESTAMPTZ,
  run_count INT DEFAULT 0,
  avg_latency_ms INT,
  error_rate NUMERIC(5,4),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE agent_runs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  agent_id UUID REFERENCES agent_configs(id) ON DELETE CASCADE,
  status task_status DEFAULT 'pending',
  trigger TEXT,                        -- 'scheduled', 'manual', 'event', 'chain'
  input JSONB,
  output JSONB,
  tokens_used INT,
  latency_ms INT,
  error TEXT,
  parent_run_id UUID REFERENCES agent_runs(id), -- for chained runs
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE agent_insights (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  agent_id UUID REFERENCES agent_configs(id) ON DELETE CASCADE,
  run_id UUID REFERENCES agent_runs(id) ON DELETE SET NULL,
  insight_type TEXT,                   -- 'recommendation', 'alert', 'analysis', 'prediction'
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  confidence NUMERIC(5,2),
  impact_score NUMERIC(5,2),
  
  -- Related entities
  fund_id UUID REFERENCES funds(id) ON DELETE SET NULL,
  deal_id UUID REFERENCES deals(id) ON DELETE SET NULL,
  company_id UUID REFERENCES portfolio_companies(id) ON DELETE SET NULL,
  
  is_dismissed BOOLEAN DEFAULT false,
  is_actioned BOOLEAN DEFAULT false,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- DATA INGESTION
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE data_sources (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  source_type TEXT,                    -- 'api', 'file', 'email', 'manual', 'scrape'
  provider TEXT,                       -- 'pitchbook', 'preqin', 'sec', 'bloomberg'
  connection_config JSONB,             -- encrypted connection details
  sync_schedule TEXT,                  -- cron expression
  last_sync_at TIMESTAMPTZ,
  last_sync_status task_status,
  last_sync_records INT,
  is_active BOOLEAN DEFAULT true,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE ingestion_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_id UUID REFERENCES data_sources(id) ON DELETE CASCADE,
  status task_status DEFAULT 'pending',
  records_processed INT DEFAULT 0,
  records_created INT DEFAULT 0,
  records_updated INT DEFAULT 0,
  records_failed INT DEFAULT 0,
  errors JSONB DEFAULT '[]',
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- DOCUMENTS & FILES
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  file_type TEXT,                      -- 'pdf', 'docx', 'xlsx', 'pptx', etc.
  category TEXT,                       -- 'lpa', 'ddq', 'side_letter', 'ic_memo', 'quarterly_report'
  storage_path TEXT,                   -- Supabase Storage path
  file_size_bytes BIGINT,
  
  -- Related entities
  fund_id UUID REFERENCES funds(id) ON DELETE SET NULL,
  deal_id UUID REFERENCES deals(id) ON DELETE SET NULL,
  lp_id UUID REFERENCES lps(id) ON DELETE SET NULL,
  gp_firm_id UUID REFERENCES gp_firms(id) ON DELETE SET NULL,
  
  -- AI processing
  ai_summary TEXT,
  ai_extracted_data JSONB,
  ai_processed_at TIMESTAMPTZ,
  
  uploaded_by_id UUID REFERENCES team_members(id),
  version INT DEFAULT 1,
  is_current BOOLEAN DEFAULT true,
  tags JSONB DEFAULT '[]',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- BENCHMARKS & MARKET DATA
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE benchmarks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,                  -- 'Cambridge Associates US VC', 'Preqin Buyout', etc.
  provider TEXT,
  strategy fund_strategy,
  vintage_year INT,
  as_of_date DATE,
  irr_q1 NUMERIC(6,2),
  irr_median NUMERIC(6,2),
  irr_q3 NUMERIC(6,2),
  tvpi_q1 NUMERIC(6,3),
  tvpi_median NUMERIC(6,3),
  tvpi_q3 NUMERIC(6,3),
  dpi_q1 NUMERIC(6,3),
  dpi_median NUMERIC(6,3),
  dpi_q3 NUMERIC(6,3),
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE market_data_snapshots (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  snapshot_date DATE NOT NULL,
  data_type TEXT,                      -- 'secondary_pricing', 'fundraising', 'exits', 'valuations'
  data JSONB NOT NULL,
  source TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- NAV & PERFORMANCE HISTORY
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE nav_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  fund_id UUID REFERENCES funds(id) ON DELETE CASCADE,
  report_date DATE NOT NULL,
  nav_millions NUMERIC(12,4),
  tvpi NUMERIC(6,3),
  dpi NUMERIC(6,3),
  irr NUMERIC(6,2),
  called_pct NUMERIC(5,2),
  distributed_pct NUMERIC(5,2),
  unrealized_pct NUMERIC(5,2),
  portfolio_company_count INT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(fund_id, report_date)
);

CREATE TABLE portfolio_nav_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  report_date DATE NOT NULL,
  total_nav_millions NUMERIC(14,4),
  total_committed_millions NUMERIC(14,4),
  total_called_millions NUMERIC(14,4),
  total_distributed_millions NUMERIC(14,4),
  weighted_irr NUMERIC(6,2),
  weighted_tvpi NUMERIC(6,3),
  weighted_dpi NUMERIC(6,3),
  fund_count INT,
  company_count INT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(report_date)
);

-- ═══════════════════════════════════════════════════════════════
-- EVENTS & CONFERENCES
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  event_type TEXT,                     -- 'conference', 'dinner', 'webinar', 'roadshow', 'lp_meeting'
  location TEXT,
  start_date DATE,
  end_date DATE,
  cost_dollars NUMERIC(10,2),
  attendees JSONB DEFAULT '[]',        -- team member IDs
  objectives TEXT,
  
  -- ROI tracking
  new_contacts INT DEFAULT 0,
  deals_sourced INT DEFAULT 0,
  lp_intros INT DEFAULT 0,
  capital_linked_millions NUMERIC(12,2) DEFAULT 0,
  roi_multiple NUMERIC(8,2),
  
  notes TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- PLATFORM & DISTRIBUTION
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE platform_applications (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  platform_name TEXT NOT NULL,         -- 'Hightower', 'Goldman', 'Mercer-Regis', etc.
  application_date DATE,
  status TEXT DEFAULT 'pending',       -- 'pending', 'in_review', 'approved', 'declined', 'onboarded'
  primary_contact TEXT,
  primary_email TEXT,
  requirements JSONB DEFAULT '[]',     -- checklist items
  completed_requirements JSONB DEFAULT '[]',
  expected_aum_millions NUMERIC(12,2),
  advisor_count INT,
  avg_ticket_millions NUMERIC(12,2),
  fee_arrangement JSONB,
  notes TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE advisor_battlecards (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  objection TEXT NOT NULL,
  category TEXT,                       -- 'fees', 'performance', 'liquidity', 'risk', 'alternatives'
  response TEXT NOT NULL,
  supporting_data JSONB,
  effectiveness_score NUMERIC(5,2),
  use_count INT DEFAULT 0,
  created_by_id UUID REFERENCES team_members(id),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- AUDIT LOG
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES team_members(id) ON DELETE SET NULL,
  action TEXT NOT NULL,
  table_name TEXT,
  record_id UUID,
  old_data JSONB,
  new_data JSONB,
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════
-- INDEXES
-- ═══════════════════════════════════════════════════════════════

-- Funds
CREATE INDEX idx_funds_gp ON funds(gp_firm_id);
CREATE INDEX idx_funds_strategy ON funds(strategy);
CREATE INDEX idx_funds_status ON funds(status);
CREATE INDEX idx_funds_vintage ON funds(vintage_year);

-- Deals
CREATE INDEX idx_deals_status ON deals(status);
CREATE INDEX idx_deals_type ON deals(deal_type);
CREATE INDEX idx_deals_signal ON deals(signal);
CREATE INDEX idx_deals_owner ON deals(owner_id);
CREATE INDEX idx_deals_fund ON deals(fund_id);
CREATE INDEX idx_deals_conviction ON deals(conviction_score DESC);
CREATE INDEX idx_deals_created ON deals(created_at DESC);

-- Portfolio Companies
CREATE INDEX idx_companies_sector ON portfolio_companies(sector);
CREATE INDEX idx_companies_stage ON portfolio_companies(stage);
CREATE INDEX idx_companies_name_trgm ON portfolio_companies USING gin(name gin_trgm_ops);

-- Contacts
CREATE INDEX idx_contacts_tier ON contacts(tier);
CREATE INDEX idx_contacts_owner ON contacts(relationship_owner_id);
CREATE INDEX idx_contacts_score ON contacts(network_score DESC);
CREATE INDEX idx_contacts_name_trgm ON contacts USING gin(name gin_trgm_ops);
CREATE INDEX idx_contacts_org_trgm ON contacts USING gin(organization gin_trgm_ops);

-- LPs
CREATE INDEX idx_lps_status ON lps(status);
CREATE INDEX idx_lps_type ON lps(lp_type);
CREATE INDEX idx_lps_channel ON lps(channel);

-- Signals
CREATE INDEX idx_signals_severity ON signals(severity);
CREATE INDEX idx_signals_type ON signals(signal_type);
CREATE INDEX idx_signals_created ON signals(created_at DESC);
CREATE INDEX idx_signals_unread ON signals(is_read) WHERE NOT is_read;

-- Cash Flows
CREATE INDEX idx_cashflows_fund ON cash_flows(fund_id);
CREATE INDEX idx_cashflows_date ON cash_flows(flow_date);
CREATE INDEX idx_cashflows_type ON cash_flows(flow_type);

-- NAV History
CREATE INDEX idx_nav_fund_date ON nav_history(fund_id, report_date DESC);
CREATE INDEX idx_portfolio_nav_date ON portfolio_nav_history(report_date DESC);

-- Agent Runs
CREATE INDEX idx_agent_runs_agent ON agent_runs(agent_id);
CREATE INDEX idx_agent_runs_status ON agent_runs(status);
CREATE INDEX idx_agent_runs_created ON agent_runs(created_at DESC);

-- Audit
CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_table ON audit_log(table_name);
CREATE INDEX idx_audit_created ON audit_log(created_at DESC);

-- ═══════════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY
-- ═══════════════════════════════════════════════════════════════

ALTER TABLE team_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE gp_firms ENABLE ROW LEVEL SECURITY;
ALTER TABLE funds ENABLE ROW LEVEL SECURITY;
ALTER TABLE portfolio_companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE fund_company_positions ENABLE ROW LEVEL SECURITY;
ALTER TABLE deals ENABLE ROW LEVEL SECURITY;
ALTER TABLE ic_votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE deal_activity ENABLE ROW LEVEL SECURITY;
ALTER TABLE secondary_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE lps ENABLE ROW LEVEL SECURITY;
ALTER TABLE lp_interactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE lp_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE contact_interactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE contact_relationships ENABLE ROW LEVEL SECURITY;
ALTER TABLE cash_flows ENABLE ROW LEVEL SECURITY;
ALTER TABLE pacing_models ENABLE ROW LEVEL SECURITY;
ALTER TABLE gp_evaluations ENABLE ROW LEVEL SECURITY;
ALTER TABLE reference_calls ENABLE ROW LEVEL SECURITY;
ALTER TABLE signals ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE data_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE ingestion_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE benchmarks ENABLE ROW LEVEL SECURITY;
ALTER TABLE market_data_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE nav_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE portfolio_nav_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE advisor_battlecards ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

-- Authenticated team members can read everything
CREATE POLICY "team_read_all" ON team_members FOR SELECT TO authenticated USING (true);
CREATE POLICY "gp_read" ON gp_firms FOR SELECT TO authenticated USING (true);
CREATE POLICY "funds_read" ON funds FOR SELECT TO authenticated USING (true);
CREATE POLICY "companies_read" ON portfolio_companies FOR SELECT TO authenticated USING (true);
CREATE POLICY "positions_read" ON fund_company_positions FOR SELECT TO authenticated USING (true);
CREATE POLICY "deals_read" ON deals FOR SELECT TO authenticated USING (true);
CREATE POLICY "votes_read" ON ic_votes FOR SELECT TO authenticated USING (true);
CREATE POLICY "activity_read" ON deal_activity FOR SELECT TO authenticated USING (true);
CREATE POLICY "secondaries_read" ON secondary_transactions FOR SELECT TO authenticated USING (true);
CREATE POLICY "lps_read" ON lps FOR SELECT TO authenticated USING (true);
CREATE POLICY "lp_interactions_read" ON lp_interactions FOR SELECT TO authenticated USING (true);
CREATE POLICY "lp_reports_read" ON lp_reports FOR SELECT TO authenticated USING (true);
CREATE POLICY "contacts_read" ON contacts FOR SELECT TO authenticated USING (true);
CREATE POLICY "contact_interactions_read" ON contact_interactions FOR SELECT TO authenticated USING (true);
CREATE POLICY "contact_relationships_read" ON contact_relationships FOR SELECT TO authenticated USING (true);
CREATE POLICY "cashflows_read" ON cash_flows FOR SELECT TO authenticated USING (true);
CREATE POLICY "pacing_read" ON pacing_models FOR SELECT TO authenticated USING (true);
CREATE POLICY "gp_evals_read" ON gp_evaluations FOR SELECT TO authenticated USING (true);
CREATE POLICY "ref_calls_read" ON reference_calls FOR SELECT TO authenticated USING (true);
CREATE POLICY "signals_read" ON signals FOR SELECT TO authenticated USING (true);
CREATE POLICY "agents_read" ON agent_configs FOR SELECT TO authenticated USING (true);
CREATE POLICY "agent_runs_read" ON agent_runs FOR SELECT TO authenticated USING (true);
CREATE POLICY "agent_insights_read" ON agent_insights FOR SELECT TO authenticated USING (true);
CREATE POLICY "data_sources_read" ON data_sources FOR SELECT TO authenticated USING (true);
CREATE POLICY "ingestion_read" ON ingestion_logs FOR SELECT TO authenticated USING (true);
CREATE POLICY "docs_read" ON documents FOR SELECT TO authenticated USING (true);
CREATE POLICY "benchmarks_read" ON benchmarks FOR SELECT TO authenticated USING (true);
CREATE POLICY "market_data_read" ON market_data_snapshots FOR SELECT TO authenticated USING (true);
CREATE POLICY "nav_history_read" ON nav_history FOR SELECT TO authenticated USING (true);
CREATE POLICY "portfolio_nav_read" ON portfolio_nav_history FOR SELECT TO authenticated USING (true);
CREATE POLICY "events_read" ON events FOR SELECT TO authenticated USING (true);
CREATE POLICY "platform_apps_read" ON platform_applications FOR SELECT TO authenticated USING (true);
CREATE POLICY "battlecards_read" ON advisor_battlecards FOR SELECT TO authenticated USING (true);
CREATE POLICY "audit_read" ON audit_log FOR SELECT TO authenticated USING (true);

-- Admin write policies (team members with admin flag)
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM team_members 
    WHERE auth_user_id = auth.uid() 
    AND (permissions->>'admin')::boolean = true
  );
$$ LANGUAGE sql SECURITY DEFINER;

-- Write policies for key tables
CREATE POLICY "deals_insert" ON deals FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "deals_update" ON deals FOR UPDATE TO authenticated USING (true);
CREATE POLICY "votes_insert" ON ic_votes FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "activity_insert" ON deal_activity FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "lps_insert" ON lps FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "lps_update" ON lps FOR UPDATE TO authenticated USING (true);
CREATE POLICY "contacts_insert" ON contacts FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "contacts_update" ON contacts FOR UPDATE TO authenticated USING (true);
CREATE POLICY "signals_insert" ON signals FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "signals_update" ON signals FOR UPDATE TO authenticated USING (true);

-- ═══════════════════════════════════════════════════════════════
-- FUNCTIONS & TRIGGERS
-- ═══════════════════════════════════════════════════════════════

-- Auto-update updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_team_updated BEFORE UPDATE ON team_members FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_gp_updated BEFORE UPDATE ON gp_firms FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_funds_updated BEFORE UPDATE ON funds FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_companies_updated BEFORE UPDATE ON portfolio_companies FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_deals_updated BEFORE UPDATE ON deals FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_lps_updated BEFORE UPDATE ON lps FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_contacts_updated BEFORE UPDATE ON contacts FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_agent_configs_updated BEFORE UPDATE ON agent_configs FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_pacing_updated BEFORE UPDATE ON pacing_models FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_events_updated BEFORE UPDATE ON events FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Auto-calculate fund metrics
CREATE OR REPLACE FUNCTION calc_fund_metrics()
RETURNS TRIGGER AS $$
BEGIN
  -- Calculate TVPI
  IF NEW.called_millions > 0 THEN
    NEW.tvpi = (NEW.nav_millions + COALESCE(NEW.distributed_millions, 0)) / NEW.called_millions;
  END IF;
  -- Calculate DPI
  IF NEW.called_millions > 0 THEN
    NEW.dpi = COALESCE(NEW.distributed_millions, 0) / NEW.called_millions;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_fund_metrics BEFORE INSERT OR UPDATE ON funds FOR EACH ROW EXECUTE FUNCTION calc_fund_metrics();

-- Deal status change → audit log + activity
CREATE OR REPLACE FUNCTION log_deal_change()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.status IS DISTINCT FROM NEW.status THEN
    INSERT INTO deal_activity (deal_id, action, old_value, new_value)
    VALUES (NEW.id, 'status_change', OLD.status::text, NEW.status::text);
  END IF;
  IF OLD.signal IS DISTINCT FROM NEW.signal THEN
    INSERT INTO deal_activity (deal_id, action, old_value, new_value)
    VALUES (NEW.id, 'signal_change', OLD.signal::text, NEW.signal::text);
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_deal_changes AFTER UPDATE ON deals FOR EACH ROW EXECUTE FUNCTION log_deal_change();

-- Portfolio NAV snapshot function
CREATE OR REPLACE FUNCTION snapshot_portfolio_nav()
RETURNS void AS $$
DECLARE
  snap_date DATE := CURRENT_DATE;
BEGIN
  INSERT INTO portfolio_nav_history (
    report_date, total_nav_millions, total_committed_millions,
    total_called_millions, total_distributed_millions,
    weighted_irr, weighted_tvpi, weighted_dpi,
    fund_count, company_count
  )
  SELECT
    snap_date,
    SUM(nav_millions),
    SUM(committed_millions),
    SUM(called_millions),
    SUM(distributed_millions),
    AVG(irr) FILTER (WHERE irr IS NOT NULL),
    AVG(tvpi) FILTER (WHERE tvpi IS NOT NULL),
    AVG(dpi) FILTER (WHERE dpi IS NOT NULL),
    COUNT(*),
    (SELECT COUNT(DISTINCT company_id) FROM fund_company_positions)
  FROM funds
  WHERE status IN ('invested', 'harvesting')
  ON CONFLICT (report_date) DO UPDATE SET
    total_nav_millions = EXCLUDED.total_nav_millions,
    total_committed_millions = EXCLUDED.total_committed_millions,
    total_called_millions = EXCLUDED.total_called_millions,
    total_distributed_millions = EXCLUDED.total_distributed_millions,
    weighted_irr = EXCLUDED.weighted_irr,
    weighted_tvpi = EXCLUDED.weighted_tvpi,
    weighted_dpi = EXCLUDED.weighted_dpi,
    fund_count = EXCLUDED.fund_count,
    company_count = EXCLUDED.company_count;
END;
$$ LANGUAGE plpgsql;

-- Search function for global search
CREATE OR REPLACE FUNCTION search_all(query TEXT)
RETURNS TABLE (
  entity_type TEXT,
  entity_id UUID,
  name TEXT,
  description TEXT,
  relevance REAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT 'fund'::TEXT, f.id, f.name, g.name || ' · ' || f.vintage_year::TEXT,
         similarity(f.name, query) AS rel
  FROM funds f JOIN gp_firms g ON f.gp_firm_id = g.id
  WHERE f.name % query OR g.name % query
  
  UNION ALL
  
  SELECT 'company'::TEXT, c.id, c.name, c.sector || ' · ' || COALESCE(c.stage, ''),
         similarity(c.name, query) AS rel
  FROM portfolio_companies c
  WHERE c.name % query
  
  UNION ALL
  
  SELECT 'deal'::TEXT, d.id, d.name, d.deal_type::TEXT || ' · ' || d.status::TEXT,
         similarity(d.name, query) AS rel
  FROM deals d
  WHERE d.name % query
  
  UNION ALL
  
  SELECT 'contact'::TEXT, ct.id, ct.name, COALESCE(ct.organization, '') || ' · ' || COALESCE(ct.title, ''),
         similarity(ct.name, query) AS rel
  FROM contacts ct
  WHERE ct.name % query
  
  UNION ALL
  
  SELECT 'lp'::TEXT, l.id, l.name, l.lp_type || ' · ' || l.status::TEXT,
         similarity(l.name, query) AS rel
  FROM lps l
  WHERE l.name % query
  
  ORDER BY rel DESC
  LIMIT 20;
END;
$$ LANGUAGE plpgsql;

-- ═══════════════════════════════════════════════════════════════
-- VIEWS (materialized for performance)
-- ═══════════════════════════════════════════════════════════════

-- Portfolio summary view
CREATE MATERIALIZED VIEW mv_portfolio_summary AS
SELECT
  f.id AS fund_id,
  f.name AS fund_name,
  g.name AS gp_name,
  f.vintage_year,
  f.strategy,
  f.status,
  f.committed_millions,
  f.called_millions,
  f.nav_millions,
  f.distributed_millions,
  f.tvpi,
  f.dpi,
  f.irr,
  f.unfunded_millions,
  CASE
    WHEN f.called_millions > 0 THEN f.nav_millions / f.called_millions
    ELSE NULL
  END AS rvpi,
  f.quartile,
  COUNT(DISTINCT fcp.company_id) AS company_count,
  SUM(fcp.current_value_millions) AS total_position_value
FROM funds f
JOIN gp_firms g ON f.gp_firm_id = g.id
LEFT JOIN fund_company_positions fcp ON f.id = fcp.fund_id
WHERE f.status IN ('invested', 'harvesting', 'committed')
GROUP BY f.id, g.name;

CREATE UNIQUE INDEX ON mv_portfolio_summary(fund_id);

-- Deal pipeline summary
CREATE MATERIALIZED VIEW mv_deal_pipeline AS
SELECT
  d.id,
  d.name,
  d.deal_type,
  d.signal,
  d.status,
  d.conviction_score,
  d.target_commitment_millions,
  d.irr_base,
  d.urgency,
  d.deadline,
  t.name AS owner_name,
  g.name AS gp_name,
  f.name AS fund_name,
  COUNT(v.id) AS vote_count,
  COUNT(v.id) FILTER (WHERE v.vote = 'approve') AS approve_count
FROM deals d
LEFT JOIN team_members t ON d.owner_id = t.id
LEFT JOIN gp_firms g ON d.gp_firm_id = g.id
LEFT JOIN funds f ON d.fund_id = f.id
LEFT JOIN ic_votes v ON d.id = v.deal_id
WHERE d.status NOT IN ('fully_realized', 'declined')
GROUP BY d.id, t.name, g.name, f.name
ORDER BY d.conviction_score DESC NULLS LAST;

CREATE UNIQUE INDEX ON mv_deal_pipeline(id);

-- Network graph view
CREATE MATERIALIZED VIEW mv_network_graph AS
SELECT
  c.id,
  c.name,
  c.organization,
  c.tier,
  c.network_score,
  c.influence_score,
  c.relationship_strength,
  c.relationship_owner_id,
  t.name AS owner_name,
  COUNT(DISTINCT ci.id) AS interaction_count,
  MAX(ci.occurred_at) AS last_interaction,
  array_agg(DISTINCT cr.contact_b_id) FILTER (WHERE cr.contact_b_id IS NOT NULL) AS connected_to
FROM contacts c
LEFT JOIN team_members t ON c.relationship_owner_id = t.id
LEFT JOIN contact_interactions ci ON c.id = ci.contact_id
LEFT JOIN contact_relationships cr ON c.id = cr.contact_a_id
GROUP BY c.id, t.name;

CREATE UNIQUE INDEX ON mv_network_graph(id);

-- Refresh function
CREATE OR REPLACE FUNCTION refresh_materialized_views()
RETURNS void AS $$
BEGIN
  REFRESH MATERIALIZED VIEW CONCURRENTLY mv_portfolio_summary;
  REFRESH MATERIALIZED VIEW CONCURRENTLY mv_deal_pipeline;
  REFRESH MATERIALIZED VIEW CONCURRENTLY mv_network_graph;
END;
$$ LANGUAGE plpgsql;

-- ═══════════════════════════════════════════════════════════════
-- SEED DATA: TEAM
-- ═══════════════════════════════════════════════════════════════
INSERT INTO team_members (name, email, role, title, expertise, permissions) VALUES
  ('Jason Goldman', 'jason@newco.vc', 'Operating Partner', 'Operating Partner & Co-Founder', '["VC Operations", "Brand Development", "Berkeley Network", "AI Safety", "Trust & Safety"]', '{"admin": true, "ic_vote": true, "deal_create": true}'),
  ('Ken Wallace', 'ken@newco.vc', 'Managing Partner', 'Managing Partner & CIO', '["Quantitative Analysis", "Secondary Markets", "Portfolio Construction", "Risk Management", "Fund Selection"]', '{"admin": true, "ic_vote": true, "deal_create": true}'),
  ('Bob Burlinson', 'bob@newco.vc', 'Head of Distribution', 'Head of Distribution & Client Relations', '["RIA Distribution", "Platform Approvals", "Client Suitability", "LP Relations", "Mercer-Regis"]', '{"admin": false, "ic_vote": true, "deal_create": true}'),
  ('Brett Brewer', 'brett@newco.vc', 'Partner', 'Partner, Digital & AdTech', '["Digital Advertising", "Trust & Safety", "AdTech", "Growth Equity", "Public Markets"]', '{"admin": false, "ic_vote": true, "deal_create": true}'),
  ('Matthew Goldman', 'matthew@newco.vc', 'Analyst', 'Senior Analyst', '["Financial Modeling", "Due Diligence", "Market Research", "Data Analysis"]', '{"admin": false, "ic_vote": false, "deal_create": true}');

-- ═══════════════════════════════════════════════════════════════
-- SEED DATA: GP FIRMS
-- ═══════════════════════════════════════════════════════════════
INSERT INTO gp_firms (name, slug, hq_city, founded_year, aum_millions, strategy, sector_focus, health_score) VALUES
  ('Founders Fund', 'founders-fund', 'San Francisco', 2005, 12000, 'venture', '["Deep Tech", "AI", "Defense"]', 94),
  ('a16z', 'a16z', 'Menlo Park', 2009, 42000, 'venture', '["AI", "Crypto", "Enterprise", "Bio"]', 92),
  ('NEA', 'nea', 'Menlo Park', 1977, 25000, 'venture', '["Enterprise", "Healthcare", "Deep Tech"]', 88),
  ('General Catalyst', 'general-catalyst', 'Cambridge', 2000, 25000, 'growth', '["AI", "Healthcare", "Fintech"]', 90),
  ('Insight Partners', 'insight', 'New York', 1995, 90000, 'growth', '["Enterprise SaaS", "Data", "Security"]', 82),
  ('Tiger Global', 'tiger-global', 'New York', 2001, 80000, 'growth', '["Internet", "Software", "Consumer"]', 58),
  ('Lightspeed', 'lightspeed', 'Menlo Park', 2000, 18000, 'venture', '["Enterprise", "Consumer", "Crypto"]', 86),
  ('Sequoia Capital', 'sequoia', 'Menlo Park', 1972, 85000, 'venture', '["AI", "Enterprise", "Consumer", "Healthcare"]', 95);

-- ═══════════════════════════════════════════════════════════════
-- SEED DATA: FUNDS
-- ═══════════════════════════════════════════════════════════════
INSERT INTO funds (gp_firm_id, name, vintage_year, strategy, status, fund_size_millions, committed_millions, called_millions, distributed_millions, nav_millions, irr, mgmt_fee_rate, carry_rate, co_invest_rights) VALUES
  ((SELECT id FROM gp_firms WHERE slug='founders-fund'), 'Founders Fund VII', 2021, 'venture', 'invested', 3400, 25.0, 22.5, 2.8, 48.2, 38.5, 0.0200, 0.2000, true),
  ((SELECT id FROM gp_firms WHERE slug='a16z'), 'a16z Infrastructure Fund III', 2022, 'venture', 'invested', 2500, 15.0, 12.0, 0, 18.6, 24.2, 0.0200, 0.2500, true),
  ((SELECT id FROM gp_firms WHERE slug='nea'), 'NEA 19', 2023, 'venture', 'invested', 5200, 20.0, 8.0, 0, 9.2, 15.0, 0.0200, 0.2000, false),
  ((SELECT id FROM gp_firms WHERE slug='general-catalyst'), 'GC Growth V', 2022, 'growth', 'invested', 4800, 18.0, 14.4, 1.2, 22.1, 22.8, 0.0175, 0.2000, true),
  ((SELECT id FROM gp_firms WHERE slug='insight'), 'Insight XII', 2021, 'growth', 'invested', 20000, 30.0, 27.0, 4.5, 35.8, 18.4, 0.0175, 0.2000, false),
  ((SELECT id FROM gp_firms WHERE slug='lightspeed'), 'Lightspeed V', 2020, 'venture', 'harvesting', 4200, 12.0, 11.4, 6.2, 19.8, 28.6, 0.0200, 0.2000, true),
  ((SELECT id FROM gp_firms WHERE slug='sequoia'), 'Sequoia Capital Fund XVI', 2022, 'venture', 'invested', 8000, 22.0, 15.4, 0.5, 26.4, 20.1, 0.0200, 0.3000, true),
  ((SELECT id FROM gp_firms WHERE slug='tiger-global'), 'Tiger Global PIP 15', 2021, 'growth', 'invested', 12700, 0, 0, 0, 0, -12.0, 0.0150, 0.2000, false);

-- ═══════════════════════════════════════════════════════════════
-- SEED DATA: AGENT CONFIGS
-- ═══════════════════════════════════════════════════════════════
INSERT INTO agent_configs (agent_type, name, description, system_prompt, schedule) VALUES
  ('sentinel', 'Sentinel', 'Real-time market monitoring and alert generation. Scans news, SEC filings, PitchBook updates for portfolio-relevant signals.', 'You are Sentinel, the real-time intelligence agent for NEWCO. Monitor all portfolio companies, GP firms, and market signals. Generate alerts for material events.', '*/15 * * * *'),
  ('persona_panel', 'Persona Panel', 'Multi-perspective investment analysis. Simulates IC members with different risk profiles to stress-test investment theses.', 'You are the Persona Panel, simulating multiple investment committee perspectives to stress-test deal theses.', NULL),
  ('living_thesis', 'Living Thesis', 'Dynamic investment thesis tracking. Monitors thesis validity, updates conviction scores, flags thesis drift.', 'You are the Living Thesis agent. Track and update investment theses across the portfolio. Flag when thesis conditions change.', '0 6 * * *'),
  ('dashboard', 'Dashboard Intelligence', 'Generates natural-language portfolio commentary, identifies trends, and produces LP report narratives.', 'You are the Dashboard Intelligence agent. Generate portfolio commentary and trend analysis for the NEWCO team.', '0 8 * * 1'),
  ('pattern_hunter', 'Pattern Hunter', 'Cross-portfolio pattern detection. Identifies correlated risks, emerging themes, and structural opportunities.', 'You are the Pattern Hunter. Identify cross-portfolio patterns, correlated risks, and emerging investment themes.', '0 9 * * *'),
  ('scenario_engine', 'Scenario Engine', 'Monte Carlo simulation and scenario analysis for portfolio outcomes under different market conditions.', 'You are the Scenario Engine. Run portfolio simulations and stress tests under various market scenarios.', '0 7 * * 1'),
  ('network_mapper', 'Network Mapper', 'Relationship intelligence and network optimization. Identifies warm introduction paths and relationship decay.', 'You are the Network Mapper. Analyze the relationship graph, identify optimal connection paths, and flag decaying relationships.', '0 10 * * *'),
  ('capital_optimizer', 'Capital Optimizer', 'Portfolio construction optimization using Kelly criterion, pacing models, and rebalancing recommendations.', 'You are the Capital Optimizer. Optimize portfolio allocation using quantitative frameworks including Kelly criterion and mean-variance optimization.', '0 8 * * 1,4');

-- ═══════════════════════════════════════════════════════════════
-- PUBLIC MARKETS TABLES — NYSE Listed Fund Operations
-- ═══════════════════════════════════════════════════════════════

-- Stock price & trading data
CREATE TABLE stock_prices (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  date DATE NOT NULL,
  open_price DECIMAL(12,4),
  high_price DECIMAL(12,4),
  low_price DECIMAL(12,4),
  close_price DECIMAL(12,4) NOT NULL,
  volume BIGINT,
  vwap DECIMAL(12,4),
  nav_per_share DECIMAL(12,4),
  premium_discount DECIMAL(8,4), -- calculated: (close - nav) / nav
  market_cap DECIMAL(16,2),
  shares_outstanding DECIMAL(14,2),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(date)
);
CREATE INDEX idx_stock_prices_date ON stock_prices(date DESC);

-- NAV marks per position (ASC 820)
CREATE TABLE nav_marks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  quarter TEXT NOT NULL, -- e.g. 'Q4 2025'
  company_id UUID REFERENCES portfolio_companies(id),
  fund_id UUID REFERENCES funds(id),
  fair_value DECIMAL(16,2) NOT NULL,
  asc_820_level INTEGER CHECK (asc_820_level IN (1, 2, 3)),
  methodology TEXT NOT NULL, -- 'last_round_calibration', 'comparable_public', 'secondary_market', 'dcf', 'quoted_price'
  valuation_agent TEXT, -- 'Houlihan Lokey', 'Lincoln International', etc.
  confidence_score INTEGER CHECK (confidence_score BETWEEN 0 AND 100),
  prior_mark DECIMAL(16,2),
  change_pct DECIMAL(8,4),
  notes TEXT,
  approved_by UUID REFERENCES team_members(id),
  approved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE nav_marks ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read nav_marks" ON nav_marks FOR SELECT TO authenticated USING (true);

-- Fair Value Committee meetings
CREATE TABLE fvc_meetings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  quarter TEXT NOT NULL,
  meeting_date DATE NOT NULL,
  status TEXT DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'in_progress', 'completed', 'approved')),
  chair_id UUID REFERENCES team_members(id),
  attendees UUID[],
  quorum_met BOOLEAN DEFAULT false,
  total_nav DECIMAL(16,2),
  nav_per_share DECIMAL(12,4),
  change_from_prior DECIMAL(8,4),
  external_valuation_agents TEXT[],
  audit_firm TEXT DEFAULT 'KPMG',
  board_approved BOOLEAN DEFAULT false,
  board_approved_at TIMESTAMPTZ,
  minutes_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE fvc_meetings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read fvc_meetings" ON fvc_meetings FOR SELECT TO authenticated USING (true);

-- Institutional shareholders (13F tracking)
CREATE TABLE shareholders (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  institution_name TEXT NOT NULL,
  institution_type TEXT CHECK (institution_type IN ('index', 'quant', 'hedge_fund', 'multi_strat', 'thematic', 'quant_value', 'pension', 'endowment', 'ria', 'retail_broker', 'other')),
  shares_held DECIMAL(14,2) NOT NULL,
  pct_outstanding DECIMAL(8,4),
  market_value DECIMAL(16,2),
  change_shares DECIMAL(14,2) DEFAULT 0,
  change_type TEXT CHECK (change_type IN ('new', 'increased', 'decreased', 'unchanged', 'exited')),
  filing_quarter TEXT NOT NULL,
  filing_date DATE,
  strategy_notes TEXT,
  cost_basis_est DECIMAL(12,4),
  is_activist BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE shareholders ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read shareholders" ON shareholders FOR SELECT TO authenticated USING (true);
CREATE INDEX idx_shareholders_institution ON shareholders(institution_name);
CREATE INDEX idx_shareholders_quarter ON shareholders(filing_quarter DESC);

-- Short interest tracking
CREATE TABLE short_interest (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  report_date DATE NOT NULL,
  short_shares DECIMAL(14,2) NOT NULL,
  pct_float DECIMAL(8,4),
  days_to_cover DECIMAL(8,2),
  borrow_cost_annualized DECIMAL(8,4),
  squeeze_score INTEGER CHECK (squeeze_score BETWEEN 0 AND 100),
  change_from_prior DECIMAL(14,2),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(report_date)
);
ALTER TABLE short_interest ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read short_interest" ON short_interest FOR SELECT TO authenticated USING (true);

-- SEC filings tracker
CREATE TABLE sec_filings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  form_type TEXT NOT NULL, -- 'N-CSR', 'N-CSRS', 'N-PORT', 'N-CEN', 'DEF14A', 'Form4', '13F', '8-K'
  filing_name TEXT NOT NULL,
  filing_deadline DATE NOT NULL,
  status TEXT DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'review', 'filed', 'overdue')),
  preparer_id UUID REFERENCES team_members(id),
  reviewer_id UUID REFERENCES team_members(id),
  external_counsel TEXT,
  filed_date DATE,
  sec_accession_number TEXT,
  edgar_url TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE sec_filings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read sec_filings" ON sec_filings FOR SELECT TO authenticated USING (true);

-- ATM (At-the-Market) program transactions
CREATE TABLE atm_transactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  transaction_date DATE NOT NULL,
  shares_sold DECIMAL(14,2) NOT NULL,
  avg_price DECIMAL(12,4) NOT NULL,
  gross_proceeds DECIMAL(16,2) NOT NULL,
  commission DECIMAL(12,2),
  net_proceeds DECIMAL(16,2) NOT NULL,
  nav_per_share_at_sale DECIMAL(12,4),
  premium_captured DECIMAL(8,4),
  program_name TEXT DEFAULT 'ATM-2025',
  program_capacity_remaining DECIMAL(16,2),
  broker_dealer TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE atm_transactions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read atm_transactions" ON atm_transactions FOR SELECT TO authenticated USING (true);

-- Share buyback program
CREATE TABLE buyback_transactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  transaction_date DATE NOT NULL,
  shares_repurchased DECIMAL(14,2) NOT NULL,
  avg_price DECIMAL(12,4) NOT NULL,
  total_cost DECIMAL(16,2) NOT NULL,
  nav_per_share_at_purchase DECIMAL(12,4),
  discount_to_nav DECIMAL(8,4),
  nav_accretion_per_share DECIMAL(12,6),
  authorization_remaining DECIMAL(16,2),
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE buyback_transactions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read buyback_transactions" ON buyback_transactions FOR SELECT TO authenticated USING (true);

-- IPO / exit event tracking
CREATE TABLE ipo_events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_id UUID REFERENCES portfolio_companies(id),
  event_type TEXT NOT NULL CHECK (event_type IN ('ipo', 'direct_listing', 'spac', 'tender_offer', 'secondary_sale', 'acquisition', 'merger')),
  estimated_timeline TEXT,
  estimated_valuation_low DECIMAL(16,2),
  estimated_valuation_high DECIMAL(16,2),
  current_mark DECIMAL(16,2),
  nav_impact_pct DECIMAL(8,4),
  probability INTEGER CHECK (probability BETWEEN 0 AND 100),
  status TEXT DEFAULT 'monitoring' CHECK (status IN ('monitoring', 'exploring', 'confidential_filing', 's1_prep', 's1_filed', 'roadshow', 'priced', 'completed', 'cancelled')),
  lockup_days INTEGER DEFAULT 180,
  lockup_expiry DATE,
  our_exposure DECIMAL(16,2), -- look-through dollar exposure
  fund_sources TEXT[], -- which funds give us exposure
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE ipo_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read ipo_events" ON ipo_events FOR SELECT TO authenticated USING (true);

-- Board members & governance
CREATE TABLE board_members (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  role TEXT NOT NULL,
  is_independent BOOLEAN DEFAULT false,
  committees TEXT[],
  term_expires DATE,
  shares_owned DECIMAL(14,2) DEFAULT 0,
  expertise TEXT,
  bio TEXT,
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE board_members ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read board_members" ON board_members FOR SELECT TO authenticated USING (true);

-- Insider trading window
CREATE TABLE trading_windows (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  window_type TEXT CHECK (window_type IN ('open', 'closed', 'blackout')),
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  reason TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE trading_windows ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read trading_windows" ON trading_windows FOR SELECT TO authenticated USING (true);

-- Insider transactions (Form 4)
CREATE TABLE insider_transactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  person_name TEXT NOT NULL,
  role TEXT NOT NULL,
  transaction_date DATE NOT NULL,
  transaction_type TEXT CHECK (transaction_type IN ('purchase', 'sale', 'grant', 'exercise', 'gift')),
  shares DECIMAL(14,2) NOT NULL,
  price DECIMAL(12,4),
  total_value DECIMAL(16,2),
  pre_cleared BOOLEAN DEFAULT false,
  form4_filed DATE,
  sec_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE insider_transactions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read insider_transactions" ON insider_transactions FOR SELECT TO authenticated USING (true);

-- IR meetings & analyst coverage
CREATE TABLE ir_meetings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  institution_name TEXT NOT NULL,
  contact_name TEXT,
  meeting_type TEXT CHECK (meeting_type IN ('one_on_one', 'group', 'conference', 'call', 'site_visit', 'investor_day', 'non_deal_roadshow')),
  meeting_date DATE NOT NULL,
  attendees UUID[], -- team_members
  topics TEXT[],
  outcome TEXT,
  follow_up TEXT,
  sentiment TEXT CHECK (sentiment IN ('very_positive', 'positive', 'neutral', 'negative', 'very_negative')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE ir_meetings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read ir_meetings" ON ir_meetings FOR SELECT TO authenticated USING (true);

-- Earnings call Q&A bank
CREATE TABLE qa_bank (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  category TEXT NOT NULL,
  question TEXT NOT NULL,
  approved_answer TEXT NOT NULL,
  frequency_asked INTEGER DEFAULT 0,
  last_asked DATE,
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'review', 'retired')),
  owner_id UUID REFERENCES team_members(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE qa_bank ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read qa_bank" ON qa_bank FOR SELECT TO authenticated USING (true);

-- Defensive governance measures
CREATE TABLE governance_measures (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  measure_name TEXT NOT NULL,
  measure_type TEXT CHECK (measure_type IN ('poison_pill', 'classified_board', 'supermajority', 'advance_notice', 'forum_selection', 'dno_insurance', 'bylaw_provision', 'other')),
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'not_adopted', 'expired', 'under_review')),
  effective_date DATE,
  expiry_date DATE,
  trigger_threshold DECIMAL(8,4), -- e.g. 0.15 for 15% ownership trigger
  details TEXT,
  risk_level TEXT CHECK (risk_level IN ('low', 'medium', 'high')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE governance_measures ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read governance_measures" ON governance_measures FOR SELECT TO authenticated USING (true);

-- Compliance checklist items (1940 Act)
CREATE TABLE compliance_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  requirement TEXT NOT NULL,
  regulation TEXT NOT NULL, -- '1940 Act', 'SEC Rule 17j-1', 'Reg S-X', etc.
  status TEXT DEFAULT 'compliant' CHECK (status IN ('compliant', 'non_compliant', 'scheduled', 'na', 'under_review')),
  current_value TEXT,
  threshold_value TEXT,
  risk_level TEXT CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
  last_reviewed DATE,
  reviewer_id UUID REFERENCES team_members(id),
  next_review DATE,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE compliance_items ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read compliance_items" ON compliance_items FOR SELECT TO authenticated USING (true);

-- Look-through exposure decomposition
CREATE TABLE look_through_exposure (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  quarter TEXT NOT NULL,
  company_name TEXT NOT NULL,
  fund_sources TEXT[] NOT NULL,
  pct_nav DECIMAL(8,4) NOT NULL,
  sector TEXT,
  sub_sector TEXT,
  stage TEXT CHECK (stage IN ('seed', 'series_a', 'early_growth', 'growth', 'late_stage', 'pre_ipo', 'public')),
  geography TEXT,
  themes TEXT[],
  revenue DECIMAL(16,2),
  revenue_growth DECIMAL(8,4),
  valuation DECIMAL(16,2),
  our_exposure_dollars DECIMAL(16,2),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(quarter, company_name)
);
ALTER TABLE look_through_exposure ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Authenticated read look_through_exposure" ON look_through_exposure FOR SELECT TO authenticated USING (true);
CREATE INDEX idx_look_through_quarter ON look_through_exposure(quarter DESC);
CREATE INDEX idx_look_through_sector ON look_through_exposure(sector);

-- ═══ Materialized view: Public Markets Summary ═══
CREATE MATERIALIZED VIEW mv_public_markets_summary AS
SELECT
  sp.date,
  sp.close_price,
  sp.nav_per_share,
  sp.premium_discount,
  sp.volume,
  sp.market_cap,
  sp.shares_outstanding,
  si.short_shares,
  si.pct_float AS short_pct_float,
  si.days_to_cover,
  si.borrow_cost_annualized,
  si.squeeze_score,
  (SELECT SUM(net_proceeds) FROM atm_transactions WHERE transaction_date >= CURRENT_DATE - INTERVAL '30 days') AS atm_proceeds_30d,
  (SELECT SUM(total_cost) FROM buyback_transactions WHERE transaction_date >= CURRENT_DATE - INTERVAL '30 days') AS buyback_cost_30d,
  (SELECT COUNT(*) FROM ipo_events WHERE status IN ('s1_prep', 's1_filed', 'confidential_filing', 'roadshow')) AS active_ipo_pipeline
FROM stock_prices sp
LEFT JOIN short_interest si ON si.report_date = (SELECT MAX(report_date) FROM short_interest WHERE report_date <= sp.date)
WHERE sp.date >= CURRENT_DATE - INTERVAL '365 days'
ORDER BY sp.date DESC;

CREATE UNIQUE INDEX idx_mv_public_markets_date ON mv_public_markets_summary(date);

-- ═══ Function: Calculate premium/discount automatically ═══
CREATE OR REPLACE FUNCTION calc_premium_discount()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.nav_per_share IS NOT NULL AND NEW.nav_per_share > 0 THEN
    NEW.premium_discount := (NEW.close_price - NEW.nav_per_share) / NEW.nav_per_share;
  END IF;
  IF NEW.close_price IS NOT NULL AND NEW.shares_outstanding IS NOT NULL THEN
    NEW.market_cap := NEW.close_price * NEW.shares_outstanding;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_calc_premium_discount
  BEFORE INSERT OR UPDATE ON stock_prices
  FOR EACH ROW EXECUTE FUNCTION calc_premium_discount();

-- ═══ SEED DATA: PUBLIC MARKETS ═══

-- Board members
INSERT INTO board_members (name, role, is_independent, committees, term_expires, shares_owned, expertise) VALUES
  ('Jason Goldman', 'Chair & Operating Partner', false, ARRAY['FVC Chair', 'Executive'], '2027-06-30', 142500, 'VC Ops, Brand, Berkeley Network'),
  ('Ken Wallace', 'Managing Partner & CIO', false, ARRAY['FVC', 'Investment'], '2027-06-30', 98200, 'Quant, Secondaries, Risk'),
  ('Dr. Sarah Chen', 'Independent Director', true, ARRAY['Audit Chair', 'Compensation'], '2028-06-30', 5000, 'AI/ML Professor, Stanford AI Lab'),
  ('Robert Martinez', 'Independent Director', true, ARRAY['Governance Chair', 'FVC'], '2026-06-30', 8000, 'Former SEC Commissioner, Compliance'),
  ('Linda Park', 'Independent Director', true, ARRAY['Compensation Chair', 'Audit'], '2028-06-30', 12000, 'Former BlackRock PM, Alts Specialist');

-- Current trading window
INSERT INTO trading_windows (window_type, start_date, end_date, reason) VALUES
  ('closed', '2026-02-01', '2026-03-30', 'Q4 2025 earnings preparation and NAV mark finalization');

-- Governance measures
INSERT INTO governance_measures (measure_name, measure_type, status, effective_date, expiry_date, trigger_threshold, details, risk_level) VALUES
  ('Shareholder Rights Plan', 'poison_pill', 'active', '2025-11-15', '2028-11-15', 0.15, '15% ownership trigger. Flip-in provision dilutes hostile acquirer.', 'low'),
  ('Supermajority Vote for Amendments', 'supermajority', 'active', '2025-06-01', NULL, 0.667, '66.7% required to amend bylaws or remove directors without cause.', 'low'),
  ('Advance Notice Bylaw', 'advance_notice', 'active', '2025-06-01', NULL, NULL, '90-120 day advance notice required for director nominations.', 'low'),
  ('Forum Selection Clause', 'forum_selection', 'active', '2025-06-01', NULL, NULL, 'All derivative actions must be brought in Delaware Court of Chancery.', 'low'),
  ('D&O Insurance Tower', 'dno_insurance', 'active', '2025-01-01', '2026-01-01', NULL, '$25M tower. Primary: AIG. Excess: Chubb + Berkshire.', 'low');

-- ATM Agent config
INSERT INTO agent_configs (agent_type, name, description, system_prompt, schedule) VALUES
  ('ir_intelligence', 'IR Intelligence', 'Monitors shareholder activity, 13F filings, short interest, and analyst sentiment. Generates IR briefings.', 'You are the IR Intelligence agent. Monitor institutional ownership changes, short interest, analyst coverage, and retail sentiment. Generate weekly IR briefings for the team.', '0 7 * * 1'),
  ('compliance_monitor', 'Compliance Monitor', 'Tracks SEC filing deadlines, 1940 Act requirements, trading windows, and regulatory changes.', 'You are the Compliance Monitor agent. Track all SEC filing deadlines, 1940 Act requirements, and regulatory changes that affect a registered closed-end fund.', '0 6 * * *');

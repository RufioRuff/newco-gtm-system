# Supabase Setup Guide - NEWCO V10 Platform

## Overview

This guide walks you through setting up Supabase (PostgreSQL database + Edge Functions) for the NEWCO V10 platform.

**Why Supabase?**
- PostgreSQL database with real-time subscriptions
- Row-level security (RLS) for data protection
- Edge Functions for serverless compute
- Built-in authentication
- GraphQL API (via RedwoodJS)

---

## Step 1: Create Supabase Project

### **1.1 Sign Up**
1. Go to [https://supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign up with GitHub (recommended) or email

### **1.2 Create New Project**
1. Click "New Project"
2. Choose settings:
   - **Name:** `newco-v10` (or your preference)
   - **Database Password:** Generate strong password (save this!)
   - **Region:** Choose closest to you (e.g., US West for California)
   - **Plan:** Free tier is fine for development

3. Click "Create new project"
4. Wait 2-3 minutes for provisioning

---

## Step 2: Get API Credentials

### **2.1 Navigate to Settings**
1. Click "Project Settings" (gear icon in sidebar)
2. Click "API" in left menu

### **2.2 Copy Credentials**
You'll need these for `.env`:

```bash
# Project URL
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co

# Anon (public) key
SUPABASE_ANON_KEY=eyJhbG...very-long-key

# Service role (secret) key
SUPABASE_SERVICE_ROLE_KEY=eyJhbG...even-longer-secret-key
```

⚠️ **Never commit service role key to git!**

### **2.3 Get Database Connection String**
1. Go to "Project Settings" → "Database"
2. Scroll to "Connection string"
3. Copy the "URI" format:

```bash
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

Replace `[YOUR-PASSWORD]` with your database password from Step 1.2

---

## Step 3: Create Database Schema

### **3.1 Open SQL Editor**
1. Click "SQL Editor" in Supabase sidebar
2. Click "New query"

### **3.2 Run Schema Creation**

Copy and paste this SQL to create the database structure:

```sql
-- ════════════════════════════════════════════════════════
-- NEWCO V10 DATABASE SCHEMA
-- ════════════════════════════════════════════════════════

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ════════════════════════════════════════════════════════
-- FUNDS TABLE
-- ════════════════════════════════════════════════════════

CREATE TABLE funds (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  fund_id TEXT UNIQUE NOT NULL,
  fund_name TEXT NOT NULL,
  gp_name TEXT NOT NULL,
  vintage INTEGER,
  commitment_amount NUMERIC(12, 2),
  total_called NUMERIC(12, 2),
  total_distributed NUMERIC(12, 2),
  current_nav NUMERIC(12, 2),
  fund_type TEXT,
  sector TEXT,
  status TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ════════════════════════════════════════════════════════
-- PORTFOLIO COMPANIES TABLE
-- ════════════════════════════════════════════════════════

CREATE TABLE portfolio_companies (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_id TEXT UNIQUE NOT NULL,
  company_name TEXT NOT NULL,
  fund_id TEXT REFERENCES funds(fund_id),
  fund_name TEXT,
  gp_name TEXT,
  sector TEXT,
  stage TEXT,
  status TEXT,
  investment_date DATE,
  exit_date DATE,
  exit_type TEXT,
  valuation_estimate NUMERIC(15, 2),
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ════════════════════════════════════════════════════════
-- TEAM MEMBERS TABLE
-- ════════════════════════════════════════════════════════

CREATE TABLE team_members (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  member_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  role TEXT,
  email TEXT,
  status TEXT DEFAULT 'Active',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ════════════════════════════════════════════════════════
-- CAPITAL CALLS TABLE
-- ════════════════════════════════════════════════════════

CREATE TABLE capital_calls (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  call_id TEXT UNIQUE NOT NULL,
  fund_id TEXT REFERENCES funds(fund_id),
  call_date DATE NOT NULL,
  amount NUMERIC(12, 2) NOT NULL,
  due_date DATE,
  status TEXT DEFAULT 'Pending',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ════════════════════════════════════════════════════════
-- DISTRIBUTIONS TABLE
-- ════════════════════════════════════════════════════════

CREATE TABLE distributions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  distribution_id TEXT UNIQUE NOT NULL,
  fund_id TEXT REFERENCES funds(fund_id),
  distribution_date DATE NOT NULL,
  amount NUMERIC(12, 2) NOT NULL,
  type TEXT, -- 'Return of Capital', 'Capital Gain', 'Income'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ════════════════════════════════════════════════════════
-- USERS TABLE (for authentication)
-- ════════════════════════════════════════════════════════

CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  email TEXT UNIQUE NOT NULL,
  role TEXT NOT NULL DEFAULT 'analyst', -- admin, analyst, lp_viewer, board_member
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ════════════════════════════════════════════════════════
-- INDEXES for performance
-- ════════════════════════════════════════════════════════

CREATE INDEX idx_funds_gp ON funds(gp_name);
CREATE INDEX idx_funds_vintage ON funds(vintage);
CREATE INDEX idx_funds_status ON funds(status);

CREATE INDEX idx_companies_fund ON portfolio_companies(fund_id);
CREATE INDEX idx_companies_sector ON portfolio_companies(sector);
CREATE INDEX idx_companies_status ON portfolio_companies(status);

CREATE INDEX idx_capital_calls_fund ON capital_calls(fund_id);
CREATE INDEX idx_capital_calls_date ON capital_calls(call_date);

CREATE INDEX idx_distributions_fund ON distributions(fund_id);
CREATE INDEX idx_distributions_date ON distributions(distribution_date);

-- ════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ════════════════════════════════════════════════════════

-- Enable RLS
ALTER TABLE funds ENABLE ROW LEVEL SECURITY;
ALTER TABLE portfolio_companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE capital_calls ENABLE ROW LEVEL SECURITY;
ALTER TABLE distributions ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Admin: Full access to everything
CREATE POLICY "Admins have full access to funds"
  ON funds FOR ALL
  USING (EXISTS (
    SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin'
  ));

CREATE POLICY "Admins have full access to companies"
  ON portfolio_companies FOR ALL
  USING (EXISTS (
    SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin'
  ));

-- Analysts: Read all, write some
CREATE POLICY "Analysts can read funds"
  ON funds FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM users WHERE id = auth.uid() AND role IN ('analyst', 'admin')
  ));

CREATE POLICY "Analysts can read companies"
  ON portfolio_companies FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM users WHERE id = auth.uid() AND role IN ('analyst', 'admin')
  ));

-- LP Viewers: Read-only access
CREATE POLICY "LP viewers can read funds"
  ON funds FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM users WHERE id = auth.uid() AND role IN ('lp_viewer', 'board_member', 'analyst', 'admin')
  ));

-- Board members: Read-only, but all tables
CREATE POLICY "Board can read funds"
  ON funds FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM users WHERE id = auth.uid() AND role IN ('board_member', 'admin')
  ));

-- ════════════════════════════════════════════════════════
-- FUNCTIONS
-- ════════════════════════════════════════════════════════

-- Update timestamp function
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add update triggers
CREATE TRIGGER update_funds_updated_at
  BEFORE UPDATE ON funds
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_companies_updated_at
  BEFORE UPDATE ON portfolio_companies
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_team_updated_at
  BEFORE UPDATE ON team_members
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

3. Click "Run" to execute
4. Verify tables created: Check "Table Editor" in sidebar

---

## Step 4: Load Your Real Data

### **4.1 Option A: Manual CSV Import (Easiest)**

1. Go to "Table Editor" in Supabase
2. Select "funds" table
3. Click "Insert" → "Import data via spreadsheet"
4. Upload `/Users/rufio/NEWCO/data/portfolio_funds.csv`
5. Map columns and import

6. Repeat for "portfolio_companies" table with:
   `/Users/rufio/NEWCO/data/portfolio_companies.csv`

### **4.2 Option B: SQL Insert (Automated)**

Create a script to load data:

```bash
cd /Users/rufio/NEWCO/alpha-engine

# Create data loader script
cat > scripts/load-data-to-supabase.js << 'EOF'
const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const csv = require('csv-parser');

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function loadFunds() {
  const funds = [];

  fs.createReadStream('/Users/rufio/NEWCO/data/portfolio_funds.csv')
    .pipe(csv())
    .on('data', (row) => funds.push(row))
    .on('end', async () => {
      const { data, error } = await supabase
        .from('funds')
        .insert(funds);

      if (error) console.error('Error:', error);
      else console.log('✓ Loaded', funds.length, 'funds');
    });
}

async function loadCompanies() {
  const companies = [];

  fs.createReadStream('/Users/rufio/NEWCO/data/portfolio_companies.csv')
    .pipe(csv())
    .on('data', (row) => companies.push(row))
    .on('end', async () => {
      const { data, error } = await supabase
        .from('portfolio_companies')
        .insert(companies);

      if (error) console.error('Error:', error);
      else console.log('✓ Loaded', companies.length, 'companies');
    });
}

loadFunds();
loadCompanies();
EOF

# Install dependencies
yarn add @supabase/supabase-js csv-parser

# Run loader
node scripts/load-data-to-supabase.js
```

---

## Step 5: Configure RedwoodJS

### **5.1 Update .env**

Copy `.env.local` to `.env` and fill in your Supabase credentials:

```bash
cd /Users/rufio/NEWCO/alpha-engine
cp .env.local .env
```

Edit `.env` with your values from Step 2.

### **5.2 Configure Supabase Auth**

1. In Supabase dashboard, go to "Authentication" → "Providers"
2. Enable "Email" provider (default is fine)
3. Optional: Enable Google, GitHub SSO

### **5.3 Test Database Connection**

```bash
# Install PostgreSQL client
brew install postgresql

# Test connection
psql $DATABASE_URL -c "SELECT COUNT(*) FROM funds;"
```

Should return count of your funds (85).

---

## Step 6: Start Development Server

```bash
cd /Users/rufio/NEWCO/alpha-engine

# Start RedwoodJS dev server
yarn rw dev
```

This starts:
- **Web:** http://localhost:8910 (React frontend)
- **API:** http://localhost:8911 (GraphQL API)

---

## Step 7: Create First User

### **7.1 Sign Up**
1. Open http://localhost:8910
2. If there's a login screen, click "Sign up"
3. Enter email and password
4. Check email for verification link

### **7.2 Set User Role**

In Supabase SQL Editor:

```sql
-- Give yourself admin role
UPDATE users
SET role = 'admin'
WHERE email = 'your-email@example.com';
```

---

## Step 8: Verify Everything Works

### **8.1 Test GraphQL API**

Open GraphQL Playground: http://localhost:8911/graphql

Try query:

```graphql
query {
  funds {
    id
    fundName
    gpName
    commitmentAmount
    tvpi
    status
  }
}
```

Should return your 85 funds!

### **8.2 Test Web Interface**

1. Open http://localhost:8910
2. Should see AlphaEngine dashboard
3. Verify funds and companies displayed

---

## Troubleshooting

### **Issue: "Could not connect to database"**

**Fix:**
1. Check DATABASE_URL is correct
2. Verify database password
3. Check firewall/network settings
4. Try connecting via psql first

### **Issue: "No permission to access table"**

**Fix:**
1. Verify RLS policies created (Step 3.2)
2. Check user role: `SELECT * FROM users WHERE email = 'your-email';`
3. Temporarily disable RLS for testing: `ALTER TABLE funds DISABLE ROW LEVEL SECURITY;`

### **Issue: "API not responding"**

**Fix:**
```bash
# Restart dev server
yarn rw dev

# Check ports available
lsof -i :8910
lsof -i :8911
```

### **Issue: "CORS errors"**

**Fix:**
1. In Supabase, go to "Project Settings" → "API"
2. Add http://localhost:8910 to allowed origins
3. Restart dev server

---

## Next Steps

### **Deploy to Production**

See `DEPLOYMENT_GUIDE.md` for instructions on:
- Deploying to Vercel
- Setting up production Supabase
- Configuring CI/CD
- Setting up monitoring

### **Add More Data**

- Import capital calls
- Import distributions
- Add team members
- Configure LP portal access

### **Enable Advanced Features**

- Set up Edge Functions for real-time NAV calculations
- Configure secondary market data feeds
- Enable AI agent features
- Set up email notifications

---

## Resources

- **Supabase Docs:** https://supabase.com/docs
- **RedwoodJS Docs:** https://redwoodjs.com/docs
- **Your Data:** `/Users/rufio/NEWCO/data/`
- **API Reference:** `/Users/rufio/NEWCO/QUICK_START.md`

---

## Summary

✅ **What You Set Up:**
- PostgreSQL database in Supabase
- Tables for funds, companies, capital calls, distributions
- Row-level security (RLS) policies
- Authentication with role-based access
- GraphQL API via RedwoodJS
- Development environment

✅ **What's Next:**
- Load your 85 funds + 62 companies
- Create your user account
- Test the web interface
- Deploy to production (optional)

Your NEWCO V10 platform is now ready for professional deployment! 🚀

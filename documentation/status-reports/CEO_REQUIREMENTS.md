# CEO Requirements - Ken Wallace Perspective
## What I Actually Need to Run NEWCO

*From the desk of Ken Wallace, CEO*

Look, I love what we've built so far - the GTM tools, network analysis, and public markets tracking are solid. But as CEO of a publicly traded VC fund-of-funds, I need **operational tools that help me run the business**, not just raise capital.

Here's what's missing from my daily workflow:

---

## 1. Portfolio Management & Monitoring 🎯

**What I Need:**

### Fund Investment Tracking
```bash
# I need to track our 15-20 underlying fund investments
./scripts/newco_cli.py portfolio show

# For each fund:
- Commitment size ($2-5M)
- Capital called to date
- Capital remaining
- Current NAV
- TVPI, DPI, RVPI
- Vintage year
- Stage focus (seed, A, B, etc.)
- Sector focus
- Geography
- Manager contacts
```

**Why:** I need to know where our $50M is deployed at all times.

### Capital Call Forecasting
```bash
# When will I need to have cash ready?
./scripts/newco_cli.py portfolio cashflow --forecast 12

# Show:
- Expected capital calls by month
- Cash reserves needed
- Distributions expected
- Net cash position
```

**Why:** Public company CEOs get fired for missing capital calls or holding too much idle cash.

### Portfolio Construction Analysis
```bash
# Am I diversified properly?
./scripts/newco_cli.py portfolio analyze --diversification

# Show concentration by:
- Vintage year (no more than 30% in any single year)
- Stage (balanced across seed/A/B/growth)
- Sector (no more than 40% in any sector)
- Geography (West Coast vs East Coast vs International)
- Manager (no more than 15% in any single fund)
```

**Why:** My board will crucify me if we're over-concentrated.

---

## 2. Manager Relationship Management 🤝

**What I Need:**

### Fund Manager CRM
```bash
# Different from LP CRM - this is for FUND MANAGERS
./scripts/newco_cli.py managers list

# For each manager:
- Fund name
- GP names and backgrounds
- Investment strategy
- Track record (IRR, MOIC)
- Our relationship status
- Next meeting date
- Due diligence status
- Investment committee decision
```

**Why:** I'm managing relationships with 15-20 fund managers. I can't confuse them with LPs!

### Manager Pipeline
```bash
# Who are we evaluating for next fund?
./scripts/newco_cli.py managers pipeline

# Stages:
- Sourced (50+ managers)
- Initial screening (20 managers)
- Deep due diligence (10 managers)
- Investment committee (5 managers)
- Committed (2-3 per quarter)
- Passed (tracking for future)
```

**Why:** I need a healthy pipeline to deploy capital consistently.

### Due Diligence Tracking
```bash
# Where are we in DD process?
./scripts/newco_cli.py managers dd-status [manager_name]

# Checklist:
- [ ] Initial call completed
- [ ] Track record verified
- [ ] Reference checks (3+ LPs)
- [ ] Strategy deep dive
- [ ] Portfolio company visits (3+)
- [ ] Operations review
- [ ] Legal review (LPA, side letters)
- [ ] IC memo drafted
- [ ] IC approval
- [ ] Terms negotiated
- [ ] Committed
```

**Why:** We do 6-8 week due diligence on each manager. I need to track progress.

---

## 3. Performance Attribution & Reporting 📊

**What I Need:**

### Fund Performance Dashboard
```bash
# How are our funds performing?
./scripts/newco_cli.py portfolio performance

# Show by fund:
- TVPI (Total Value / Paid In)
- DPI (Distributions / Paid In)
- RVPI (Residual Value / Paid In)
- IRR (Internal Rate of Return)
- vs Vintage year benchmark
- vs Our target (top quartile)
```

**Why:** This goes in my quarterly board deck and earnings calls.

### Attribution Analysis
```bash
# What's driving our returns?
./scripts/newco_cli.py portfolio attribution

# Break down NAV growth by:
- Unrealized appreciation (fund NAVs up)
- Realized gains (distributions received)
- New commitments (capital deployed)
- Fee drag (management fees paid)
- FX impact (if any international)
```

**Why:** Analysts will ask me exactly this on earnings calls.

### Benchmark Comparison
```bash
# How do we compare to benchmarks?
./scripts/newco_cli.py portfolio benchmark

# Compare to:
- Cambridge Associates US VC index
- Pitchbook VC fund-of-funds benchmark
- Public VC comparables (HTGC, TPVG)
- Top quartile VC threshold
```

**Why:** "Are you generating alpha?" - Every analyst, every quarter.

---

## 4. Risk Management 🛡️

**What I Need:**

### Concentration Risk
```bash
# Am I too concentrated anywhere?
./scripts/newco_cli.py risk concentration

# Flag if:
- Any single fund > 15% of portfolio
- Any vintage year > 30% of portfolio
- Any sector > 40% of portfolio
- Top 3 funds > 40% of portfolio
```

**Why:** Concentration = career risk for me.

### Correlation Analysis
```bash
# Are my funds correlated?
./scripts/newco_cli.py risk correlation

# Show:
- Funds that invest in same companies
- Managers who co-invest together
- Sector overlap
- Stage overlap
```

**Why:** If funds are highly correlated, I'm not actually diversified.

### Vintage Year Risk
```bash
# Am I exposed to bad vintage years?
./scripts/newco_cli.py risk vintage

# Show:
- % deployed in 2020-2021 (peak bubble years)
- % deployed in 2023-2024 (correction years)
- Optimal: spread across 3-4 vintages
```

**Why:** Vintage year is the #1 driver of VC returns.

### Liquidity Risk
```bash
# Can I meet capital calls?
./scripts/newco_cli.py risk liquidity

# Show:
- Unfunded commitments
- Expected capital calls (12 months)
- Cash on hand
- Public stock liquidity
- Credit facility availability
```

**Why:** Missing a capital call = default = disaster.

---

## 5. Board & Governance 🏛️

**What I Need:**

### Board Meeting Prep
```bash
# Generate board deck automatically
./scripts/newco_cli.py board prep --meeting Q1-2026

# Auto-generate:
- Portfolio overview (1 slide)
- Performance by fund (1 slide)
- Capital deployment (1 slide)
- Pipeline status (1 slide)
- Public market performance (1 slide)
- Risk dashboard (1 slide)
- Action items from last meeting
```

**Why:** Board meetings are quarterly. I need this automated.

### Investment Committee Management
```bash
# Track IC decisions
./scripts/newco_cli.py ic list

# For each IC meeting:
- Date
- Attendees
- Managers presented
- Decisions made
- Vote results
- Follow-up items
```

**Why:** IC governance is crucial for fiduciary duty.

### Governance Compliance
```bash
# Are we compliant with our investment policy?
./scripts/newco_cli.py governance check

# Verify:
- [ ] Diversification requirements met
- [ ] No single fund > 15%
- [ ] Minimum 10 fund investments
- [ ] Cash reserves > 10% of NAV
- [ ] All funds < $250M AUM (our mandate)
```

**Why:** If I breach investment policy, I'm personally liable.

---

## 6. LP Reporting Automation 📝

**What I Need:**

### Quarterly Letter Generation
```bash
# Auto-generate quarterly LP letter
./scripts/newco_cli.py lp-reporting letter --quarter Q1-2026

# Include:
- CEO letter (I write this)
- Portfolio summary (auto-generated)
- Performance metrics (auto-generated)
- Manager updates (I write highlights)
- Market commentary (I write this)
- Upcoming capital calls
```

**Why:** I spend 40 hours per quarter on LP letters. Automate what I can.

### Data Room Management
```bash
# What do LPs have access to?
./scripts/newco_cli.py lp-reporting dataroom

# Track:
- Who has access (which LPs)
- What they can see (fund details, performance)
- Download history
- Questions asked
```

**Why:** LPs have information rights. I need to track this.

### Capital Call Notices
```bash
# Send capital call notice
./scripts/newco_cli.py lp-reporting capital-call \
  --amount 500000 \
  --fund "Fund X" \
  --due-date 2026-03-15

# Auto-generate:
- Notice letter
- Wire instructions
- Deadline reminder
- Track responses
```

**Why:** I send 20-30 capital call notices per year. Should be automated.

---

## 7. Deal Pipeline & Sourcing 🔍

**What I Need:**

### Manager Sourcing
```bash
# How am I finding new managers?
./scripts/newco_cli.py pipeline source

# Track source of each manager:
- VC partner referral (best source - warm intro)
- Platform referral (Hamilton Lane, etc.)
- Inbound (manager reaches out)
- Conference (met at event)
- Research (Pitchbook, Crunchbase)
```

**Why:** Need to know which sourcing channels work best.

### Referral Tracking
```bash
# Who is referring me the best managers?
./scripts/newco_cli.py pipeline referrals

# Show:
- Person who referred
- Managers referred
- Conversion rate (sourced → committed)
- Thank you notes sent
```

**Why:** I need to cultivate my best referral sources.

### Market Intelligence
```bash
# What's happening in VC manager landscape?
./scripts/newco_cli.py market intelligence

# Track:
- New funds raising (Pitchbook data)
- Manager departures (spin-outs from big firms)
- Hot sectors (AI, climate, bio)
- Fundraising environment
- LP sentiment
```

**Why:** I need to stay ahead of market trends.

---

## 8. Financial Planning & Modeling 💰

**What I Need:**

### Cash Flow Modeling
```bash
# Model next 3 years
./scripts/newco_cli.py finance model --years 3

# Project:
- Capital calls by quarter
- Distributions received
- Management fees paid
- Operating expenses
- Net cash position
- Need for stock issuance
```

**Why:** I need to know if/when I need to raise more capital.

### Scenario Analysis
```bash
# What if scenarios
./scripts/newco_cli.py finance scenario

# Scenarios:
- Base case (expected)
- Bull case (strong returns, high distributions)
- Bear case (write-downs, slow distributions)
- Stress case (major fund failures)
```

**Why:** Board wants to see scenario planning.

### Budget vs Actual
```bash
# Are we on budget?
./scripts/newco_cli.py finance budget-variance

# Compare:
- Planned deployment vs actual
- Planned expenses vs actual
- Revenue (management fees) vs forecast
- Public market value vs target
```

**Why:** CFO reports this to me monthly. I report to board quarterly.

---

## 9. Team & Talent Management 👥

**What I Need:**

### Deal Team Tracking
```bash
# Who's working on what?
./scripts/newco_cli.py team workload

# Show:
- Person
- Active due diligences
- IC memos in progress
- Manager relationships owned
- Utilization %
```

**Why:** Need to balance workload across team.

### IC Voting History
```bash
# Track IC member voting patterns
./scripts/newco_cli.py team ic-votes

# Show:
- IC member
- Yes votes
- No votes
- Abstentions
- Hit rate (% of Yes votes that performed well)
```

**Why:** Helps me understand who has best judgment.

### Professional Development
```bash
# Track team learning
./scripts/newco_cli.py team development

# For each team member:
- Funds managed
- Due diligences completed
- IC presentations
- Manager relationships
- Training completed
```

**Why:** I'm building a team. Need to track growth.

---

## 10. Competitive Intelligence 🔭

**What I Need:**

### Competitor Tracking
```bash
# What are other fund-of-funds doing?
./scripts/newco_cli.py competitive track

# Track competitors:
- Other public VC vehicles
- Private VC fund-of-funds
- Their fund commitments (public info)
- Their performance (if disclosed)
- Their LP base
- Their fee structures
```

**Why:** Need to know who I'm competing with for managers and LPs.

### Manager Market Map
```bash
# Who are the best emerging managers?
./scripts/newco_cli.py competitive managers

# Track:
- All sub-$250M VC funds
- Performance data
- Who's investing in them
- Availability (are they oversubscribed?)
```

**Why:** Manager selection is my core value-add. Need comprehensive data.

---

## Bottom Line

**What I Really Need:**

1. **Portfolio Management** - Track my 15-20 fund investments
2. **Manager CRM** - Separate from LP CRM
3. **Performance Reporting** - Automated board/LP materials
4. **Risk Dashboard** - Real-time concentration monitoring
5. **Cash Flow Modeling** - Know when I need capital
6. **IC Management** - Track decisions and voting
7. **Deal Pipeline** - Manager sourcing and DD tracking
8. **Competitive Intel** - Know the market

**The Current System is Great For:**
- ✅ Raising capital (GTM)
- ✅ Building relationships (Network Analysis)
- ✅ Public markets (Stock tracking)

**But I Also Need To:**
- ❌ Manage the portfolio (15-20 funds)
- ❌ Select managers (due diligence workflow)
- ❌ Report to board (automated materials)
- ❌ Manage team (workload, development)
- ❌ Plan finances (cash flow, budgets)

---

## Priority List

**Must Have (Need This Week):**
1. Portfolio tracking (fund investments)
2. Capital call forecasting
3. Manager CRM
4. Performance dashboard

**Should Have (Need This Month):**
5. Board deck automation
6. LP letter generation
7. Risk dashboard
8. Due diligence tracking

**Nice to Have (Need This Quarter):**
9. Financial modeling
10. Competitive intelligence
11. Team management
12. Market intelligence

---

*Ken Wallace, CEO*
*NEWCO - Publicly Traded VC Fund-of-Funds*

P.S. - The network analysis stuff is gold. Knowing Bob Burlinson can open doors to 50+ LPs? That's exactly the kind of leverage insight I need. But I also need to run the portfolio day-to-day!

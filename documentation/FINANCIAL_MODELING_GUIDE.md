# Financial Modeling Guide

## Overview

The financial modeling system projects cash flows, analyzes scenarios, and helps plan fundraising for NEWCO. This is critical for strategic planning and ensuring adequate liquidity.

**Key Features:**
1. **3-5 Year Cash Flow Projections** - Model capital calls, distributions, expenses
2. **Scenario Analysis** - Bull, base, bear cases
3. **Budget vs Actual Tracking** - Monitor spending against budget
4. **Fundraising Analysis** - Know when to raise capital
5. **What-If Analysis** - Test parameter sensitivity

---

## Quick Start

### Run Scenario Analysis

```bash
./scripts/newco_cli.py finance scenarios --years 3
```

Shows bull/base/bear projections side-by-side for 3 years.

**Use Case:** Board presentation, strategic planning, fundraising materials

### Check Cash Runway

```bash
./scripts/newco_cli.py finance fundraising 5000000 --runway 24
```

Analyzes whether $5M cash provides 24 months of runway.

**Output:**
- Current runway in months
- Recommendation (URGENT/SOON/HEALTHY)
- Target raise amount
- Monthly cash flow forecast

---

## Scenario Analysis

### What It Does

Models three scenarios over 3-5 years:

**Bull Case** (🟢)
- NAVs grow 50%
- Distributions 30% faster
- 4 new commitments per year

**Base Case** (🟡)
- NAVs stable
- Distributions on schedule
- 3 new commitments per year

**Bear Case** (🔴)
- NAVs down 30%
- Distributions 30% slower
- 2 new commitments per year

### Command

```bash
# 3-year projection (default)
./scripts/newco_cli.py finance scenarios

# 5-year projection
./scripts/newco_cli.py finance scenarios --years 5
```

### Example Output

```
SCENARIO ANALYSIS - CASH FLOW PROJECTIONS

YEAR 2026
Metric                         Bull                 Base                 Bear
Capital Calls                  $3,290,000          $3,290,000          $3,290,000
Distributions                  $1,004,250          $772,500            $540,750
New Commitments                $12,000,000         $9,000,000          $6,000,000
Management Fees                $356,250            $318,750            $281,250
Operating Expenses             $750,000            $750,000            $750,000
Net Cash Flow                  -$15,392,000        -$12,586,250        -$9,780,500
Estimated NAV                  $8,770,000          $8,770,000          $8,770,000
```

### Key Metrics Explained

**Capital Calls**
- Cash required for existing fund commitments
- Follows industry deployment curves:
  - Year 1: 30% of commitment
  - Year 2: 36% of commitment
  - Year 3: 24% of commitment
  - Year 4+: 10% of commitment

**Distributions**
- Cash returned from funds
- Starts in year 3-4 (typical VC timeline)
- Accelerates as funds mature

**New Commitments**
- Capital deployed to new funds
- Varies by scenario (2-4 per year)
- Assumes $3M average commitment

**Management Fees**
- 1.25% on committed capital (or NAV)
- Standard for fund-of-funds

**Operating Expenses**
- Base: $500K + $50K per fund
- Grows 3% annually with inflation

**Net Cash Flow**
- Total cash in minus cash out
- Negative early (J-curve effect)
- Positive later as distributions exceed calls

---

## Cash Flow Projections

### Single Scenario Projection

```bash
# Base case (default)
./scripts/newco_cli.py finance project --years 3

# Bear case
./scripts/newco_cli.py finance project --years 3 --scenario bear

# Bull case
./scripts/newco_cli.py finance project --years 5 --scenario bull
```

**Use Case:** Detailed view of a single scenario, board materials, strategic planning

### Understanding the J-Curve

**Years 0-3:** Negative cash flow
- Capital calls > Distributions
- Funds still investing, not exiting
- Need cash reserves or credit facility

**Years 4-7:** Improving cash flow
- Distributions increasing
- Capital calls decreasing
- Approaching break-even

**Years 8+:** Positive cash flow
- Distributions > Capital calls
- Mature portfolio
- Self-sustaining

---

## Fundraising Analysis

### When to Raise Capital

```bash
./scripts/newco_cli.py finance fundraising <current_cash> --runway <months>
```

**Parameters:**
- `current_cash`: Current cash position
- `runway`: Desired months of cash (default: 24)

### Example Analysis

```bash
./scripts/newco_cli.py finance fundraising 5000000 --runway 24
```

**Output:**
```
💰 Current Cash Position: $5,000,000
📅 Current Runway: 4 months
🎯 Target Runway: 24 months

📊 Recommendation:
   SOON: Only 4 months of runway. Begin fundraising process.

💵 Target Raise Amount: $22,594,500
```

### Recommendations Explained

**URGENT (< 6 months runway)**
- Negative or critically low cash
- Raise capital immediately
- Risk of missing capital calls

**SOON (6-18 months runway)**
- Below target runway
- Begin fundraising process (3-6 month process)
- Target raise: 24-36 months of runway

**HEALTHY (> 18 months runway)**
- Adequate liquidity
- Monitor quarterly
- No immediate action needed

### Fundraising Timeline

Typical fundraising process takes **3-6 months:**

**Month 1-2:** Preparation
- Update materials
- Refine strategy
- Identify target investors

**Month 3-4:** Outreach
- Investor meetings
- Due diligence
- Term sheet negotiations

**Month 5-6:** Closing
- Legal documentation
- Regulatory approvals
- Capital deployment

**Recommendation:** Start fundraising when runway = 18 months to close before runway = 12 months.

---

## Budget vs Actual Tracking

### Set Annual Budget

```bash
./scripts/newco_cli.py finance add-budget 2026 "Salaries & Benefits" 1200000
./scripts/newco_cli.py finance add-budget 2026 "Office & Facilities" 150000
./scripts/newco_cli.py finance add-budget 2026 "Travel & Entertainment" 100000
./scripts/newco_cli.py finance add-budget 2026 "Professional Services" 200000
./scripts/newco_cli.py finance add-budget 2026 "Due Diligence Costs" 300000
```

### Log Actual Spending

```bash
# Monthly actuals
./scripts/newco_cli.py finance add-actual 1 2026 "Salaries & Benefits" 100000
./scripts/newco_cli.py finance add-actual 1 2026 "Travel & Entertainment" 7500
./scripts/newco_cli.py finance add-actual 1 2026 "Due Diligence Costs" 20000
```

### Analyze Variance

```bash
./scripts/newco_cli.py finance variance
./scripts/newco_cli.py finance variance --year 2025
```

**Output:**
```
BUDGET VARIANCE ANALYSIS - 2026

Category                  Budget          Actual          Variance        %          Status
Salaries & Benefits       $1,200,000     $202,000        -$998,000      -83.2%     ⚠️ Under
Travel & Entertainment    $100,000       $22,500         -$77,500       -77.5%     ⚠️ Under
Due Diligence Costs       $300,000       $65,000         -$235,000      -78.3%     ⚠️ Under
```

**Variance Flags:**
- ⚠️  **Over/Under > 10%** - Investigate
- ✓ **Within 10%** - On track

### Common Budget Categories

**Personnel:**
- Salaries & Benefits
- Bonuses & Incentives
- Recruiting & Onboarding

**Operating:**
- Office & Facilities
- Technology & Software
- Professional Services (legal, accounting, audit)

**Investment Activities:**
- Due Diligence Costs
- Travel & Entertainment
- Market Research

**Governance:**
- Board & Governance
- Insurance & Legal
- Compliance & Regulatory

---

## Modeling Assumptions

All projections use assumptions stored in `/Users/rufio/NEWCO/models/model_assumptions.json`.

### Key Assumptions

**Deployment Rates:**
```json
{
  "year_1": 0.30,  // 30% of commitment in year 1
  "year_2": 0.36,  // 36% in year 2
  "year_3": 0.24,  // 24% in year 3
  "year_4_plus": 0.10  // 10% in year 4+
}
```

**Distribution Timing:**
```json
{
  "years_to_first_distribution": 3,  // Distributions start year 3
  "distribution_acceleration": 0.15   // 15% increase per year
}
```

**Management Fees:**
```json
{
  "fee_rate": 0.0125,  // 1.25% annual fee
  "on_commitment": true  // Fee on commitment vs NAV
}
```

**Operating Expenses:**
```json
{
  "annual_base": 500000,    // $500K base
  "per_fund": 50000,        // $50K per fund
  "inflation": 0.03         // 3% annual increase
}
```

**Scenario Parameters:**
```json
{
  "bull": {
    "multiple_markup": 1.5,              // NAVs grow 50%
    "distribution_acceleration": 1.3,    // 30% faster
    "new_commitments_per_year": 4
  },
  "base": {
    "multiple_markup": 1.0,              // NAVs stable
    "distribution_acceleration": 1.0,    // On schedule
    "new_commitments_per_year": 3
  },
  "bear": {
    "multiple_markup": 0.7,              // 30% mark-down
    "distribution_acceleration": 0.7,    // 30% slower
    "new_commitments_per_year": 2
  }
}
```

### Customizing Assumptions

Edit `/Users/rufio/NEWCO/models/model_assumptions.json` to change assumptions:

```json
{
  "deployment_rates": {
    "year_1": 0.25,  // Change to 25% in year 1
    "year_2": 0.35
  },
  "management_fees": {
    "fee_rate": 0.015,  // Change to 1.5% fee
    "on_commitment": false  // Calculate on NAV instead
  }
}
```

Assumptions apply to all future projections until changed.

---

## Use Cases

### 1. Board Strategic Planning

**Scenario:**
Board asks "What if we slow down deployment?"

**Analysis:**
```bash
# Current plan: 3 new funds per year
./scripts/newco_cli.py finance scenarios --years 5

# Edit assumptions: 2 new funds per year
# Re-run scenarios
./scripts/newco_cli.py finance scenarios --years 5

# Compare outcomes
```

### 2. Fundraising Materials

**Scenario:**
Preparing to raise $20M from new LPs

**Analysis:**
```bash
# Show base case projection
./scripts/newco_cli.py finance project --years 3 --scenario base

# Analyze current runway
./scripts/newco_cli.py finance fundraising 5000000

# Include in pitch deck:
# - "We need $22M to maintain 24-month runway"
# - "Base case shows positive NAV growth"
# - "Even in bear case, portfolio performs well"
```

### 3. Monthly CFO Review

**Workflow:**
```bash
# 1. Check budget variance
./scripts/newco_cli.py finance variance

# 2. Log current month actuals
./scripts/newco_cli.py finance add-actual 2 2026 "Salaries" 105000
./scripts/newco_cli.py finance add-actual 2 2026 "Travel" 12000

# 3. Update assumptions if needed
# Edit model_assumptions.json

# 4. Re-run projections
./scripts/newco_cli.py finance scenarios

# 5. Report to CEO
# - Budget variances > 10%
# - Updated cash flow projections
# - Fundraising recommendations
```

### 4. Stress Testing

**Scenario:**
"What if our funds mark down 40%?"

**Analysis:**
```bash
# Edit assumptions: bear case multiple_markup = 0.6
# Run bear scenario
./scripts/newco_cli.py finance project --years 3 --scenario bear

# Results:
# - How much does NAV drop?
# - Does cash flow turn positive?
# - When do we need to raise?
```

---

## Advanced: What-If Analysis

### Testing Parameter Sensitivity

The system can test how changes to specific parameters affect outcomes.

**Example: New Commitments Per Year**

What if we commit to 2, 3, 4, or 5 new funds per year?

```python
from financial_modeling import FinancialModeler

modeler = FinancialModeler()

# Test different commitment rates
results = modeler.what_if_analysis(
    parameter='scenarios.base.new_commitments_per_year',
    values=[2, 3, 4, 5]
)

for result in results:
    print(f"Commitments/year: {result['parameter_value']}")
    print(f"  Net Cash Flow: ${result['net_cashflow']:,.0f}")
    print(f"  Ending NAV: ${result['ending_nav']:,.0f}")
```

**Example: Fee Rate**

What if fees are 1.0%, 1.25%, or 1.5%?

```python
results = modeler.what_if_analysis(
    parameter='management_fees.fee_rate',
    values=[0.010, 0.0125, 0.015]
)
```

---

## Integration with Other Systems

### Portfolio Data

Projections use real portfolio data:
- Current fund commitments
- Vintage years (for deployment curves)
- Current NAVs (for distribution estimates)

### Risk Management

Financial models inform risk monitoring:
- Liquidity risk (runway analysis)
- Concentration risk (new commitment sizing)
- Vintage risk (deployment timing)

### Board Reporting

Scenario analysis can be included in board decks:
```bash
# Generate scenarios
./scripts/newco_cli.py finance scenarios > reports/board/scenarios_Q1_2026.txt

# Include in board deck
# Shows bull/base/bear outcomes
```

---

## Best Practices

### For CEOs

1. **Review scenarios quarterly** - Update assumptions based on actual results
2. **Monitor runway monthly** - Don't get surprised by cash needs
3. **Use in fundraising** - Projections are key part of investor materials
4. **Stress test regularly** - "What if things go wrong?"

### For CFOs

1. **Update actuals monthly** - Keep budget variance current
2. **Revise assumptions quarterly** - As actual deployment rates become clear
3. **Model sensitivity** - Test key parameter changes
4. **Maintain 24+ month runway** - Plan fundraising well in advance

### For Board Members

1. **Request scenario analysis** - Understand range of outcomes
2. **Review budget variances** - Are we spending as planned?
3. **Challenge assumptions** - Are deployment rates realistic?
4. **Assess liquidity** - Do we have adequate runway?

---

## Troubleshooting

### "Negative Cash Flow Every Year"

**Issue:** Model shows continuous negative cash flow

**Explanation:** This is normal for growing fund-of-funds
- J-curve effect: Capital calls precede distributions
- New commitments require cash
- Distributions accelerate in years 5-10

**Solution:** Not an error. Plan for:
- Credit facility
- Regular fundraising cadence
- Maintaining 24+ month cash runway

### "Distributions Seem Low"

**Issue:** Distribution projections lower than expected

**Check:**
1. Funds old enough to distribute? (Year 3+ typically)
2. Distribution assumptions realistic?
3. Fund NAVs growing or flat?

**Adjust:** Edit `model_assumptions.json`:
```json
{
  "distribution_timing": {
    "years_to_first_distribution": 2,  // Earlier distributions
    "distribution_acceleration": 0.20  // Faster acceleration
  }
}
```

### "Budget Variance Shows Everything Under"

**Issue:** All categories show "Under Budget"

**Explanation:** Only 2 months of actuals vs annual budget

**Solution:** Normal. After 6 months, variances become meaningful. After 12 months, close to actual.

### "Fundraising Says URGENT But We Have Cash"

**Issue:** Current cash seems adequate but model says urgent

**Check:**
1. How much are monthly capital calls?
2. Are new commitments depleting cash fast?
3. Is runway calculation including all cash needs?

**Common Cause:** Large unfunded commitments coming due

---

## Example Workflows

### Quarterly Financial Review

```bash
# Week 1: Update actuals
./scripts/newco_cli.py finance add-actual 3 2026 "Salaries" 103000
# ... (all categories)

# Week 2: Check variances
./scripts/newco_cli.py finance variance

# Week 3: Update projections
./scripts/newco_cli.py finance scenarios --years 3

# Week 4: Board presentation
./scripts/newco_cli.py board deck
# (includes financial projections)
```

### Pre-Fundraise Planning

```bash
# 6 months before expected fundraise:

# 1. Current state
./scripts/newco_cli.py finance fundraising 8000000 --runway 24

# 2. Scenario analysis
./scripts/newco_cli.py finance scenarios --years 3

# 3. Determine raise amount
# Based on:
# - Current runway
# - 3-year projections
# - Desired 24-month post-raise runway

# 4. Create investor materials
# Include:
# - Base case projection
# - Scenario analysis (bull/base/bear)
# - Use of proceeds
```

### Annual Budget Process

```bash
# October: Set next year budget
./scripts/newco_cli.py finance add-budget 2027 "Salaries" 1500000
./scripts/newco_cli.py finance add-budget 2027 "Travel" 120000
# ... (all categories)

# Monthly: Log actuals
./scripts/newco_cli.py finance add-actual 1 2027 "Salaries" 125000

# Quarterly: Review variances
./scripts/newco_cli.py finance variance

# Adjust budget mid-year if needed
# Add updated budget lines for H2
```

---

## Command Reference

```bash
# Scenario analysis
./scripts/newco_cli.py finance scenarios [--years N]

# Single scenario projection
./scripts/newco_cli.py finance project [--years N] [--scenario bull|base|bear]

# Budget variance
./scripts/newco_cli.py finance variance [--year YYYY]

# Fundraising analysis
./scripts/newco_cli.py finance fundraising <cash> [--runway N]

# Budget management
./scripts/newco_cli.py finance add-budget <year> <category> <amount>
./scripts/newco_cli.py finance add-actual <month> <year> <category> <amount>
```

---

## Data Files

**Model Assumptions:**
- `/Users/rufio/NEWCO/models/model_assumptions.json`

**Budget Data:**
- `/Users/rufio/NEWCO/data/annual_budget.csv`
- `/Users/rufio/NEWCO/data/monthly_actuals.csv`

---

**Questions?**

For financial modeling assistance:
- **Strategic Planning:** Contact CEO
- **Budget Management:** Contact CFO
- **Technical Issues:** Check this guide or system logs

---

*Last Updated: February 2026*
*Version: 1.0*

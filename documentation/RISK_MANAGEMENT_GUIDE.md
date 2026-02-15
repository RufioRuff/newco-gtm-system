# Risk Management Guide

## Overview

The risk management system provides real-time monitoring of portfolio risks and governance compliance. This is critical for a publicly traded VC fund-of-funds where concentration risk = career risk for the CEO.

**Key Risk Areas:**
1. **Concentration Risk** - Over-exposure to single fund/sector/vintage
2. **Vintage Year Risk** - Exposure to bubble or correction years
3. **Liquidity Risk** - Ability to meet capital calls
4. **Correlation Risk** - Portfolio company overlap between funds

## Quick Start

### View Comprehensive Risk Dashboard

```bash
./scripts/newco_cli.py risk dashboard
```

This shows all risk metrics in one view:
- Overall risk score (0-100)
- Concentration violations
- Vintage year exposure
- Liquidity forecast
- Correlation status

**When to use:** Weekly review, before board meetings, after adding new funds

### Check Governance Compliance

```bash
./scripts/newco_cli.py risk governance
```

Verifies compliance with investment policy:
- ✓ Minimum 10 fund investments
- ✓ No single fund > 15%
- ✓ No vintage year > 30%
- ✓ No sector > 40%

**When to use:** Monthly, before IC meetings, for board reporting

## Risk Metrics Explained

### 1. Concentration Risk

**What it checks:**
- Fund count (minimum 10)
- Single fund max (15% of total commitment)
- Top 3 funds max (40% of total)
- Vintage year max (30% per year)
- Sector max (40% per sector)

**Command:**
```bash
./scripts/newco_cli.py risk concentration
```

**Example Output:**
```
🎯 CONCENTRATION RISK CHECK
Status: VIOLATION
Fund Count: 5

⚠️  VIOLATIONS (3)
  • Only 5 funds (minimum 10)
  • Gamma Growth Fund I: 30.3% (max 15%)
  • Vintage 2024: 48.5% (max 30%)
```

**What to do:**
- **Fund count < 10**: Add more funds to diversify
- **Single fund > 15%**: Avoid large commitments or increase total portfolio size
- **Vintage > 30%**: Spread commitments across multiple vintage years
- **Sector > 40%**: Diversify across sectors

**Why it matters:** Over-concentration increases downside risk. If your largest fund fails, you don't want it to be 30% of your portfolio.

### 2. Vintage Year Risk

**What it analyzes:**
- Bubble era exposure (2020-2021): High valuation years = high risk
- Correction era exposure (2023-2024): Lower valuations = opportunity
- Vintage diversification: More years = better

**Command:**
```bash
./scripts/newco_cli.py risk vintage
```

**Example Output:**
```
📅 VINTAGE YEAR RISK ANALYSIS
Bubble Era Exposure (2020-2021): 0.0%
Correction Era Exposure (2023-2024): 87.9%
Vintage Diversification: 3 years

Vintage Breakdown:
  2023: 39.4% (2 funds) - Risk: MEDIUM
  2024: 48.5% (2 funds) - Risk: MEDIUM
  2025: 12.1% (1 funds) - Risk: LOW
```

**What to do:**
- **Bubble exposure > 30%**: Expect mark-downs, monitor closely
- **Diversification < 3 years**: Add funds from other vintages
- **Diversification ≥ 4 years**: ✓ Good diversification

**Why it matters:** Vintage year is the #1 driver of VC returns. 2021 vintage funds are down 30-50% industry-wide. 2023-2024 vintages may outperform due to lower entry prices.

### 3. Liquidity Risk

**What it checks:**
- Unfunded commitments
- 12-month capital call forecast
- Recommended cash reserve (25% of forecast)

**Command:**
```bash
./scripts/newco_cli.py risk liquidity
```

**Example Output:**
```
💰 LIQUIDITY RISK CHECK
Unfunded Commitments: $9,600,000
12-Month Forecast: $4,950,000
Required Cash Reserve: $1,237,500

Recommendations:
  • Maintain $1,237,500 cash reserve
  • Monitor fund deployment pace
  • Review credit facility if needed
```

**What to do:**
- Ensure cash reserve > 25% of 12-month forecast
- Monitor deployment pace (funds calling faster than expected?)
- Have credit facility as backup

**Why it matters:** Missing a capital call = default = career-ending event. Always maintain adequate reserves.

### 4. Correlation Risk

**What it tracks:**
- Portfolio company overlap between funds
- High overlap pairs (>30% shared companies)

**Command:**
```bash
./scripts/newco_cli.py risk correlation
```

**Example Output:**
```
🔗 CORRELATION RISK ANALYSIS
Status: LOW
Tracked Correlations: 5
High Overlap Pairs: 1

Recommendations:
  • Track portfolio company overlap across funds
  • Avoid funds with >30% company overlap
  • Consider syndicate patterns in manager selection
```

**What to do:**
- Track which funds co-invest frequently
- Avoid selecting multiple funds that always syndicate together
- If overlap > 30%, you're not truly diversified

**Why it matters:** If two funds have 50% portfolio company overlap, they're highly correlated. When one marks down, the other likely will too.

## Risk Scoring System

**Overall Risk Score (0-100):**
- **0-20**: 🟢 LOW - All systems go
- **21-50**: 🟡 MEDIUM - Monitor closely
- **51-100**: 🔴 HIGH - Action required

**Scoring Formula:**
```
Risk Score =
  + 40 points if concentration violations
  + 20 points if concentration warnings
  + 30 points if liquidity alert
  + 20 points if bubble exposure > 30%
  + 10 points if high correlation
```

## Investment Policy Limits

These limits are set in the investment policy (IPS):

| Policy Limit | Threshold | Rationale |
|-------------|-----------|-----------|
| Minimum fund count | 10 funds | Diversification |
| Single fund max | 15% | Concentration risk |
| Top 3 funds max | 40% | Concentration risk |
| Vintage year max | 30% | Vintage risk |
| Sector max | 40% | Sector risk |
| Cash reserve min | 10% of NAV | Liquidity |

**Changing Limits:**

If your board approves different limits, edit `/Users/rufio/NEWCO/scripts/risk_management.py`:

```python
LIMITS = {
    'single_fund_max': 0.15,      # 15% max in any single fund
    'vintage_year_max': 0.30,     # 30% max in any vintage year
    'sector_max': 0.40,           # 40% max in any sector
    'top_3_funds_max': 0.40,      # 40% max in top 3 funds
    'cash_reserve_min': 0.10,     # 10% min cash reserves
    'min_fund_count': 10          # Minimum 10 fund investments
}
```

## Workflows

### Weekly Risk Review

```bash
# 1. Check overall risk dashboard
./scripts/newco_cli.py risk dashboard

# 2. If violations exist, drill down
./scripts/newco_cli.py risk concentration
./scripts/newco_cli.py risk vintage
./scripts/newco_cli.py risk liquidity

# 3. Log any risk events
# (manual entry in data/risk_events.csv for now)
```

**Time required:** 10 minutes

### Before Board Meeting

```bash
# Generate governance compliance report
./scripts/newco_cli.py risk governance > reports/governance_$(date +%Y%m%d).txt

# Include in board deck
# Risk section should show:
# - Overall risk score
# - Any policy violations
# - Mitigation actions taken
```

**Time required:** 5 minutes

### Before IC Meeting

```bash
# Check if new fund would create violations
# Example: Adding $3M to Fintech sector

# 1. Check current sector exposure
./scripts/newco_cli.py risk concentration | grep "Sector Exposure" -A 10

# 2. Calculate: Current + New = ?
# If Fintech is 30% and new fund is 15%, total would be 45% (over 40% limit)

# 3. Flag for IC discussion
```

**Time required:** 5 minutes

### After Adding New Fund

```bash
# 1. Add fund to portfolio
./scripts/newco_cli.py portfolio add-fund --name "New Fund" ...

# 2. Immediately check risk impact
./scripts/newco_cli.py risk dashboard

# 3. Document any new violations
```

**Time required:** 5 minutes

## Tracking Risk Events

Risk events are logged in `/Users/rufio/NEWCO/data/risk_events.csv`:

**Event Types:**
- `concentration_breach` - Exceeded concentration limit
- `liquidity_shortage` - Insufficient cash for capital call
- `correlation_high` - Two funds with >50% overlap discovered
- `vintage_concentration` - Single vintage over 30%

**Severity Levels:**
- `Low` - Minor issue, monitoring only
- `Medium` - Requires action within 30 days
- `High` - Requires immediate action
- `Critical` - Board-level escalation

**Example CSV Entry:**
```csv
event_id,date,risk_type,severity,description,status,resolved_date,notes
RE0001,2026-02-01,concentration_breach,High,Gamma Growth Fund exceeds 15% limit,Open,,IC approved overweight position
```

## Integration with Other Systems

### Portfolio Management
```bash
# Risk dashboard uses portfolio data
# Any changes to portfolio automatically reflected in risk metrics
./scripts/newco_cli.py portfolio add-fund ...
./scripts/newco_cli.py risk dashboard  # Shows updated risk
```

### Board Reporting
```bash
# Export governance report for board deck
./scripts/newco_cli.py risk governance > reports/board/governance_Q1_2026.txt
```

### IC Process
```bash
# Before IC meeting, generate risk summary
./scripts/newco_cli.py risk dashboard > reports/ic/risk_summary_$(date +%Y%m%d).txt
```

## Advanced: Custom Risk Metrics

### Tracking Fund Correlation

To track portfolio company overlap between funds:

1. Obtain portfolio company lists from each fund manager
2. Add to `/Users/rufio/NEWCO/data/fund_correlations.csv`:

```csv
fund_id_1,fund_id_2,shared_companies,overlap_score,notes
F001,F003,5,0.35,"Both invest heavily in AI/ML"
```

3. Run correlation analysis:
```bash
./scripts/newco_cli.py risk correlation
```

### Monitoring Specific Sectors

To get sector-specific risk breakdown:

```bash
# Filter portfolio by sector, then check concentration
./scripts/newco_cli.py portfolio show | grep "Sector: Fintech" -A 5
./scripts/newco_cli.py risk concentration
```

## Troubleshooting

### "Fund Count: 0"

**Issue:** Risk dashboard shows no funds

**Solution:**
```bash
# Check if portfolio funds exist
./scripts/newco_cli.py portfolio show

# If empty, load demo data
./scripts/demo_portfolio.py
```

### "KeyError: 'amount'"

**Issue:** Liquidity forecast failing

**Solution:** Check that portfolio funds have proper commitment dates:
```bash
grep "commitment_date" data/portfolio_funds.csv
```

All funds need `commitment_date` field for deployment curve calculation.

### Risk Score Always 0

**Issue:** Risk score shows 0 even with violations

**Solution:** Check that limits are defined correctly in `risk_management.py`. Restart CLI after any changes.

## Best Practices

### For CEOs

1. **Review weekly** - 10 minutes every Monday
2. **Before IC meetings** - Check if new fund creates violations
3. **Before board meetings** - Generate governance report
4. **After capital calls** - Check liquidity forecast

### For Analysts

1. **Track correlations** - Maintain fund_correlations.csv
2. **Log risk events** - Document any violations
3. **Monitor trends** - Is risk score increasing?

### For Board Members

1. **Request governance report** - Quarterly at minimum
2. **Review violations** - Any breaches of investment policy?
3. **Assess mitigation** - What actions are being taken?

## Reporting Templates

### Weekly Email to CEO

```
Risk Dashboard Summary - Week of [DATE]

Overall Risk: [LOW/MEDIUM/HIGH] (Score: X/100)

Status:
✓ Concentration: Compliant
⚠️  Vintage Risk: 2024 vintage at 48% (over 30% limit)
✓ Liquidity: $1.2M reserve (adequate)
✓ Correlation: Low overlap

Action Items:
1. Add 2023 or 2025 vintage funds to reduce 2024 concentration
2. Maintain $1.2M+ cash reserve for Q1 capital calls
```

### Quarterly Board Report

```
Governance & Risk Report - Q1 2026

Investment Policy Compliance:
✓ PASS: Fund count (15 funds, minimum 10)
✓ PASS: Single fund limit (largest 12%, limit 15%)
⚠️  FAIL: Vintage year (2023 at 35%, limit 30%)
✓ PASS: Sector limits (all < 40%)

Risk Score: 22/100 (LOW-MEDIUM)

Mitigation Actions:
- Added 2024 vintage fund to reduce 2023 concentration
- Targeting 2025 vintages for next 2 commitments
```

## API for External Tools

The risk module can be imported directly:

```python
from risk_management import RiskManager

rm = RiskManager()
dashboard = rm.get_risk_dashboard()

print(f"Risk Score: {dashboard['risk_score']}")
print(f"Violations: {len(dashboard['concentration']['violations'])}")
```

## Future Enhancements

Planned features (not yet implemented):

1. **Scenario Analysis** - "What if we add $5M to Fintech?"
2. **Historical Risk Tracking** - Risk score over time
3. **Automated Alerts** - Email when violations occur
4. **Stress Testing** - Model portfolio in market downturn
5. **Peer Benchmarking** - Compare to other fund-of-funds

---

**Questions?**

Risk management is critical for governance. If you have questions about:
- Interpreting risk metrics
- Setting appropriate limits
- Board reporting
- Escalation procedures

Contact: Ken Wallace, CEO (ken@newco.com)

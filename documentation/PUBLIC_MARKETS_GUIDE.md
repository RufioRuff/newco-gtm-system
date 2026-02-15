# Public Markets Guide
## For Publicly Traded VC Fund-of-Funds

## Overview

NEWCO is structured as a **publicly traded VC fund-of-funds** - a unique vehicle that combines:
- **Public market liquidity** (stock trades on exchange)
- **Private VC exposure** (invests in venture funds)

This guide covers the public markets tools, regulatory requirements, and investor relations for this structure.

---

## Table of Contents

1. [Understanding the Structure](#understanding-the-structure)
2. [Key Metrics](#key-metrics)
3. [Regulatory Requirements](#regulatory-requirements)
4. [Using the Tools](#using-the-tools)
5. [Investor Relations](#investor-relations)
6. [Best Practices](#best-practices)

---

## Understanding the Structure

### What is a Publicly Traded VC Fund-of-Funds?

**Structure:**
- Public company listed on stock exchange (e.g., NYSE, NASDAQ)
- Invests in portfolio of private venture capital funds
- Shareholders buy/sell stock like any public company
- BUT: Underlying assets are illiquid VC fund stakes

**Examples of Similar Structures:**
- **BDCs (Business Development Companies)** - Hercules Capital (HTGC), TriplePoint (TPVG)
- **Permanent Capital Vehicles** - Pershing Square Holdings
- **Listed PE Funds** - 3i Group (LSE), Partners Group
- **Interval Funds** - Some with quarterly liquidity

### Key Advantages

**For Investors:**
- ✅ Liquidity - Can sell stock anytime (vs 10-year lockup)
- ✅ Diversification - Exposure to 15-20 VC funds
- ✅ Transparent pricing - Daily stock price, quarterly NAV
- ✅ Lower minimums - $100s vs $millions for direct VC
- ✅ Regulatory oversight - SEC reporting, public audits

**For the Fund:**
- ✅ Permanent capital - No redemption pressure
- ✅ Retail access - Broader investor base
- ✅ Public profile - Credibility, marketing
- ✅ Liquidity for LPs - Exit mechanism

### Key Challenges

**Structural:**
- ❌ Premium/Discount to NAV - Stock may trade below NAV
- ❌ Valuation lag - Private fund NAVs lag 1-3 months
- ❌ Complexity - Public + private regulations
- ❌ Trading blackouts - Restricted insider trading periods
- ❌ Disclosure burden - Quarterly reporting, compliance costs

**Market:**
- ❌ Limited comparables - Few public VC vehicles
- ❌ Liquidity concerns - May trade at discount
- ❌ Retail misunderstanding - Complex strategy
- ❌ Activist risk - Discount arbitrage activists

---

## Key Metrics

### 1. Premium/Discount to NAV

**Most important metric for publicly traded funds**

**Formula:**
```
Premium/Discount = (Stock Price - NAV per Share) / NAV per Share × 100
```

**Example:**
- Stock Price: $18.50
- NAV per Share: $20.00
- Premium/Discount: -7.5% (trading at discount)

**Interpretation:**
- **Premium (positive)**: Stock trades ABOVE NAV
  - Market is bullish on strategy
  - Strong demand, limited supply
  - Management has credibility

- **Discount (negative)**: Stock trades BELOW NAV
  - Market skepticism about strategy
  - Liquidity concerns
  - Uncertainty about fund valuations
  - Activist opportunity (buy at discount, push for catalyst)

**Typical Ranges:**
- CEFs (Closed-End Funds): -10% to +5%
- BDCs: -20% to +10%
- Interval Funds: -5% to +5%

**Check current premium/discount:**
```bash
./scripts/newco_cli.py public nav
```

### 2. Net Asset Value (NAV)

**Value of underlying assets per share**

**Calculation:**
```
NAV = (Total Assets - Total Liabilities) / Shares Outstanding

Total Assets:
  + Fund commitments (at fair value)
  + Cash and cash equivalents
  + Public securities (mark-to-market)

Total Liabilities:
  - Accrued expenses
  - Management fees payable
  - Other liabilities
```

**Valuation Challenges for VC Fund-of-Funds:**

1. **Private Fund Stakes (Level 3)**
   - Use fund manager reported NAVs
   - Typically lag 1-3 months
   - May need adjustments for material events

2. **Fair Value Hierarchy (ASC 820)**
   - **Level 1**: Quoted prices (public stocks) - Easy
   - **Level 2**: Observable inputs (recent transactions)
   - **Level 3**: Unobservable inputs (private funds) - 90%+ of portfolio

3. **Timing Issues**
   - Your NAV date: March 31
   - Fund A last NAV: February 28 (1 month lag)
   - Fund B last NAV: December 31 (3 month lag)

**Best Practices:**
- Disclose NAV methodology clearly
- Update NAVs when material events occur
- Cross-check valuations (portfolio company values)
- Conservative approach to fair value

### 3. Liquidity Metrics

**Average Daily Volume (ADV)**
- Number of shares traded per day
- Higher ADV = more liquid

**Average Daily Dollar Volume**
- ADV × Stock Price
- Institutional investors need $1M+ daily volume

**Bid-Ask Spread**
- Difference between buy and sell prices
- Tighter spread = more liquid

**Volatility**
- Price fluctuations
- Lower volatility typically means better liquidity

**Check liquidity:**
```bash
./scripts/newco_cli.py public liquidity
```

### 4. Investor Base Composition

**Categories:**
- **Institutional** (30-50%) - Mutual funds, pension funds
- **Retail** (20-40%) - Individual investors
- **Strategic** (5-15%) - LPs who also invest in fund
- **Insiders** (5-15%) - Management, board
- **Activists** (0-10%) - Hedge funds seeking catalyst

**Why It Matters:**
- Institutional heavy = more stable shareholder base
- Retail heavy = more volatility, less sophistication
- High insider ownership = good alignment
- Activist presence = potential for corporate action

**Check investor base:**
```bash
./scripts/newco_cli.py public investors
```

### 5. Comparable Analysis

**Peer Group:**
- Other public VC vehicles (rare)
- BDCs with VC focus
- Listed PE funds
- Permanent capital vehicles

**Benchmarks:**
- Peer average premium/discount
- Peer expense ratios
- Peer liquidity metrics

**Check comparables:**
```bash
./scripts/newco_cli.py public comparables
```

---

## Regulatory Requirements

### SEC Filing Requirements

**Quarterly (10-Q)**
- **Frequency**: 3x per year (Q1, Q2, Q3)
- **Deadline**: 45 days after quarter end
- **Content**:
  - Financial statements (unaudited)
  - MD&A (Management Discussion & Analysis)
  - Portfolio holdings summary
  - Risk factors update

**Annual (10-K)**
- **Frequency**: Once per year
- **Deadline**: 90 days after fiscal year end
- **Content**:
  - Audited financial statements
  - Complete portfolio disclosure
  - Full risk factor section
  - Compensation disclosure

**Material Events (8-K)**
- **Frequency**: As needed
- **Deadline**: 4 business days after event
- **Triggers**:
  - Major fund commitments
  - Management changes
  - Covenant violations
  - Material portfolio events

**Proxy Statement (DEF 14A)**
- **Frequency**: Annual
- **Deadline**: Before annual shareholder meeting
- **Content**:
  - Board elections
  - Executive compensation
  - Shareholder proposals
  - Related party transactions

**NAV Disclosure**
- **Frequency**: Weekly or Monthly
- **Deadline**: 5 business days
- **Content**:
  - NAV per share
  - Methodology
  - Significant changes

**Portfolio Holdings (Form 13F)**
- **Frequency**: Quarterly (if > $100M in public securities)
- **Deadline**: 45 days after quarter
- **Content**:
  - Public stock holdings
  - NOT required for private funds

**Check filing deadlines:**
```bash
./scripts/newco_cli.py compliance calendar
```

### Trading Restrictions

**Blackout Periods**

**Quarterly Blackout:**
- Starts: ~2 weeks before earnings
- Ends: 2 days after earnings call
- Affected: Officers, directors, 10%+ shareholders
- Purpose: Prevent trading on material non-public info

**Example Q1 Blackout:**
- Quarter End: March 31
- Blackout Start: May 1 (2 weeks before filing)
- 10-Q Due: May 15
- Earnings Call: May 16
- Blackout End: May 18

**Window Periods:**
- Typically 6-8 weeks per quarter when insiders CAN trade
- After earnings through ~2 weeks before next quarter end

**Ad-Hoc Blackouts:**
- Material events (acquisitions, major deals)
- "MNPI periods" - in possession of material non-public info

**Check blackout status:**
```bash
./scripts/newco_cli.py compliance blackout
```

### Section 16 (Insider Trading)

**Who is an "Insider":**
- Officers (CEO, CFO, CIO, etc.)
- Directors
- 10%+ shareholders

**Filing Requirements:**

**Form 3** - Initial Ownership
- When: Within 10 days of becoming insider
- What: Initial holdings

**Form 4** - Changes in Ownership
- When: Within 2 business days of trade
- What: Every buy, sell, option exercise

**Form 5** - Annual Statement
- When: Within 45 days of fiscal year end
- What: Small/exempt transactions for year

**Section 16(b) - Short-Swing Profit Rule**
- Any profit from buy AND sell within 6 months
- Must be returned to company
- Applies automatically
- Example: Buy in January, Sell in May = must return profit

**Check insider trading rules:**
```bash
./scripts/newco_cli.py compliance insider-rules
```

### Fair Value Requirements

**ASC 820 - Fair Value Measurement**

**Three-Level Hierarchy:**

**Level 1: Quoted Prices**
- Public stocks
- Easy: Daily mark-to-market
- High reliability

**Level 2: Observable Inputs**
- Recent secondary transactions
- Update when observable
- Medium-high reliability

**Level 3: Unobservable Inputs**
- **Private VC fund stakes (90%+ of your portfolio)**
- Based on fund manager reported NAVs
- Quarterly updates (with 1-3 month lag)
- Requires:
  - Reliance on fund manager valuations
  - Adjustments for material subsequent events
  - Liquidity discounts (if applicable)
  - Cross-checks with portfolio company valuations

**Disclosure Requirements:**
- Describe methodology in 10-K/10-Q
- Disclose Level 1/2/3 breakdown
- Explain significant changes
- Discuss sensitivity to assumptions

---

## Using the Tools

### View Public Market Analysis

**Comprehensive Report:**
```bash
./scripts/newco_cli.py public show
```

Shows:
- Current stock price and NAV
- Premium/discount analysis
- Comparable vehicles
- Investor base composition
- Liquidity metrics

### Track Stock Price

**Add Daily Price:**
```bash
./scripts/newco_cli.py public add-price \
  --date 2026-02-13 \
  --close 18.50 \
  --volume 75000
```

**View NAV:**
```bash
./scripts/newco_cli.py public nav
```

### Update NAV

**Add NAV Data:**
```bash
./scripts/newco_cli.py public add-nav \
  --date 2026-03-31 \
  --nav 20.50 \
  --shares 10000000
```

Automatically calculates premium/discount based on stock price.

### Monitor Comparables

**View Peer Group:**
```bash
./scripts/newco_cli.py public comparables
```

Shows comparable public vehicles and their premium/discount to NAV.

**Add Comparable:**
Edit `data/public_comparables.csv` to add peers.

### Track Investor Base

**View Composition:**
```bash
./scripts/newco_cli.py public investors
```

Shows breakdown by:
- Institutional vs retail
- Concentration (top 10 holders)
- Strategic investors
- Insider ownership

### Check Compliance Status

**Compliance Dashboard:**
```bash
./scripts/newco_cli.py compliance status
```

Shows:
- Trading blackout status
- Upcoming filing deadlines
- SEC requirements
- Fair value guidance

**Quarterly Calendar:**
```bash
./scripts/newco_cli.py compliance calendar --quarter 1 --year 2026
```

---

## Investor Relations

### Dual Constituency

**Public Shareholders:**
- Buy/sell stock on exchange
- Care about: Stock price, premium/discount, liquidity
- Communication: Earnings calls, press releases, investor conferences

**Private LPs:**
- Direct investors in the fund
- Care about: NAV, fund performance, manager selection
- Communication: Quarterly letters, annual meetings, capital calls

### IR Calendar

**Quarterly Earnings:**
- Earnings release (before market open)
- Earnings call (same day, typically 8am ET)
- Slides and transcript posted
- Q&A with analysts

**Annual Events:**
- Annual shareholder meeting
- Proxy voting
- Annual report publication

**Ongoing:**
- Non-deal roadshows (meet investors)
- Investor conferences (2-4x per year)
- One-on-one meetings with analysts
- Quarterly NAV disclosures

### Communications Strategy

**For Public Shareholders:**
- Emphasize: Liquidity, diversification, access
- Address: Discount to NAV, performance track record
- Transparency: Portfolio holdings, manager selection

**For Private LPs:**
- Emphasize: Fund performance, manager relationships
- Address: Public vs private benefits
- Alignment: Public stock option for liquidity

---

## Best Practices

### Narrowing the Discount

**Strategies to reduce premium/discount:**

1. **Strong Performance**
   - Outperform peers
   - Demonstrate manager selection skill
   - Show NAV growth

2. **Transparency**
   - Frequent NAV updates (weekly/monthly)
   - Detailed portfolio disclosure
   - Clear valuation methodology

3. **Liquidity Programs**
   - Share buybacks when trading at discount
   - Issuing shares when at premium
   - Managed distribution policy

4. **Investor Education**
   - Explain structure to retail investors
   - Host educational webinars
   - Clear, simple communications

5. **Corporate Actions**
   - Tender offers
   - Conversion to open-end structure
   - Merger with similar vehicle

### Managing Volatility

**Stock Price vs NAV:**
- Stock price can swing daily
- NAV only updates quarterly
- Creates apparent volatility

**Mitigation:**
- Frequent NAV updates
- Explain valuation lag
- Provide interim NAV estimates
- Highlight long-term NAV trend

### Activist Defense

**Discount Arbitrage Activists:**
- Buy at discount
- Push for:
  - Liquidation
  - Tender offer
  - Open-end conversion
  - Board seats

**Defense Strategies:**
- Strong performance (best defense)
- Narrow discount proactively
- Engaged shareholder communication
- Consider activist-friendly moves
- Maintain strong board

### Disclosure Management

**What to Disclose:**
- ✅ Portfolio holdings (quarterly)
- ✅ NAV methodology
- ✅ Material events
- ✅ Manager relationships
- ✅ Risk factors

**What to Protect:**
- ❌ Specific deal terms (confidential)
- ❌ Competitive intelligence
- ❌ Non-material info
- ❌ Future plans (forward-looking)

**Balance:**
- Transparency builds trust
- BUT protect competitive position
- "Disclose what's required, protect what's valuable"

---

## Monitoring Dashboard

### Weekly Checklist

**Monday:**
```bash
./scripts/newco_cli.py public show
./scripts/newco_cli.py compliance blackout
```

**After Price Update:**
```bash
./scripts/newco_cli.py public add-price --date [date] --close [price] --volume [volume]
./scripts/newco_cli.py public nav
```

### Monthly Checklist

**First Week:**
- Review liquidity metrics
- Check investor base changes
- Update comparables analysis

**Last Week:**
- Review compliance calendar
- Prepare for blackout period (if quarter end approaching)

### Quarterly Checklist

**Week After Quarter End:**
- Update NAV
- Prepare 10-Q/10-K
- Schedule earnings call
- Implement trading blackout

**Week of Earnings:**
- File 10-Q/10-K
- Host earnings call
- Update investor relations materials

---

## Key Metrics Summary

| Metric | Formula | Target | Check Command |
|--------|---------|--------|---------------|
| Premium/Discount | (Price - NAV) / NAV × 100 | -5% to +5% | `public nav` |
| Liquidity Score | Volume + Volatility | > 60/100 | `public liquidity` |
| Institutional % | Institutional / Total | 40-60% | `public investors` |
| Top 10 Concentration | Top 10 / Total | 40-70% | `public investors` |
| Avg Daily Volume | Sum(Volume) / Days | > 50,000 | `public liquidity` |

---

## Troubleshooting

**"Stock trading at large discount"**
- Review fund performance vs peers
- Increase disclosure frequency
- Consider buyback program
- Host investor education events

**"Low liquidity / High volatility"**
- Engage market makers
- Increase investor relations efforts
- Consider larger investor base
- Improve trading infrastructure

**"Activist shareholder pressure"**
- Focus on performance
- Engage proactively
- Consider friendly actions
- Strengthen board

**"Valuation questions"**
- Clearly disclose methodology
- Cross-check valuations
- Conservative approach
- Regular updates

---

## Resources

**Commands:**
- `./scripts/newco_cli.py public show` - Full analysis
- `./scripts/newco_cli.py public nav` - Premium/discount
- `./scripts/newco_cli.py compliance status` - Compliance dashboard

**Documentation:**
- [PLAYBOOK.md](PLAYBOOK.md) - Daily workflows
- [90_Day_Plan.md](90_Day_Plan.md) - Execution plan
- This guide - Public markets specifics

**Regulatory:**
- SEC.gov - Filing guidance
- Your legal counsel - Compliance questions
- Auditors - Fair value guidance

---

## Key Takeaways

1. **Premium/discount to NAV is your most important metric**
2. **Liquidity matters - track it closely**
3. **Disclosure builds trust - be transparent**
4. **Trading blackouts are sacred - never violate**
5. **Level 3 valuations require careful methodology**
6. **Public + private = dual constituency**
7. **Performance is best defense against discount**

---

*Your competitive advantage: Permanent capital + public liquidity + professional VC manager selection*

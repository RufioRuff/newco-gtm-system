# Reporting & Board Materials Guide

## Overview

The reporting system automates generation of board meeting materials and LP communications. This saves Ken Wallace 40+ hours per quarter on manual report preparation.

**Key Features:**
1. **Board Deck Automation** - Auto-generate quarterly board presentations
2. **LP Letter Generation** - Quarterly investor letters with placeholders for CEO message
3. **Capital Call Notices** - Automated LP communications for capital calls
4. **Distribution Notices** - Automated LP communications for distributions
5. **Annual Summaries** - Year-end performance reports
6. **Action Item Tracking** - Board action item management

---

## Board Reporting

### Generate Board Deck

```bash
# Generate board deck for current quarter
./scripts/newco_cli.py board deck

# Generate for specific quarter
./scripts/newco_cli.py board deck --quarter 2 --year 2026

# Generate text format (for email)
./scripts/newco_cli.py board deck --format text
```

**Output:** Markdown or text file in `/Users/rufio/NEWCO/reports/board/`

**What's Included:**

**Slide 1: Executive Summary**
- Portfolio NAV and TVPI
- Fund count
- Risk level
- Pipeline activity (active DD, IC review)
- Premium/discount to NAV (if public)

**Slide 2: Portfolio Overview**
- Total commitment and deployment
- Diversification by vintage, stage, sector
- Diversification score

**Slide 3: Performance Metrics**
- Portfolio TVPI, DPI, RVPI
- Top performing funds
- Fund performance distribution (how many > 1.0x, > 2.0x)

**Slide 4: Capital Deployment**
- Deployment status
- YTD capital calls
- 12-month forecast by quarter

**Slide 5: Manager Pipeline**
- Pipeline summary by stage
- Conversion rate
- Managers in IC review

**Slide 6: Public Market Performance** (if applicable)
- Stock price and premium/discount
- QTD and YTD returns
- Trading metrics
- Investor composition

**Slide 7: Risk Dashboard**
- Risk level and score
- Compliance status
- Policy violations
- Liquidity forecast

**Slide 8: Action Items**
- Open items
- Overdue items
- Recently completed

### Action Item Management

```bash
# List all action items
./scripts/newco_cli.py board actions

# Add new action item
./scripts/newco_cli.py board add-action \
  "Evaluate 2 new AI/ML fund opportunities" \
  --owner "Ken Wallace" \
  --due 2026-03-31

# Update action item status
./scripts/newco_cli.py board update-action AI0001 \
  --status "Completed" \
  --notes "Completed due diligence on both managers"
```

**Action Item Statuses:**
- `Open` - Not yet started
- `In Progress` - Work underway
- `Completed` - Finished
- `Deferred` - Postponed to future meeting

**Tracking:**
- All action items stored in `/Users/rufio/NEWCO/data/board_action_items.csv`
- Automatically included in next board deck
- Overdue items flagged in red

### Board Deck Workflow

**1 Week Before Board Meeting:**
```bash
# Generate board deck
./scripts/newco_cli.py board deck --quarter 1 --year 2026

# Review output
open reports/board/board_deck_Q1_2026.md

# Update action items
./scripts/newco_cli.py board actions
```

**Day of Board Meeting:**
- Board deck is pre-generated with all metrics
- All data is current as of generation time
- CEO can add narrative commentary as needed
- Action items from previous meeting are tracked

**After Board Meeting:**
```bash
# Add new action items from meeting
./scripts/newco_cli.py board add-action \
  "Complete due diligence on Zeta Ventures" \
  --owner "Senior Analyst" \
  --due 2026-04-30
```

**Time Saved:** 4-6 hours per quarter (from manual deck preparation)

---

## LP Reporting

### Generate Quarterly Letter

```bash
# Generate letter for current quarter
./scripts/newco_cli.py lp letter

# Generate for specific quarter
./scripts/newco_cli.py lp letter --quarter 2 --year 2026
```

**Output:** Markdown file in `/Users/rufio/NEWCO/reports/lp/`

**What's Auto-Generated:**

1. **Executive Summary**
   - Portfolio snapshot (NAV, commitments, performance)
   - Public market performance (if applicable)

2. **Portfolio Review**
   - Diversification by vintage, stage, sector
   - Performance highlights (top 3 funds)
   - Portfolio distribution (% above 1.0x, 2.0x)

3. **Manager Updates**
   - New commitments this quarter
   - Pipeline activity

4. **Capital Deployment & Liquidity**
   - Deployment status
   - 12-month capital call forecast
   - Distribution outlook

5. **Risk Management**
   - Risk level and compliance status
   - Vintage diversification
   - Liquidity position

6. **Looking Ahead**
   - Priorities for next quarter
   - Template paragraph (edit as needed)

7. **Appendix**
   - Fund-by-fund performance table

**What Needs Manual Editing:**

- **CEO Opening Message** (paragraph 1) - Customize for each quarter
- **Market Commentary** (section 3) - Add current market insights
- **Manager Updates** (section 4) - Add qualitative details
- **Looking Ahead** (section 6) - Customize priorities

**Process:**

```bash
# 1. Generate letter
./scripts/newco_cli.py lp letter

# 2. Open and edit
open reports/lp/quarterly_letter_Q1_2026.md

# 3. Edit these sections:
#    - CEO opening (paragraph 1)
#    - Market commentary
#    - Manager highlights
#    - Looking ahead

# 4. Convert to PDF for distribution
# (use pandoc, markdown editor, or copy to Word)
```

**Time Saved:** 30-35 hours per quarter (from ~40 hours to ~5 hours)

### Capital Call Notices

```bash
# Generate capital call notice
./scripts/newco_cli.py lp capital-call <fund_id> <amount> <due_date>

# Example
./scripts/newco_cli.py lp capital-call F001 500000 2026-03-15
```

**What's Included:**
- Fund details (name, manager, vintage)
- Call amount and due date
- Current fund metrics (TVPI, paid-in %)
- Pro-rata note (no LP action required for fund-of-funds structure)

**Use Case:**
When underlying fund manager issues capital call to NEWCO, generate notice to inform LPs. For a fund-of-funds, LPs typically don't need to do anything (NEWCO handles capital calls), but this keeps them informed.

### Distribution Notices

```bash
# Generate distribution notice
./scripts/newco_cli.py lp distribution <fund_id> <amount> <date>

# Example
./scripts/newco_cli.py lp distribution F002 300000 2026-03-20
```

**What's Included:**
- Fund details
- Distribution amount and type (capital gain, return of capital)
- Updated fund metrics (DPI, TVPI)
- Pro-rata allocation info
- Tax information note

**Use Case:**
When underlying fund makes distribution to NEWCO, generate notice to inform LPs of pro-rata distribution.

### Annual Summary

```bash
# Generate annual summary
./scripts/newco_cli.py lp annual 2025
```

**What's Included:**
- Full year portfolio overview
- Annual performance metrics
- Year's capital activity (calls and distributions)
- New commitments made during year
- Looking forward to next year

**Use Case:**
Year-end comprehensive report for LPs, typically distributed in January/February. Complements K-1 tax packages.

---

## Report Outputs

All reports are generated as **Markdown (.md)** files for flexibility:

### Why Markdown?

1. **Human-Readable** - Easy to read and edit in any text editor
2. **Version Control** - Can be tracked in git
3. **Flexible Output** - Convert to PDF, Word, HTML, PowerPoint
4. **Easy Editing** - Ken can edit CEO message and commentary directly

### Converting to Other Formats

**To PDF:**
```bash
# Using pandoc (install: brew install pandoc)
pandoc reports/lp/quarterly_letter_Q1_2026.md \
  -o quarterly_letter_Q1_2026.pdf \
  --pdf-engine=xelatex

# Using markdown editor (Typora, MacDown, etc.)
# Just open the .md file and export to PDF
```

**To Word:**
```bash
# Using pandoc
pandoc reports/lp/quarterly_letter_Q1_2026.md \
  -o quarterly_letter_Q1_2026.docx

# Or copy/paste from markdown editor to Word
```

**To PowerPoint (board deck):**
```bash
# Using pandoc
pandoc reports/board/board_deck_Q1_2026.md \
  -o board_deck_Q1_2026.pptx \
  -t beamer

# Or use markdown to generate slides with Marp, reveal.js, etc.
```

---

## Automation Workflows

### Weekly Executive Summary

Create simple script to email Ken weekly summary:

```bash
#!/bin/bash
# weekly_summary.sh

# Generate mini board deck (text format)
./scripts/newco_cli.py board deck --format text > /tmp/weekly_summary.txt

# Email to Ken
mail -s "Weekly Portfolio Summary" ken@newco.com < /tmp/weekly_summary.txt
```

Run weekly via cron:
```cron
# Every Monday at 8am
0 8 * * 1 /Users/rufio/NEWCO/weekly_summary.sh
```

### Month-End Close

```bash
#!/bin/bash
# month_end_close.sh

# 1. Update all NAVs (manual step reminder)
echo "Remember to update NAVs in data/fund_navs.csv"

# 2. Generate risk dashboard
./scripts/newco_cli.py risk dashboard > reports/monthly/risk_$(date +%Y%m).txt

# 3. Generate portfolio performance
./scripts/newco_cli.py portfolio performance > reports/monthly/performance_$(date +%Y%m).txt

echo "Month-end reports generated in reports/monthly/"
```

### Quarter-End Close

```bash
#!/bin/bash
# quarter_end.sh

QUARTER=$(( ($(date +%-m) - 1) / 3 + 1 ))
YEAR=$(date +%Y)

# 1. Generate board deck
./scripts/newco_cli.py board deck --quarter $QUARTER --year $YEAR

# 2. Generate LP letter
./scripts/newco_cli.py lp letter --quarter $QUARTER --year $YEAR

# 3. Generate governance report
./scripts/newco_cli.py risk governance > reports/board/governance_Q${QUARTER}_${YEAR}.txt

echo "Quarterly reports generated:"
echo "  - Board deck: reports/board/board_deck_Q${QUARTER}_${YEAR}.md"
echo "  - LP letter: reports/lp/quarterly_letter_Q${QUARTER}_${YEAR}.md"
echo "  - Governance: reports/board/governance_Q${QUARTER}_${YEAR}.txt"
echo ""
echo "Next steps:"
echo "  1. Review and edit LP letter (CEO message, market commentary)"
echo "  2. Review board deck"
echo "  3. Update board action items"
```

---

## Customization

### Board Deck Templates

To customize board deck format, edit `/Users/rufio/NEWCO/scripts/board_reporting.py`:

**Example: Add custom slide**

```python
def _generate_custom_slide(self):
    """Generate custom slide"""
    return {
        'title': 'Custom Slide',
        'content': 'Your custom content here'
    }

# Add to sections in generate_board_deck()
sections = {
    # ... existing slides ...
    'custom': self._generate_custom_slide()
}
```

### LP Letter Templates

To customize LP letter, edit `/Users/rufio/NEWCO/scripts/lp_reporting.py`:

**Example: Change opening**

```python
# Line ~68 in _compile_quarterly_letter()
if ceo_message:
    letter += f"{ceo_message}\n\n"
else:
    letter += f"""I am pleased to share our Q{quarter} {year} update.
    [Your custom default message here]
    """
```

### Report Branding

Add company branding to generated reports:

```python
# In _compile_markdown_report() or _compile_quarterly_letter()
header = """
![NEWCO Logo](assets/logo.png)

# NEWCO
*Leading publicly traded VC fund-of-funds*

---
"""
```

---

## Data Sources

Reports pull data from:

| Data Source | Used For |
|-------------|----------|
| `portfolio_management.py` | Fund metrics, performance, cashflow |
| `manager_crm.py` | Pipeline status, DD activity |
| `risk_management.py` | Risk scores, violations, compliance |
| `public_markets.py` | Stock price, premium/discount |
| `data/board_action_items.csv` | Action items tracking |

**Data Freshness:**
- Reports use real-time data from CSV files
- Ensure CSVs are updated before generating reports
- NAVs should be updated monthly or quarterly

---

## Best Practices

### For CEOs

1. **Generate board deck 1 week before meeting** - Time to review and add commentary
2. **Edit LP letter CEO message and market commentary** - Don't send template text
3. **Update action items after each board meeting** - Keep tracking current
4. **Review reports before distribution** - Auto-generated content may need context

### For Analysts

1. **Keep CSVs updated** - Reports are only as good as underlying data
2. **Update NAVs quarterly at minimum** - Critical for accurate reporting
3. **Log all capital calls and distributions** - Ensures accurate cashflow tracking
4. **Test reports after data updates** - Catch issues before board meeting

### For Board Members

1. **Board deck provides snapshot** - Deep dives available on request
2. **Action items track board directives** - Hold management accountable
3. **Risk dashboard shows compliance** - Key governance metric

---

## Troubleshooting

### "KeyError: 'fund_count'"

**Issue:** Portfolio data structure mismatch

**Fix:**
```bash
# Check portfolio structure
./scripts/newco_cli.py portfolio show

# If empty, load demo data
./scripts/demo_portfolio.py
```

### "Output file empty or incomplete"

**Issue:** Missing data in one of the underlying CSVs

**Fix:**
```bash
# Check which CSVs exist
ls data/*.csv

# Verify portfolio funds exist
cat data/portfolio_funds.csv

# Verify NAVs exist
cat data/fund_navs.csv
```

### "Manager pipeline empty"

**Issue:** No managers in CRM

**Fix:**
```bash
# Add demo managers
./scripts/demo_portfolio.py

# Or add manually
./scripts/newco_cli.py managers add \
  --fund "Example Fund I" \
  --gps "John Doe" \
  --firm "Example VC" \
  --stage "Seed"
```

### Board Deck Missing Slides

**Issue:** Some data sources not available (e.g., public markets)

**Solution:** This is expected. Slides that depend on unavailable data will show "*Data not available*" message. Add data to enable those slides.

---

## Future Enhancements

Planned features (not yet implemented):

1. **PowerPoint Export** - Direct PPTX generation
2. **Email Integration** - Send reports via email
3. **Templating Engine** - Fully customizable report templates
4. **Historical Tracking** - Compare quarter-over-quarter
5. **Interactive Dashboards** - Web-based report viewer
6. **AI Assistance** - Auto-draft CEO message and commentary

---

## Command Reference

### Board Commands

```bash
# Generate board deck
./scripts/newco_cli.py board deck [--quarter Q] [--year Y] [--format markdown|text]

# List action items
./scripts/newco_cli.py board actions

# Add action item
./scripts/newco_cli.py board add-action "<item>" --owner "<name>" --due YYYY-MM-DD

# Update action item
./scripts/newco_cli.py board update-action <ID> --status "<status>" --notes "<notes>"
```

### LP Commands

```bash
# Generate quarterly letter
./scripts/newco_cli.py lp letter [--quarter Q] [--year Y]

# Generate capital call notice
./scripts/newco_cli.py lp capital-call <fund_id> <amount> <due_date>

# Generate distribution notice
./scripts/newco_cli.py lp distribution <fund_id> <amount> <date>

# Generate annual summary
./scripts/newco_cli.py lp annual <year>
```

---

## Example Use Cases

### Quarterly Board Meeting Prep

```bash
# Week before meeting
./scripts/newco_cli.py board deck --quarter 1 --year 2026

# Review generated deck
open reports/board/board_deck_Q1_2026.md

# Check action items from last meeting
./scripts/newco_cli.py board actions

# Update completed actions
./scripts/newco_cli.py board update-action AI0001 --status "Completed"

# Print governance report for compliance discussion
./scripts/newco_cli.py risk governance > board_governance.txt
```

### Quarterly LP Communication

```bash
# Generate LP letter
./scripts/newco_cli.py lp letter

# Open and edit
open reports/lp/quarterly_letter_Q1_2026.md

# Edit:
# - CEO opening message (personalize for quarter)
# - Market commentary (add current insights)
# - Manager highlights (add qualitative color)

# Convert to PDF
pandoc reports/lp/quarterly_letter_Q1_2026.md -o LP_Letter_Q1_2026.pdf

# Distribute to LPs via email/portal
```

### Capital Call Management

```bash
# Underlying fund issues capital call to NEWCO
# Example: Acme Ventures calls $500K

# 1. Log in portfolio system
./scripts/newco_cli.py portfolio capital-call F001 500000 2026-03-15

# 2. Generate LP notice
./scripts/newco_cli.py lp capital-call F001 500000 2026-03-15

# 3. Review and send
open reports/lp/capital_call_F001_20260213.md

# 4. Track liquidity impact
./scripts/newco_cli.py risk liquidity
```

---

**Questions?**

For assistance with reporting:
- **Board Reporting:** Contact Ken Wallace
- **LP Communications:** Contact Investor Relations
- **Technical Issues:** Check troubleshooting section or system logs

---

*Last Updated: February 2026*
*Version: 1.0*

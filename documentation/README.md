# NEWCO GTM Management System

Complete backend system to execute the NEWCO go-to-market strategy across 324+ contacts.

## Quick Start

```bash
cd ~/NEWCO

# Install dependencies
pip install -r requirements.txt

# View dashboard
./scripts/newco_cli.py report dashboard

# See today's tasks
./scripts/newco_cli.py tasks today

# View top priorities
./scripts/newco_cli.py contact prioritize
```

## What This System Does

- **Contact Management:** Track 324+ contacts with status, tier, category, and priority scoring
- **Email Generation:** Auto-generate personalized emails from templates
- **Pipeline Tracking:** Monitor conversion rates, stage movement, and weekly KPIs
- **Activity Logging:** Record all emails, meetings, and calls
- **Task Automation:** Generate next actions based on 90-day blitz plan
- **Reporting:** Weekly reports, dashboards, and analytics

## Project Structure

```
~/NEWCO/
├── data/               # CSV database files
│   ├── contacts.csv
│   ├── interactions.csv
│   ├── pipeline.csv
│   └── targets.csv
├── templates/          # Email and meeting templates
│   ├── email/
│   ├── meeting/
│   └── follow_up/
├── scripts/            # Python CLI and modules
│   ├── newco_cli.py
│   ├── email_generator.py
│   ├── pipeline_manager.py
│   ├── reports.py
│   └── automation.py
├── config/             # Configuration files
│   ├── config.yaml
│   └── personas.yaml
├── docs/               # Documentation
│   ├── PLAYBOOK.md     # User guide
│   ├── 90_Day_Plan.md  # Execution roadmap
│   └── NEWCO_One_Pager.md
└── reports/            # Generated reports
    ├── weekly/
    └── exports/
```

## Core Features

### 1. LinkedIn Network Scraping & Analysis 🌟 NEW! 🔥
**Scrape 1st-4th degree LinkedIn connections and run network effects analysis**

```bash
# ONE COMMAND - Full pipeline (30-60 min)
./scripts/run_full_network_analysis.sh

# Scrapes Jason Goldman's network, imports to NEWCO, runs analysis
```

**What it does:**
- 🕸️ Scrapes LinkedIn profiles & connections (1st-4th degree)
- 📊 Maps 500-1000+ contacts into network graph
- 🎯 Identifies network multipliers, brokers, structural holes
- 🔗 Finds warm introduction paths
- 💾 Imports all data into NEWCO contact system

**Output:**
- Top 10-20 **network multipliers** (1 person = 10+ connections leverage)
- **Warm intro paths** to reach anyone (30-50% vs 1-3% cold email)
- **Structural hole** positions for competitive advantage
- **Broker** identification for accessing disconnected groups

See [LINKEDIN_NETWORK_ANALYSIS_GUIDE.md](LINKEDIN_NETWORK_ANALYSIS_GUIDE.md) for complete guide.

### 2. Social Network Analysis 🌟
Grounded in academic research (Granovetter, Burt, Freeman, etc.)

```bash
# Comprehensive network analysis
./scripts/newco_cli.py network analyze

# Identify network multipliers (most valuable contacts)
./scripts/newco_cli.py network multipliers

# Find brokers (bridge different groups)
./scripts/newco_cli.py network brokers

# Calculate network influence
./scripts/newco_cli.py network influence
```

**Key Metrics:**
- **Network Multipliers** - Contacts who can open entire networks
- **Structural Holes** - Access to non-redundant networks (Burt 1992)
- **Betweenness Centrality** - Brokers between communities (Freeman 1977)
- **Tie Strength** - Weak vs strong ties (Granovetter 1973)
- **Homophily** - Network diversity analysis

See [NETWORK_ANALYSIS_GUIDE.md](docs/NETWORK_ANALYSIS_GUIDE.md) for complete guide.

### 3. Relationship Management
```bash
# Add relationship between contacts
./scripts/newco_cli.py relationship add 1 2 --strength 0.8 --type "worked_with"

# Show all relationships for a contact
./scripts/newco_cli.py relationship show 1

# Find warm intro paths
./scripts/newco_cli.py relationship intro-path 15

# Find mutual connections
./scripts/newco_cli.py relationship mutual 1 5

# Identify introduction opportunities
./scripts/newco_cli.py relationship opportunities
```

### 4. Advanced Analytics
```bash
# Show advanced analytics dashboard
./scripts/newco_cli.py analytics show

# Get insights and recommendations
./scripts/newco_cli.py analytics insights

# Show conversion funnel
./scripts/newco_cli.py analytics funnel

# Identify stalled contacts
./scripts/newco_cli.py analytics stalled

# Show week 12 predictions
./scripts/newco_cli.py analytics predictions
```

### 5. Contact Management
```bash
# List contacts
./scripts/newco_cli.py contact list

# Filter by tier, status, or category
./scripts/newco_cli.py contact list --tier 1 --status "Cold"

# Show contact details
./scripts/newco_cli.py contact show <id>

# Update contact
./scripts/newco_cli.py contact update <id> --status "Meeting Scheduled"

# Search contacts
./scripts/newco_cli.py contact search "Goldman"
```

### 6. Email Generation
```bash
# Generate personalized email (auto-detect template)
./scripts/newco_cli.py email generate <id>

# Use specific template
./scripts/newco_cli.py email generate <id> --template vc_partner

# Batch generate
./scripts/newco_cli.py email batch --tier 1
```

### 7. Activity Logging
```bash
# Log email
./scripts/newco_cli.py log email <id> "Subject" --sent

# Log meeting
./scripts/newco_cli.py log meeting <id> "Meeting title" \
  --outcome "Positive" --next-steps "Send deck"

# Log call
./scripts/newco_cli.py log call <id> "Call notes"
```

### 8. Pipeline & Reports
```bash
# Show pipeline
./scripts/newco_cli.py pipeline show

# Weekly metrics
./scripts/newco_cli.py pipeline weekly

# Generate weekly report
./scripts/newco_cli.py report weekly

# Show dashboard
./scripts/newco_cli.py report dashboard
```

### 9. Task Management
```bash
# Today's tasks
./scripts/newco_cli.py tasks today

# This week
./scripts/newco_cli.py tasks week

# Overdue
./scripts/newco_cli.py tasks overdue
```

## Documentation

- **[PLAYBOOK.md](docs/PLAYBOOK.md)** - Complete user guide with daily workflows
- **[90_Day_Plan.md](docs/90_Day_Plan.md)** - Week-by-week execution plan
- **[NEWCO_One_Pager.md](docs/NEWCO_One_Pager.md)** - Pitch document for reference

## Data Import

To populate the contacts database from your source documents, see `scripts/import_contacts.py`.

## Configuration

Edit `config/config.yaml` to customize:
- Pipeline statuses
- KPI targets
- Automation settings
- Email signature

Edit `config/personas.yaml` to customize:
- Contact categories
- Persona definitions
- Prioritization rules

## Email Templates

Templates are in `templates/email/`:
- `platform_gatekeeper.md` - Institutional platforms
- `family_office_cio.md` - Family office CIOs
- `vc_partner.md` - VC partners (LP intros)
- `foundation_leader.md` - Foundation leaders
- `network_multiplier.md` - Top-tier connectors

Edit templates to customize messaging while keeping `{{variables}}` intact.

## Requirements

- Python 3.10+
- PyYAML
- Jinja2 (optional, for advanced templating)

Install with:
```bash
pip install -r requirements.txt
```

## Getting Started

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Import your contacts**
   ```bash
   # Manual: Add contacts one by one
   ./scripts/newco_cli.py contact add --name "John Doe" --company "Acme" \
     --category "VC Partner" --tier 3

   # Or use import script (see scripts/import_contacts.py)
   ```

3. **Review templates**
   - Check `templates/email/` and customize as needed
   - Review `templates/meeting/` for meeting prep

4. **Start executing**
   ```bash
   # View dashboard
   ./scripts/newco_cli.py report dashboard

   # See top priorities
   ./scripts/newco_cli.py contact prioritize

   # Generate first email
   ./scripts/newco_cli.py email generate 1
   ```

5. **Read the playbook**
   - `docs/PLAYBOOK.md` has complete workflows
   - `docs/90_Day_Plan.md` has week-by-week execution plan

## Daily Workflow

**Morning (10 min):**
```bash
./scripts/newco_cli.py report dashboard
./scripts/newco_cli.py tasks today
./scripts/newco_cli.py contact prioritize
```

**After each interaction:**
```bash
./scripts/newco_cli.py log [email|meeting|call] <id> "Details"
./scripts/newco_cli.py contact update <id> --status "..." --next-action "..."
```

**Weekly (Monday):**
```bash
./scripts/newco_cli.py report weekly
./scripts/newco_cli.py pipeline show
./scripts/newco_cli.py tasks week
```

## Support

- Read `docs/PLAYBOOK.md` for detailed guidance
- Check inline help: `./scripts/newco_cli.py --help`
- Review templates in `templates/`

## Success Metrics

Track your progress toward:
- 50+ meetings in 90 days
- 25+ active conversations
- 5-10 LP commitments
- $10-25M first close

Use `./scripts/newco_cli.py report dashboard` to monitor progress.

---

**Built to transform NEWCO's GTM strategy from docs into executable operations.**

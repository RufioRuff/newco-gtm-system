# NEWCO - LinkedIn Network Analysis & GTM Management System

**Location:** `/Users/rufio/NEWCO/`
**Purpose:** Go-To-Market management system for NEWCO Fund I fundraising with LinkedIn network scraping and social network analysis

---

## Quick Start

### For Co-Founders
```bash
cd ~/NEWCO
./bin/LAUNCH.sh                    # Launch the platform
./bin/PARTNER_SETUP.sh            # Setup for partner
```

**Read First:**
- `documentation/CO_FOUNDER_QUICK_START.md` - 5-minute quick start
- `documentation/guides/LINKEDIN_NETWORK_ANALYSIS_GUIDE.md` - Complete LinkedIn guide
- `documentation/PLAYBOOK.md` - Daily workflows

### Run LinkedIn Network Analysis
```bash
export LINKEDIN_EMAIL="your@email.com"
export LINKEDIN_PASSWORD="yourpassword"
./bin/run_full_network_analysis.sh
```

### Use CLI
```bash
cd core/scripts
./newco_cli.py --help              # See all commands
./newco_cli.py contact list        # List contacts
./newco_cli.py network analyze     # Run network analysis
./newco_cli.py email generate <id> # Generate personalized email
```

---

## Directory Structure

```
~/NEWCO/
├── core/                          # Core NEWCO application
│   ├── api/                       # Backend API
│   ├── frontend/                  # Frontend application
│   ├── models/                    # ML models
│   ├── config/                    # Configuration files
│   ├── scripts/                   # Python scripts (CLI, analytics, etc.)
│   └── templates/                 # Email and document templates
│
├── agents/                        # AI agents & orchestration
│   ├── agent-orchestrator/        # Multi-agent orchestration
│   ├── specialized-agents/        # Domain-specific agents
│   ├── alpha-engine/              # Alpha generation engine
│   ├── karpathy-agent/            # Karpathy-inspired agent
│   └── llm-council/               # LLM council for decision-making
│
├── data-storage/                  # All data files
│   ├── data/                      # Core data (contacts, relationships, etc.)
│   ├── PE-VC-Source-Data/         # PE/VC source data
│   ├── data-scraper/              # Scraped data
│   ├── daily_summaries/           # Daily activity summaries
│   ├── reports/                   # Generated reports
│   └── metal_ai/                  # Metal AI integration data
│
├── documentation/                 # All documentation
│   ├── guides/                    # User guides and tutorials
│   │   ├── LINKEDIN_NETWORK_ANALYSIS_GUIDE.md
│   │   ├── QUICK_START.md
│   │   ├── CO_FOUNDER_QUICK_START.md
│   │   └── ...
│   ├── status-reports/            # Status and completion reports
│   ├── setup/                     # Setup and deployment guides
│   ├── reference/                 # Reference documentation
│   ├── README.md                  # Main project README
│   └── PLAYBOOK.md                # Daily workflow playbook
│
├── external-projects/             # Third-party repositories
│   ├── ml-frameworks/             # Large ML frameworks
│   │   ├── arrow/                 # Apache Arrow (303MB)
│   │   ├── tvm/                   # TVM deep learning compiler (764MB)
│   │   └── xgboost/               # XGBoost library (56MB)
│   └── other/                     # Other external projects
│
├── learning/                      # Learning resources
│   ├── karpathy-repos/            # Andrej Karpathy's repositories
│   │   ├── micrograd/
│   │   ├── minGPT/
│   │   ├── nanoGPT/
│   │   ├── minbpe/
│   │   └── llm.c/
│   ├── notebooks/                 # Jupyter notebooks
│   │   └── deep-learning-with-python-notebooks/
│   └── projects/                  # Learning projects
│       ├── build-your-own-x/
│       ├── learning-projects/
│       └── ml_workspace/
│
├── archive/                       # Archived/deprecated code
│   └── newco-unified-platform/    # Old unified platform (1GB)
│
├── bin/                           # Executable scripts
│   ├── EXECUTE_NOW.sh
│   ├── LAUNCH.sh
│   ├── PARTNER_SETUP.sh
│   ├── start_ai_platform.sh
│   ├── start_platform.sh
│   └── SYNC_TO_GITHUB.sh
│
├── CLAUDE.md                      # Instructions for AI assistants
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Key Features

### 1. LinkedIn Network Scraping
- Multi-degree connection crawler (1st-4th degree)
- Profile scraping with authentication
- Rate limiting and ethical scraping
- Caching for efficiency

**Scripts:**
- `core/scripts/linkedin_scraper.py`
- `core/scripts/linkedin_network_crawler.py`
- `core/scripts/import_linkedin_network.py`

### 2. Social Network Analysis
Academic theory-based analysis using:
- **Granovetter (1973)** - Weak Ties Theory
- **Burt (1992)** - Structural Holes
- **Freeman (1977)** - Betweenness Centrality
- **Bonacich (1987)** - Network Influence

**Features:**
- Network multiplier identification (1 person = 10+ connections)
- Structural hole analysis
- Broker identification
- Warm intro path finding

**Script:** `core/scripts/network_analysis.py`

### 3. Contact & Relationship Management
- 324+ contacts with tier/category/status tracking
- Relationship graph (who knows whom)
- Interaction history
- Pipeline tracking

**Data Files:**
- `data-storage/data/contacts.csv`
- `data-storage/data/relationships.csv`
- `data-storage/data/interactions.csv`

### 4. Email Generation
Personalized email templates for:
- Network multipliers (Tier 0)
- Platform gatekeepers
- Family office CIOs
- VC partners
- Foundation leaders

**Templates:** `core/templates/email/`

### 5. Analytics & Reporting
- Pipeline analytics
- Network metrics
- Board reporting
- Competitive intelligence
- Portfolio management

**Scripts:** `core/scripts/analytics.py`, `board_reporting.py`, etc.

---

## Installation

### Prerequisites
- Python 3.10+
- Node.js (for frontend)

### Install Dependencies
```bash
cd ~/NEWCO
pip install -r requirements.txt
playwright install chromium  # For LinkedIn scraping
```

### Environment Variables
Add to `~/.zshrc` or `~/.bash_profile`:
```bash
export LINKEDIN_EMAIL="your@email.com"
export LINKEDIN_PASSWORD="yourpassword"
```

---

## Usage Examples

### Scrape LinkedIn Network
```bash
cd ~/NEWCO
export LINKEDIN_EMAIL="email@example.com"
export LINKEDIN_PASSWORD="password"
./bin/run_full_network_analysis.sh
```

### Add a Contact
```bash
cd ~/NEWCO/core/scripts
./newco_cli.py contact add \
  --name "Jane Doe" \
  --company "Acme VC" \
  --category "VC Partner" \
  --tier 2
```

### Find Warm Intro Path
```bash
./newco_cli.py relationship intro-path <target_id>
```

### Generate Email
```bash
./newco_cli.py email generate <contact_id> --template network_multiplier
```

### View Network Multipliers
```bash
./newco_cli.py network multipliers
```

---

## Documentation

### Essential Reading
1. **For Non-Technical Co-Founders:**
   - `documentation/CO_FOUNDER_QUICK_START.md` - 5-minute overview
   - `documentation/PLAYBOOK.md` - Daily workflows
   - `documentation/guides/QUICK_START.md` - Getting started

2. **For Technical Setup:**
   - `documentation/guides/LINKEDIN_NETWORK_ANALYSIS_GUIDE.md` - Complete guide
   - `documentation/setup/DEPLOY_NOW.md` - Deployment
   - `documentation/NETWORK_ANALYSIS_GUIDE.md` - Network theory

3. **For Development:**
   - `CLAUDE.md` - Instructions for AI assistants
   - `documentation/reference/` - Technical reference

### Status Reports
See `documentation/status-reports/` for:
- Phase completion reports
- Integration summaries
- System status

---

## Network Effects Strategy

### Key Principles
1. **Network Multipliers > Individual Contacts**
   - Focus on 10-20 people who can open entire networks
   - 1 multiplier = 10+ individual contacts in leverage

2. **Weak Ties Are Valuable**
   - 73% of opportunities come through weak ties
   - 2nd/3rd degree connections provide novel information

3. **Structural Holes = Competitive Advantage**
   - Bridge disconnected groups
   - Non-redundant networks provide diverse information

4. **Warm Intros Work**
   - 30-50% response rate vs 1-3% cold email
   - Always find the warm introduction path

### GTM Execution
- **Week 1-2:** Activate network multipliers
- **Week 3-4:** Leverage weak ties (2nd/3rd degree)
- **Week 5-6:** Bridge structural holes

---

## Performance

### LinkedIn Scraping
- Full 4-degree crawl: 30-60 minutes
- 2-degree crawl (recommended start): 10-15 minutes
- Expected output: 500-1000+ contacts

### Network Analysis
- Analysis runtime: 1-2 minutes
- Network multipliers identified: 10-20
- Warm intro paths computed in real-time

---

## Important Notes

### LinkedIn Terms of Service
- Use responsibly for personal network analysis only
- Built-in rate limiting to respect LinkedIn
- Not for commercial data collection
- May require 2FA during login

### Privacy
- Only scrapes public profile information
- Respects LinkedIn privacy settings
- All data stored locally only

### Data Storage
- Contact data: `data-storage/data/contacts.csv`
- Relationship graph: `data-storage/data/relationships.csv`
- LinkedIn cache: `data-storage/linkedin_cache/`

---

## Architecture

### Core Application (`core/`)
The main NEWCO application with API, frontend, models, and business logic scripts.

### Agents (`agents/`)
AI-powered agents for various tasks:
- **agent-orchestrator:** Multi-agent coordination
- **specialized-agents:** Domain-specific agents
- **alpha-engine:** Alpha generation
- **llm-council:** Multi-LLM decision making

### Data Storage (`data-storage/`)
All data files organized by type:
- Primary data (contacts, relationships, interactions)
- Scraped data (PE/VC data, LinkedIn data)
- Generated reports and summaries

### External Projects (`external-projects/`)
Third-party repositories for learning and reference:
- Large ML frameworks (Arrow, TVM, XGBoost)
- These are NOT part of core NEWCO functionality

### Learning Resources (`learning/`)
Educational materials:
- Karpathy's repositories (micrograd, GPT implementations)
- Jupyter notebooks
- Tutorial projects

---

## Project History

- **Phase 1-5:** Core GTM & Capital Raising system
- **February 2026:** LinkedIn network scraping system added
  - Multi-degree connection crawler
  - Social network analysis integration
  - Import/export pipelines
  - Academic theory implementation
- **February 2026:** Directory organization and cleanup

---

## Support

### For Issues
- Check documentation in `documentation/`
- Review `CLAUDE.md` for AI assistant guidance
- Examine status reports in `documentation/status-reports/`

### Key Contacts
- Project Location: `/Users/rufio/NEWCO/`
- Main Guide: `documentation/guides/LINKEDIN_NETWORK_ANALYSIS_GUIDE.md`

---

Last Updated: February 14, 2026

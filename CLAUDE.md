# CLAUDE.md - Instructions for AI Assistants

This file provides context for AI assistants (like Claude Code) working with the NEWCO project.

---

## Project Overview

**NEWCO** is a GTM (Go-To-Market) management system for NEWCO Fund I fundraising, featuring:
1. **Contact management** - 324+ contacts with tier/category/status tracking
2. **LinkedIn network scraping** - Multi-degree connection mapping
3. **Social network analysis** - Academic theory-based network effects analysis
4. **Email generation** - Personalized templates
5. **Pipeline tracking** - Conversion rates and KPIs
6. **Relationship management** - Who knows whom, warm intro paths

---

## Key Systems

### LinkedIn Network Analysis System (NEW - Feb 2026)
**Location:** `/Users/rufio/NEWCO/core/scripts/linkedin_*.py`

**Purpose:** Scrape Jason Eliot Goldman's LinkedIn network (1st-4th degree), import into NEWCO, run social network analysis

**Quick Start:**
```bash
export LINKEDIN_EMAIL="email"
export LINKEDIN_PASSWORD="password"
~/NEWCO/bin/run_full_network_analysis.sh
```

**Key Files:**
- `core/scripts/linkedin_scraper.py` - Profile scraper with auth
- `core/scripts/linkedin_network_crawler.py` - Multi-degree BFS crawler
- `core/scripts/import_linkedin_network.py` - Import to NEWCO system
- `bin/run_full_network_analysis.sh` - Full pipeline orchestration (symlink)
- `documentation/guides/LINKEDIN_NETWORK_ANALYSIS_GUIDE.md` - Complete 200+ line guide
- `documentation/guides/CO_FOUNDER_QUICK_START.md` - 5-minute quick start for co-founder

**Academic Foundation:**
- Granovetter (1973) - Weak Ties Theory
- Burt (1992) - Structural Holes
- Freeman (1977) - Betweenness Centrality
- Bonacich (1987) - Network Influence

**Output:**
- 500-1000+ contacts mapped across 4 degrees
- Network multipliers identified (1 person = 10+ connections leverage)
- Structural holes, brokers, warm intro paths
- 30-50% response rate on warm intros vs 1-3% cold

### Network Analysis Engine
**Location:** `/Users/rufio/NEWCO/core/scripts/network_analysis.py`

**Purpose:** Social network analysis using academic research

**Key Algorithms:**
- `calculate_degree_centrality()` - Freeman 1978
- `calculate_betweenness_centrality()` - Freeman 1977
- `calculate_structural_holes()` - Burt 1992
- `analyze_tie_strength()` - Granovetter 1973
- `calculate_network_influence_score()` - Bonacich 1987
- `identify_network_multipliers()` - Composite score
- `analyze_homophily()` - McPherson 2001

**CLI:**
```bash
~/NEWCO/bin/newco network analyze
~/NEWCO/bin/newco network multipliers
~/NEWCO/bin/newco network brokers
```

### Contact & Relationship Management
**Location:** `/Users/rufio/NEWCO/core/scripts/`

**Files:**
- `data-storage/data/contacts.csv` - 324+ contacts with tier/category
- `data-storage/data/relationships.csv` - Relationship graph
- `data-storage/data/interactions.csv` - Activity log
- `core/scripts/relationship_manager.py` - Relationship operations

**CLI:**
```bash
~/NEWCO/bin/newco contact list
~/NEWCO/bin/newco relationship add <id1> <id2> --strength 0.8
~/NEWCO/bin/newco relationship intro-path <target_id>
```

### Email Generation
**Location:** `/Users/rufio/NEWCO/core/templates/email/`

**Templates:**
- `network_multiplier.md` - Tier 0 highest priority
- `platform_gatekeeper.md` - Institutional platforms
- `family_office_cio.md` - Family offices
- `vc_partner.md` - VC partners
- `foundation_leader.md` - Foundations

**CLI:**
```bash
~/NEWCO/bin/newco email generate <id> --template network_multiplier
```

---

## Documentation Structure

### For Co-Founder
1. **documentation/guides/CO_FOUNDER_QUICK_START.md** - 5-minute quick start
2. **README.md** - Project overview
3. **documentation/PLAYBOOK.md** - Daily workflows

### Technical Documentation
1. **documentation/guides/LINKEDIN_NETWORK_ANALYSIS_GUIDE.md** - Complete LinkedIn scraping guide
2. **documentation/NETWORK_ANALYSIS_GUIDE.md** - Network effects theory
3. **documentation/90_Day_Plan.md** - GTM execution strategy
4. **documentation/NEWCO_One_Pager.md** - Investment thesis

### System Documentation
- **documentation/status-reports/** - System architecture and phase completion docs
- **documentation/reference/** - Technical reference documentation
- **ORGANIZATION.md** - Directory structure guide

---

## Common Tasks

### Run LinkedIn Network Analysis
```bash
cd ~/NEWCO
export LINKEDIN_EMAIL="email"
export LINKEDIN_PASSWORD="password"
./bin/run_full_network_analysis.sh
```

### Add New Contact
```bash
~/NEWCO/bin/newco contact add \
  --name "Name" \
  --company "Company" \
  --category "VC Partner" \
  --tier 2
```

### Add Relationship
```bash
~/NEWCO/bin/newco relationship add 1 2 \
  --type "worked_with" \
  --strength 0.8 \
  --notes "Collaborated on deals"
```

### Generate Email
```bash
~/NEWCO/bin/newco email generate <id>
```

### View Dashboard
```bash
~/NEWCO/bin/newco report dashboard
```

---

## Key Principles

### Network Effects Strategy
1. **Network Multipliers > Individual Contacts**
   - Focus on 10-20 people who can open entire networks
   - 1 multiplier = 10+ individual contacts in leverage

2. **Weak Ties Are Valuable**
   - 73% of opportunities come through weak ties (Granovetter 1973)
   - 2nd/3rd degree connections provide novel information

3. **Structural Holes = Competitive Advantage**
   - Seek positions bridging disconnected groups
   - Non-redundant networks provide diverse information

4. **Warm Intros Work**
   - 30-50% response rate vs 1-3% cold email
   - Always find the warm introduction path

### GTM Strategy
- **Week 1-2:** Activate network multipliers
- **Week 3-4:** Leverage weak ties (2nd/3rd degree)
- **Week 5-6:** Bridge structural holes
- **Focus:** Top 10 multipliers first, then expand

---

## Data Files

### Primary Data
- `data-storage/data/contacts.csv` - Contact database
- `data-storage/data/relationships.csv` - Relationship graph
- `data-storage/data/interactions.csv` - Activity log
- `data-storage/data/pipeline.csv` - Deal pipeline
- `data-storage/data/linkedin_networks/` - Scraped LinkedIn data

### Cache
- `data-storage/data/linkedin_cache/` - LinkedIn scraping cache

### Reports
- `data-storage/reports/` - Generated reports

---

## Dependencies

### Core
- Python 3.10+
- pyyaml>=6.0

### LinkedIn Scraping
- playwright>=1.40.0 (browser automation)
- beautifulsoup4>=4.12.0
- lxml>=4.9.0

### Installation
```bash
pip install -r requirements.txt
playwright install chromium
```

---

## Environment Variables

### LinkedIn Scraping
```bash
export LINKEDIN_EMAIL="your@email.com"
export LINKEDIN_PASSWORD="yourpassword"
```

Add to `~/.zshrc` or `~/.bash_profile` for persistence.

---

## Important Notes

### LinkedIn ToS
- Use responsibly for personal network analysis
- Built-in rate limiting
- Not for commercial data collection
- May require 2FA during login

### Privacy
- Only scrapes public profile information
- Respects LinkedIn privacy settings
- Data stored locally only

### Performance
- Full 4-degree crawl: 30-60 minutes
- 2-degree crawl (recommended start): 10-15 minutes
- Network analysis: 1-2 minutes

---

## For AI Assistants

### When User Asks About Network Effects
1. Point to `documentation/guides/LINKEDIN_NETWORK_ANALYSIS_GUIDE.md`
2. Explain key concepts: network multipliers, weak ties, structural holes
3. Show CLI commands for network analysis
4. Reference academic papers: Granovetter, Burt, Freeman

### When User Wants to Run LinkedIn Scraping
1. Check if credentials are set (`echo $LINKEDIN_EMAIL`)
2. Check if Playwright is installed
3. Run `~/NEWCO/bin/run_full_network_analysis.sh`
4. Point to `documentation/guides/CO_FOUNDER_QUICK_START.md` for co-founder

### When User Asks About Contacts
1. Use CLI: `~/NEWCO/bin/newco contact list`
2. Data in: `data-storage/data/contacts.csv`
3. Can filter by tier, status, category

### When User Asks About Relationships
1. Use CLI: `~/NEWCO/bin/newco relationship show <id>`
2. Data in: `data-storage/data/relationships.csv`
3. Can find warm intro paths

### When Making Changes
1. Always read files first before editing
2. Preserve existing functionality
3. Follow existing code patterns
4. Update documentation if adding features
5. Test with demo data first

---

## Project History

- **Phase 1-5:** GTM & Capital Raising system built
- **Feb 2026:** LinkedIn network scraping system added
  - Multi-degree connection crawler
  - Social network analysis integration
  - Import/export pipelines
  - Academic theory implementation
- **Feb 14, 2026:** Directory reorganization
  - Organized into clear structure: core/, agents/, data-storage/, documentation/, etc.
  - Created bin/ for quick access to executables
  - Separated learning materials and external projects
  - See ORGANIZATION.md for details

---

## Contact

- **Project:** NEWCO Fund I GTM Management
- **Location:** `/Users/rufio/NEWCO/`
- **Quick Start:** `documentation/guides/CO_FOUNDER_QUICK_START.md`
- **Main Guide:** `documentation/guides/LINKEDIN_NETWORK_ANALYSIS_GUIDE.md`
- **Organization:** `ORGANIZATION.md`

---

Last Updated: February 14, 2026

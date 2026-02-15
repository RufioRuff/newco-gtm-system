# NEWCO Directory Organization

**Date:** February 14, 2026
**Status:** Complete

This document explains the directory structure and organization of the NEWCO project.

---

## Overview

The NEWCO directory has been organized into a clean, logical structure that separates:
1. **Core application code** - The main NEWCO system
2. **AI agents** - Autonomous agents and orchestration
3. **Data** - All data files and storage
4. **Documentation** - All guides, reports, and references
5. **External projects** - Third-party repos for learning
6. **Learning resources** - Educational materials
7. **Executables** - Quick access scripts
8. **Archive** - Deprecated code

---

## Directory Structure

### `/core/` - Core Application
The heart of NEWCO with all business logic and main features.

```
core/
├── api/                # Backend API
├── frontend/           # Frontend application
├── models/             # ML models
├── config/             # Configuration files
├── scripts/            # Python scripts (CLI, analytics, LinkedIn, etc.)
└── templates/          # Email and document templates
```

**Key Scripts:**
- `newco_cli.py` - Main CLI interface
- `linkedin_scraper.py` - LinkedIn profile scraper
- `linkedin_network_crawler.py` - Multi-degree network crawler
- `network_analysis.py` - Social network analysis
- `analytics.py`, `board_reporting.py`, etc. - Business analytics

**Quick Access:** Use `~/NEWCO/bin/newco` symlink for CLI

---

### `/agents/` - AI Agents
Autonomous agents and multi-agent orchestration systems.

```
agents/
├── agent-orchestrator/   # Multi-agent coordination
├── specialized-agents/   # Domain-specific agents
├── alpha-engine/         # Alpha generation engine
├── karpathy-agent/       # Karpathy-inspired agent
└── llm-council/          # Multi-LLM decision making
```

---

### `/data-storage/` - All Data
Centralized data storage for all project data.

```
data-storage/
├── data/                 # Core data (contacts, relationships, interactions)
├── PE-VC-Source-Data/    # PE/VC source data
├── data-scraper/         # Scraped data outputs
├── daily_summaries/      # Daily activity summaries
├── reports/              # Generated reports
└── metal_ai/             # Metal AI integration data
```

**Key Files:**
- `data/contacts.csv` - 324+ contacts
- `data/relationships.csv` - Relationship graph
- `data/interactions.csv` - Interaction history
- `data/linkedin_networks/` - LinkedIn scraped data
- `data/linkedin_cache/` - LinkedIn scraping cache

---

### `/documentation/` - Documentation
All project documentation organized by type.

```
documentation/
├── guides/                    # User guides and tutorials
│   ├── LINKEDIN_NETWORK_ANALYSIS_GUIDE.md
│   ├── QUICK_START.md
│   ├── CO_FOUNDER_QUICK_START.md
│   └── ...
├── status-reports/            # Completion and status reports
│   ├── PHASE2_COMPLETE.md
│   ├── INTEGRATION_COMPLETE.md
│   └── ...
├── setup/                     # Setup and deployment guides
│   └── DEPLOY_NOW.md
├── reference/                 # Technical reference docs
│   ├── ALPHA_ENGINE_INTEGRATION_GUIDE.md
│   ├── LLM_INTEGRATION_GUIDE.md
│   └── ...
├── README.md                  # Main README
├── FOR_CO_FOUNDER.txt         # Co-founder notes
└── PLAYBOOK.md                # Daily workflow guide
```

---

### `/external-projects/` - Third-Party Code
Large third-party repositories for learning and reference.

```
external-projects/
├── ml-frameworks/
│   ├── arrow/           # Apache Arrow (303MB)
│   ├── tvm/             # TVM compiler (764MB)
│   └── xgboost/         # XGBoost (56MB)
└── other/
```

**Note:** These are NOT part of core NEWCO functionality. They're included for learning and potential future integration.

---

### `/learning/` - Learning Resources
Educational materials and tutorial projects.

```
learning/
├── karpathy-repos/                        # Andrej Karpathy's repos
│   ├── micrograd/                         # Micrograd
│   ├── minGPT/                            # Minimal GPT
│   ├── nanoGPT/                           # Nano GPT
│   ├── minbpe/                            # Minimal BPE
│   └── llm.c/                             # LLM in C
├── notebooks/
│   └── deep-learning-with-python-notebooks/
└── projects/
    ├── build-your-own-x/
    ├── learning-projects/
    └── ml_workspace/
```

---

### `/bin/` - Executable Scripts
Quick access to key executable scripts.

```
bin/
├── EXECUTE_NOW.sh                         # Execute platform
├── LAUNCH.sh                              # Launch platform
├── PARTNER_SETUP.sh                       # Partner setup
├── run_full_network_analysis.sh          # Run LinkedIn analysis (symlink)
├── newco                                  # CLI shortcut (symlink)
└── ...
```

**Usage:**
```bash
~/NEWCO/bin/newco --help
~/NEWCO/bin/run_full_network_analysis.sh
```

---

### `/archive/` - Deprecated Code
Old or deprecated code kept for reference.

```
archive/
└── newco-unified-platform/    # Old unified platform (1GB)
```

---

## Key Files at Root

```
~/NEWCO/
├── CLAUDE.md              # Instructions for AI assistants
├── requirements.txt       # Python dependencies
├── README.md              # Main project README
└── ORGANIZATION.md        # This file
```

---

## Before vs After

### Before (Disorganized)
- 47+ documentation files at root level
- Scattered repos and projects
- No clear separation of concerns
- External projects mixed with core code
- 30+ subdirectories with no organization

### After (Organized)
- 8 top-level directories with clear purposes
- All docs in `documentation/` with subcategories
- Core code separated from learning materials
- External projects isolated
- Clear navigation and discoverability

---

## Migration Notes

### What Was Moved

1. **Core Code** → `core/`
   - api/, frontend/, models/, config/, scripts/, templates/

2. **Agents** → `agents/`
   - agent-orchestrator/, specialized-agents/, alpha-engine/, etc.

3. **Data** → `data-storage/`
   - All data files consolidated

4. **Documentation** → `documentation/`
   - All .md and .txt files organized by category
   - guides/, status-reports/, setup/, reference/

5. **External Projects** → `external-projects/`
   - arrow/, tvm/, xgboost/

6. **Learning Materials** → `learning/`
   - karpathy repos, notebooks, tutorial projects

7. **Scripts** → `bin/`
   - All .sh executable scripts
   - Symlinks created for frequently used scripts

8. **Old Code** → `archive/`
   - newco-unified-platform/

### Path Updates Required

If you have hardcoded paths in code or scripts, update them:
- `scripts/` → `core/scripts/`
- `data/` → `data-storage/data/`
- `config/` → `core/config/`
- `docs/` → `documentation/`

Most scripts should use relative paths or environment variables, so minimal updates should be needed.

---

## Benefits of New Structure

### 1. **Clarity**
- Immediately clear what each directory contains
- No more hunting through 47 documentation files
- Core code vs external code clearly separated

### 2. **Maintainability**
- Easy to find and update files
- Related files grouped together
- Documentation organized by purpose

### 3. **Scalability**
- Clear places to add new code
- Room for growth in each category
- Won't become cluttered again

### 4. **Onboarding**
- New developers can navigate quickly
- Documentation hierarchy is clear
- Learning resources separated from core code

### 5. **Performance**
- Large external projects isolated (1.5GB+)
- Core application is smaller and faster to navigate
- Archive keeps old code without cluttering workspace

---

## Usage Tips

### For Daily Work
```bash
# Use the CLI
~/NEWCO/bin/newco contact list
~/NEWCO/bin/newco network analyze

# Run LinkedIn analysis
~/NEWCO/bin/run_full_network_analysis.sh

# Access scripts directly
cd ~/NEWCO/core/scripts
./newco_cli.py --help
```

### For Finding Documentation
```bash
# Quick starts and guides
ls ~/NEWCO/documentation/guides/

# Status reports
ls ~/NEWCO/documentation/status-reports/

# Technical reference
ls ~/NEWCO/documentation/reference/
```

### For Data Access
```bash
# Contacts
less ~/NEWCO/data-storage/data/contacts.csv

# LinkedIn data
ls ~/NEWCO/data-storage/data/linkedin_networks/

# Reports
ls ~/NEWCO/data-storage/reports/
```

---

## Future Organization

As the project grows, consider:
1. **tests/** - Unit and integration tests
2. **notebooks/** - Jupyter notebooks at root (if used frequently)
3. **deployment/** - Deployment configurations
4. **monitoring/** - Monitoring and logging configs

---

## Questions?

- See `README.md` for project overview
- See `CLAUDE.md` for AI assistant instructions
- See `documentation/guides/` for specific guides

---

Last Updated: February 14, 2026

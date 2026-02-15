# Co-Founder Quick Start Guide
## LinkedIn Network Analysis System for NEWCO

---

## 🎯 What This System Does

This system scrapes **Jason Eliot Goldman's LinkedIn network** (1st through 4th degree connections), imports it into NEWCO's contact system, and runs **social network analysis** to identify:

- **Network Multipliers** - 1 person who can open 10+ connections
- **Warm Introduction Paths** - How to reach anyone through your network
- **Structural Holes** - Access to non-overlapping networks
- **Brokers** - People who bridge different groups
- **Weak Ties** - Paradoxically more valuable than strong ties

**Based on academic research:** Granovetter (1973), Burt (1992), Freeman (1977), Bonacich (1987)

---

## 🚀 Run It (5 Minutes to Start)

### Step 1: Set Your LinkedIn Credentials

```bash
# Add these to your ~/.zshrc or ~/.bash_profile
export LINKEDIN_EMAIL="your@email.com"
export LINKEDIN_PASSWORD="yourpassword"

# Then reload
source ~/.zshrc  # or source ~/.bash_profile
```

### Step 2: Install Dependencies (One Time)

```bash
cd ~/NEWCO
pip install -r requirements.txt
playwright install chromium
```

### Step 3: Run the Full Pipeline

```bash
cd ~/NEWCO
./scripts/run_full_network_analysis.sh
```

**That's it!** The system will:
1. ✅ Login to LinkedIn (may need to complete 2FA in browser)
2. ✅ Find Jason Goldman's profile
3. ✅ Scrape his network (1st-4th degree connections)
4. ✅ Import all contacts into NEWCO
5. ✅ Run network analysis
6. ✅ Show you the top network multipliers, brokers, and insights

**Time:** 30-60 minutes (runs automatically)

---

## 📊 What You'll Get

### Network Data Imported
- **500-1000+ contacts** from LinkedIn
- **Complete relationship graph** showing who knows whom
- **Organized by tier** (Tier 1 = Jason, Tier 2 = 1st degree, etc.)
- **Categorized automatically** (VC Partner, Family Office CIO, Executive, etc.)

### Strategic Insights
```
🌟 TOP NETWORK MULTIPLIERS
1. Contact Name (Company) - Score: 0.87
   Why valuable: Bridges disconnected groups,
   Access to non-redundant networks

💎 STRUCTURAL HOLES ACCESS
1. Contact Name - Access: 0.82
   Non-redundant contacts: 45

🌉 TOP BROKERS
1. Contact Name - Broker Score: 0.76
   Bridges 23 otherwise disconnected pairs
```

### Files Created
- **`data/contacts.csv`** - All imported contacts
- **`data/relationships.csv`** - Who knows whom
- **`data/linkedin_networks/`** - Raw scraped data (JSON + CSV)
- **`reports/`** - Network analysis reports

---

## 💡 How to Use the Results

### 1. View Network Multipliers (Highest Priority)

```bash
cd ~/NEWCO
./scripts/newco_cli.py network multipliers
```

**Strategy:** Focus on top 10 multipliers first. These people can open entire networks with a single introduction.

### 2. Find Warm Introduction Paths

```bash
# Find how to reach someone through your network
./scripts/newco_cli.py relationship intro-path <contact_id>
```

**Output:** You → Connector → Target

**Why it works:** 30-50% response rate (vs 1-3% cold email)

### 3. Generate Personalized Outreach

```bash
# Generate email using network multiplier template
./scripts/newco_cli.py email generate <contact_id> --template network_multiplier
```

### 4. View All Contacts

```bash
# List all contacts
./scripts/newco_cli.py contact list

# Filter by tier
./scripts/newco_cli.py contact list --tier 2

# Search
./scripts/newco_cli.py contact search "Goldman"
```

### 5. View Dashboard

```bash
./scripts/newco_cli.py report dashboard
```

---

## 📚 Key Concepts (2-Minute Primer)

### Network Multipliers
**What:** Contacts who have high betweenness, structural holes access, AND network influence

**Why:** 1 network multiplier = 10+ individual contacts in leverage

**Action:** Prioritize these for outreach first

### Weak Ties (Granovetter 1973)
**Paradox:** Weak ties are MORE valuable than strong ties for opportunities

**Research:** 73% of jobs found through weak ties, not close friends

**Why:** Close friends have redundant information. Weak ties bridge to NEW networks.

**Action:** Don't ignore 2nd/3rd degree connections!

### Structural Holes (Burt 1992)
**Theory:** "People near holes in social structure have higher risk of good ideas"

**What:** Gaps between disconnected groups in a network

**Why:** Access to non-redundant, non-overlapping information = competitive advantage

**Action:** Seek positions that span different communities

### Brokers / Betweenness Centrality
**What:** People who lie on paths between other people

**Why:** Gatekeepers who control information flow between groups

**Action:** Ask brokers for strategic introductions

---

## 🎯 90-Day GTM Strategy Integration

### Week 1-2: Network Multiplier Activation
```bash
./scripts/newco_cli.py network multipliers
```
- Focus on top 5-10 multipliers
- Highly personalized outreach
- Ask for 2-3 specific introductions

### Week 3-4: Leverage Weak Ties
```bash
./scripts/newco_cli.py contact list --tier 2,3
```
- Reach out to 2nd/3rd degree connections
- Use warm intro paths
- Mention mutual connections

### Week 5-6: Bridge Structural Holes
```bash
./scripts/newco_cli.py relationship opportunities
```
- Make strategic introductions
- Connect your network
- Build social capital

---

## 🔧 Troubleshooting

### "LinkedIn credentials not set"
```bash
export LINKEDIN_EMAIL="your@email.com"
export LINKEDIN_PASSWORD="yourpassword"
```

### "Playwright not installed"
```bash
pip install playwright
playwright install chromium
```

### "Login failed" or 2FA Required
- Browser window will open automatically
- Complete 2FA verification in the browser
- Press Enter when done
- System will continue

### "Could not find Jason Goldman's profile"
- System will prompt you to enter LinkedIn URL manually
- Go to LinkedIn, search for Jason Goldman, copy URL
- Paste into terminal when prompted

### "Too many requests"
- LinkedIn rate limiting detected
- Wait 24 hours before retrying
- Or reduce `max_connections_per_profile` in `linkedin_network_crawler.py`

---

## 📖 Documentation

### Complete Guides
1. **`LINKEDIN_NETWORK_ANALYSIS_GUIDE.md`** - 200+ line complete guide
   - Academic theory explained in detail
   - Practical applications
   - Advanced analysis
   - Further reading

2. **`docs/NETWORK_ANALYSIS_GUIDE.md`** - Network effects theory
   - All social network concepts
   - Metrics explained
   - Strategic applications

3. **`docs/PLAYBOOK.md`** - Daily operational workflows
   - Morning routines
   - Email generation
   - Activity logging

4. **`docs/90_Day_Plan.md`** - Week-by-week GTM execution
   - Detailed weekly breakdown
   - Target contacts
   - Sample email sequences

### CLI Help
```bash
./scripts/newco_cli.py --help
./scripts/newco_cli.py network --help
./scripts/newco_cli.py relationship --help
```

---

## 🎬 Demo / Test First

Want to test before running the full crawl?

### Option 1: Run Demo Network
```bash
cd ~/NEWCO
python3 scripts/demo_network.py
python3 scripts/network_analysis.py
```
This builds a sample network to see the analysis in action.

### Option 2: Start with 2 Degrees (Faster)
Edit `scripts/linkedin_network_crawler.py` line ~423:
```python
max_degrees=2,  # Change from 4 to 2 for testing (10-15 min)
```

Then run the full pipeline.

---

## 🚨 Important Notes

### LinkedIn Terms of Service
- ✅ Use responsibly for personal network analysis
- ✅ Built-in rate limiting and respectful delays
- ✅ Personal use only (not commercial data collection)
- ⚠️ Don't scrape at scale or sell data

### Privacy & Ethics
- Only scrapes **public profile information**
- Respects LinkedIn's visibility settings
- Use insights for **relationship building**, not manipulation
- Don't share scraped data publicly

### What Gets Scraped
- ✅ Profile: Name, title, company, location, headline
- ✅ Experience: Work history
- ✅ Education: Schools and degrees
- ✅ Connections: Visible 1st-degree connections
- ❌ Email addresses (not public)
- ❌ Private messages
- ❌ Private profiles (respects privacy settings)

---

## 💬 Questions?

### Where is everything?
```
~/NEWCO/
├── scripts/
│   ├── linkedin_scraper.py           # Profile scraper
│   ├── linkedin_network_crawler.py   # Multi-degree crawler
│   ├── import_linkedin_network.py    # Import to NEWCO
│   ├── network_analysis.py           # Analysis engine
│   └── run_full_network_analysis.sh  # Run everything
├── data/
│   ├── contacts.csv                  # Imported contacts
│   ├── relationships.csv             # Relationship graph
│   └── linkedin_networks/            # Scraped data
├── docs/
│   ├── NETWORK_ANALYSIS_GUIDE.md
│   ├── PLAYBOOK.md
│   └── 90_Day_Plan.md
└── LINKEDIN_NETWORK_ANALYSIS_GUIDE.md  # Complete guide
```

### How do I re-run later?
```bash
cd ~/NEWCO
./scripts/run_full_network_analysis.sh
```

Network data is cached, so re-scraping will only fetch new connections.

### How do I scrape someone else's network?
Edit `scripts/linkedin_network_crawler.py` line ~410:
```python
# Change search parameters
profile_url = await scraper.search_person("Other Person", "Their Company")
```

Or provide URL directly.

---

## ✅ Success Metrics

### Network Analysis
- **500-1000+ contacts** mapped
- **10-20 network multipliers** identified
- **50-100 warm intro paths** found

### GTM Conversion
- **30-50%** warm intro response rate (vs 1-3% cold)
- **2-3x faster** time to meeting
- **10x leverage** through multipliers

### Network Effects
- Access to **non-redundant information**
- **Novel opportunities** through weak ties
- **Broker positions** for influence

---

## 🎯 Next Steps

1. **Run the system:**
   ```bash
   ./scripts/run_full_network_analysis.sh
   ```

2. **Review results:**
   ```bash
   ./scripts/newco_cli.py network multipliers
   ```

3. **Prioritize outreach:**
   - Focus on top 10 multipliers
   - Find warm intro paths
   - Generate personalized emails

4. **Execute GTM plan:**
   - Follow `docs/90_Day_Plan.md`
   - Track in pipeline
   - Iterate based on results

---

**Questions? See:**
- `LINKEDIN_NETWORK_ANALYSIS_GUIDE.md` - Complete technical guide
- `docs/PLAYBOOK.md` - Daily workflows
- `README.md` - System overview

**Built for NEWCO Fund I - Network Effects-Driven GTM**

Last Updated: February 14, 2026

# Standalone Alpha Engine - Quick Start ✓

## What I Created

A simplified, standalone version of the NEWCO V10 Alpha Engine that:

✅ **Works immediately** - No setup, dependencies, or configuration
✅ **Uses your real data** - Connects to Flask API on port 5001
✅ **Live integration** - Fetches your 85 funds + 62 portfolio companies
✅ **Professional UI** - Alpha Engine design system (dark theme, institutional look)
✅ **Instant view** - Opens directly in browser

---

## Access It

**File Location:**
```
/Users/rufio/NEWCO/frontend/alpha-standalone.html
```

**Or open in browser:**
```bash
open /Users/rufio/NEWCO/frontend/alpha-standalone.html
```

**Should already be open** - I just opened it for you!

---

## What It Shows

### **Intelligence LP Dashboard**

**Portfolio Overview Stats:**
- Total Commitments (from your 85 funds)
- Called Capital (with deployment %)
- Current NAV (with average TVPI)
- Portfolio Reach (your 62 companies)

**Top Performing Funds Table:**
- Your 10 best-performing funds by TVPI
- Shows: Fund name, GP, TVPI, DPI, NAV, Sector
- Sorted by performance
- Interactive hover effects

**Portfolio Companies Table:**
- Your first 15 portfolio companies
- Shows: Company, Sector, Stage, Fund, Status
- Color-coded status badges
- Clean, professional layout

---

## How It Works

### **Data Adapter**

Automatically transforms your data:

**Your Flask API → Alpha Engine Format:**
```javascript
// Fetches from:
http://localhost:5001/api/portfolio/funds
http://localhost:5001/api/portfolio-companies

// Transforms to AlphaEngine format:
- Converts dollars to millions
- Maps fund types to tiers
- Calculates display metrics
- Formats portfolio companies
```

### **Real-Time Data**

- Loads on page load
- No refresh needed
- Instant visualization
- Live connection to your API

---

## Design System

**Professional Alpha Engine Theme:**
- Background: `#06090f` (deep blue-black)
- Cards: `#0c1018` (elevated surfaces)
- Accent: `#00e4b8` (electric cyan)
- Clean, institutional look
- Smooth hover interactions

**Typography:**
- Sans: 'DM Sans', 'Inter'
- Mono: 'JetBrains Mono', 'SF Mono'

---

## Features Included

✓ **Stat Cards** - Four key metrics with color coding
✓ **Performance Table** - Top 10 funds sorted by TVPI
✓ **Company Table** - First 15 portfolio companies
✓ **Hover Effects** - Interactive table rows
✓ **Color-Coded Status** - Visual performance indicators
✓ **Responsive Layout** - Grid-based stat cards
✓ **Professional Design** - Alpha Engine aesthetic

---

## What's Different from Full Alpha Engine

| Feature | Full Alpha Engine | Standalone Version |
|---------|------------------|-------------------|
| **Views** | 30+ views | 1 dashboard view |
| **Lines of Code** | 15,124 | ~500 |
| **Setup** | RedwoodJS + Supabase | None - just open |
| **Dependencies** | yarn install | None - CDN loaded |
| **Data Source** | GraphQL + Supabase | Flask API (port 5001) |
| **Visualizations** | D3 force graphs, etc. | Tables + stat cards |
| **Analytics** | Monte Carlo, Kelly | Basic metrics |

**Trade-off:** Simpler, but works immediately with your data!

---

## Adding More Views

To add more Alpha Engine features:

### **Option A: Extract from Full AlphaEngine**
```bash
# Full component is at:
/Users/rufio/NEWCO/alpha-engine/src/components/AlphaEngine.jsx

# Contains 30+ views you can extract:
- Morning Pulse
- Deal Radar
- IC Memo Generator
- Monte Carlo Simulator
- NAV Marks
- IPO Watch
- Network Graph (D3)
- And 20+ more...
```

### **Option B: Copy specific views**
I can extract individual views from the full AlphaEngine and add them to the standalone version. Just tell me which ones you want:
- Fund comparison?
- Portfolio planner?
- Network visualization?
- Monte Carlo simulator?

---

## Requirements

**Must be running:**
- ✅ Flask API server on port 5001
- ✅ `http://localhost:5001/api/portfolio/funds` working
- ✅ `http://localhost:5001/api/portfolio-companies` working

**If API is down:**
```bash
cd /Users/rufio/NEWCO
python3 api/server.py
```

---

## Next Steps

### **To add more data:**
Edit the data adapter in `alpha-standalone.html`:
- Add more API endpoints
- Transform additional fields
- Include calculated metrics

### **To add more views:**
Let me know which Alpha Engine views you want, and I'll extract them from the full 15,124-line component.

### **To use full Alpha Engine:**
Follow the setup in:
```
/Users/rufio/NEWCO/ALPHA_ENGINE_INTEGRATION_GUIDE.md
```

---

## Summary

You now have a **working Alpha Engine dashboard** showing:

✅ Your real 85 funds
✅ Your real 62 portfolio companies
✅ Performance metrics (TVPI, DPI, NAV)
✅ Professional Alpha Engine design
✅ Works immediately - no setup

**It's already open in your browser!**

The full NEWCO V10 platform (30+ views, 15,124 lines) is available at `/Users/rufio/NEWCO/alpha-engine/` when you're ready to set it up.

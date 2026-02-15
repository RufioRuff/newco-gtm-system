#!/bin/bash
#
# Full LinkedIn Network Analysis Pipeline for NEWCO
#
# This script orchestrates the complete workflow:
# 1. Scrape Jason Goldman's LinkedIn profile and multi-degree network
# 2. Import the network data into NEWCO's contact and relationship system
# 3. Run comprehensive network effects analysis
# 4. Generate actionable insights and recommendations
#

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║    LinkedIn Network Analysis Pipeline for NEWCO             ║"
echo "║           Full Network Effects Engine                        ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check environment variables
if [ -z "$LINKEDIN_EMAIL" ] || [ -z "$LINKEDIN_PASSWORD" ]; then
    echo "❌ Error: LinkedIn credentials not set"
    echo ""
    echo "Please set environment variables:"
    echo "  export LINKEDIN_EMAIL=\"your@email.com\""
    echo "  export LINKEDIN_PASSWORD=\"yourpassword\""
    echo ""
    exit 1
fi

echo "✅ LinkedIn credentials found"
echo ""

# Check if Playwright is installed
if ! python3 -c "import playwright" 2>/dev/null; then
    echo "📦 Installing Playwright..."
    pip install playwright
    playwright install chromium
    echo "✅ Playwright installed"
    echo ""
fi

# Step 1: Scrape LinkedIn Network
echo "════════════════════════════════════════════════════════════════"
echo "STEP 1: SCRAPE LINKEDIN NETWORK"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "This will scrape Jason Goldman's LinkedIn profile and network"
echo "(up to 4 degrees of separation)"
echo ""
echo "⚠️  This may take 30-60 minutes depending on network size"
echo ""
read -p "Press Enter to start scraping (Ctrl+C to cancel)..."
echo ""

python3 scripts/linkedin_network_crawler.py

echo ""
echo "✅ Step 1 complete: Network scraped"
echo ""

# Step 2: Import Network Data
echo "════════════════════════════════════════════════════════════════"
echo "STEP 2: IMPORT NETWORK INTO NEWCO"
echo "════════════════════════════════════════════════════════════════"
echo ""

python3 scripts/import_linkedin_network.py

echo ""
echo "✅ Step 2 complete: Network imported"
echo ""

# Step 3: Run Comprehensive Analysis
echo "════════════════════════════════════════════════════════════════"
echo "STEP 3: COMPREHENSIVE NETWORK ANALYSIS"
echo "════════════════════════════════════════════════════════════════"
echo ""

python3 scripts/network_analysis.py

echo ""
echo "✅ Step 3 complete: Analysis complete"
echo ""

# Step 4: Generate Reports
echo "════════════════════════════════════════════════════════════════"
echo "STEP 4: GENERATE INSIGHTS"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Find network multipliers
echo "🌟 TOP NETWORK MULTIPLIERS:"
echo "─────────────────────────────────────────────────────────────────"
python3 -c "
from scripts.network_analysis import NetworkAnalysisEngine
engine = NetworkAnalysisEngine()
multipliers = engine.identify_network_multipliers()
for i, m in enumerate(multipliers[:5], 1):
    print(f'{i}. {m[\"name\"]} ({m[\"company\"]}) - Score: {m[\"multiplier_score\"]:.2f}')
    print(f'   {m[\"why_valuable\"]}')
    print()
"

echo ""
echo "🌉 TOP BROKERS (Bridge Different Networks):"
echo "─────────────────────────────────────────────────────────────────"
python3 -c "
from scripts.network_analysis import NetworkAnalysisEngine
engine = NetworkAnalysisEngine()
brokers = engine.calculate_betweenness_centrality()
for i, b in enumerate(brokers[:5], 1):
    print(f'{i}. {b[\"name\"]} ({b[\"company\"]}) - Broker Score: {b[\"broker_score\"]:.2f}')
"

echo ""
echo "💎 STRUCTURAL HOLES ACCESS (Non-Redundant Networks):"
echo "─────────────────────────────────────────────────────────────────"
python3 -c "
from scripts.network_analysis import NetworkAnalysisEngine
engine = NetworkAnalysisEngine()
holes = engine.calculate_structural_holes()
for i, h in enumerate(holes[:5], 1):
    print(f'{i}. {h[\"name\"]} ({h[\"company\"]}) - Access: {h[\"structural_holes_access\"]:.2f}')
"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ PIPELINE COMPLETE"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Your LinkedIn network has been fully analyzed!"
echo ""
echo "📊 Data Location:"
echo "   Contacts: data/contacts.csv"
echo "   Relationships: data/relationships.csv"
echo "   Network files: data/linkedin_networks/"
echo ""
echo "🚀 Next Steps:"
echo "   1. Review top network multipliers above"
echo "   2. Identify warm introduction paths:"
echo "      ./scripts/newco_cli.py relationship intro-path <contact_id>"
echo "   3. Generate personalized outreach emails:"
echo "      ./scripts/newco_cli.py email generate <contact_id>"
echo "   4. Track outreach in pipeline:"
echo "      ./scripts/newco_cli.py pipeline show"
echo ""
echo "📈 Network Effects Insights:"
echo "   • Focus on network multipliers for maximum leverage"
echo "   • Use brokers to access disconnected networks"
echo "   • Leverage structural hole positions for novel opportunities"
echo "   • Weak ties (2nd/3rd degree) often more valuable than strong ties"
echo ""
echo "For detailed guidance, see docs/NETWORK_ANALYSIS_GUIDE.md"
echo ""

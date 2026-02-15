#!/bin/bash
#
# NEWCO EXECUTE NOW - Quick Start Integration
#
# This script sets up the essentials to get NEWCO running with all integrations
#

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║              NEWCO INTEGRATION EXECUTION                     ║"
echo "║         LinkedIn + Supabase + GitHub + LLMs                  ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Navigate to NEWCO directory
cd ~/NEWCO

echo "📋 Pre-flight Checklist..."
echo ""

# Check prerequisites
MISSING_DEPS=0

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Install from https://nodejs.org"
    MISSING_DEPS=1
else
    echo "✅ Node.js $(node --version)"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    MISSING_DEPS=1
else
    echo "✅ Python $(python3 --version)"
fi

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found (optional for local dev)"
else
    echo "✅ PostgreSQL installed"
fi

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found (optional for local LLMs)"
    echo "   Install from https://ollama.ai"
else
    echo "✅ Ollama installed"
fi

if [ $MISSING_DEPS -eq 1 ]; then
    echo ""
    echo "❌ Missing required dependencies. Please install and try again."
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "STEP 1: SETUP LINKEDIN NETWORK ANALYSIS"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check if credentials are set
if [ -z "$LINKEDIN_EMAIL" ] || [ -z "$LINKEDIN_PASSWORD" ]; then
    echo "⚠️  LinkedIn credentials not set"
    echo ""
    echo "Please set environment variables:"
    echo "  export LINKEDIN_EMAIL=\"your@email.com\""
    echo "  export LINKEDIN_PASSWORD=\"yourpassword\""
    echo ""
    read -p "Press Enter to continue (will skip LinkedIn scraping for now)..."
else
    echo "✅ LinkedIn credentials found"
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
cd ~/NEWCO
pip3 install -r requirements.txt

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "STEP 2: SETUP UNIFIED PLATFORM"
echo "════════════════════════════════════════════════════════════════"
echo ""

cd ~/NEWCO/newco-unified-platform

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node dependencies (this may take a few minutes)..."
    yarn install
else
    echo "✅ Node dependencies already installed"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "STEP 3: DATABASE SETUP"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check if Supabase is configured
if [ -z "$SUPABASE_URL" ]; then
    echo "⚠️  Supabase not configured"
    echo ""
    echo "Option 1: Use Supabase Cloud"
    echo "  1. Go to https://app.supabase.com"
    echo "  2. Create a new project"
    echo "  3. Get your connection details"
    echo "  4. Set environment variables:"
    echo "     export SUPABASE_URL=\"https://xxx.supabase.co\""
    echo "     export SUPABASE_ANON_KEY=\"your-anon-key\""
    echo "     export DATABASE_URL=\"postgresql://...\""
    echo ""
    echo "Option 2: Use Local PostgreSQL"
    echo "  1. Create local database: createdb newco_dev"
    echo "  2. Set: export DATABASE_URL=\"postgresql://localhost/newco_dev\""
    echo ""
    read -p "Press Enter when ready (or skip for now)..."
    echo ""
else
    echo "✅ Supabase configured: $SUPABASE_URL"
    echo ""
    echo "🔧 Applying database migrations..."

    # Apply migrations
    if [ -n "$DATABASE_URL" ]; then
        psql "$DATABASE_URL" < api/db/migrations/20260214_network_analysis.sql
        echo "✅ Migrations applied successfully"
    else
        echo "⚠️  DATABASE_URL not set, skipping migrations"
    fi
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "STEP 4: GITHUB SETUP (OPTIONAL)"
echo "════════════════════════════════════════════════════════════════"
echo ""

if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI not found"
    echo "   Install: brew install gh"
    echo "   Then run: gh auth login"
else
    echo "✅ GitHub CLI installed"
    echo ""
    read -p "Create GitHub repository? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd ~/NEWCO
        if [ ! -d ".git" ]; then
            git init
            git add .
            git commit -m "Initial commit: NEWCO unified platform with network analysis"
        fi

        echo "Creating GitHub repository..."
        gh repo create newco-platform --private --source=. --remote=origin --push
        echo "✅ Repository created and pushed to GitHub"
    fi
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "STEP 5: LOCAL LLM SETUP (OPTIONAL)"
echo "════════════════════════════════════════════════════════════════"
echo ""

if command -v ollama &> /dev/null; then
    echo "✅ Ollama found"
    echo ""
    read -p "Download LLM models? (y/n) (This will download ~10GB) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📥 Downloading models..."
        echo ""
        echo "1/3 Downloading Llama 3.1 8B (fastest, 4.7GB)..."
        ollama pull llama3.1:8b

        echo ""
        echo "2/3 Downloading Mistral 7B (4.1GB)..."
        ollama pull mistral:7b

        echo ""
        echo "3/3 Downloading CodeLlama 13B (7.4GB)..."
        ollama pull codellama:13b

        echo ""
        echo "✅ Models downloaded"
        echo ""
        echo "Additional models you can download:"
        echo "  ollama pull llama3.1:70b    # Most capable, large (40GB)"
        echo "  ollama pull deepseek-coder:6.7b  # Code generation"
        echo "  ollama pull nomic-embed-text     # Embeddings"
    fi
else
    echo "⚠️  Ollama not installed"
    echo "   Install from: https://ollama.ai"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "STEP 6: START DEVELOPMENT SERVER"
echo "════════════════════════════════════════════════════════════════"
echo ""

cd ~/NEWCO/newco-unified-platform

echo "Starting RedwoodJS development server..."
echo ""
echo "Access points:"
echo "  Frontend: http://localhost:8910"
echo "  GraphQL: http://localhost:8911/graphql"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start in background with logging
yarn rw dev > ~/NEWCO/logs/dev-server.log 2>&1 &
DEV_SERVER_PID=$!

echo "✅ Development server started (PID: $DEV_SERVER_PID)"
echo "   Logs: ~/NEWCO/logs/dev-server.log"
echo ""
echo "To view logs: tail -f ~/NEWCO/logs/dev-server.log"
echo "To stop: kill $DEV_SERVER_PID"
echo ""

# If Ollama is running, start LLM orchestrator
if command -v ollama &> /dev/null; then
    if pgrep -x "ollama" > /dev/null; then
        echo "✅ Ollama is running"
        echo "   Access: http://localhost:11434"
    else
        echo "⚠️  Ollama not running. Start with: ollama serve"
    fi
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ SETUP COMPLETE!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🎯 What's Running:"
echo "   ✅ NEWCO Unified Platform: http://localhost:8910"
echo "   ✅ GraphQL API: http://localhost:8911/graphql"
if command -v ollama &> /dev/null && pgrep -x "ollama" > /dev/null; then
    echo "   ✅ Ollama LLMs: http://localhost:11434"
fi
echo ""
echo "📚 Next Steps:"
echo "   1. Open http://localhost:8910 in your browser"
echo "   2. Navigate to Network Analysis section"
echo "   3. Start LinkedIn scraping:"
echo "      cd ~/NEWCO && ./scripts/run_full_network_analysis.sh"
echo "   4. Read documentation:"
echo "      - MASTER_INTEGRATION_PLAN.md (complete plan)"
echo "      - START_HERE.md (quick overview)"
echo "      - CO_FOUNDER_QUICK_START.md (for co-founder)"
echo ""
echo "🚀 To run LinkedIn network analysis:"
echo "   cd ~/NEWCO"
echo "   export LINKEDIN_EMAIL=\"your@email.com\""
echo "   export LINKEDIN_PASSWORD=\"yourpassword\""
echo "   ./scripts/run_full_network_analysis.sh"
echo ""
echo "🤖 To test LLM integration:"
echo "   ollama run llama3.1:8b"
echo "   > Analyze this contact's network position..."
echo ""
echo "📖 Full Documentation:"
echo "   ~/NEWCO/MASTER_INTEGRATION_PLAN.md"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Happy building! 🎉"
echo ""

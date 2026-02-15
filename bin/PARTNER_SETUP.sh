#!/bin/bash
# NEWCO Partner Setup Script
# ==========================
# Easy one-command setup for your co-founder

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              NEWCO COMPLETE SETUP FOR PARTNER                ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "This script will set up all NEWCO agents on your machine."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo -e "${BLUE}[1/8]${NC} Checking prerequisites..."
echo ""

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
    echo -e "${GREEN}✓${NC} Python 3 installed: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check Homebrew
if command_exists brew; then
    echo -e "${GREEN}✓${NC} Homebrew installed"
else
    echo -e "${YELLOW}⚠${NC} Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

echo ""
echo -e "${BLUE}[2/8]${NC} Installing Ollama (Local LLM Server)..."
echo ""

if command_exists ollama; then
    echo -e "${GREEN}✓${NC} Ollama already installed"
else
    brew install ollama
    echo -e "${GREEN}✓${NC} Ollama installed"
fi

# Start Ollama
echo "Starting Ollama server..."
pgrep -x "ollama" > /dev/null || ollama serve > /tmp/ollama_setup.log 2>&1 &
sleep 3
echo -e "${GREEN}✓${NC} Ollama running"

echo ""
echo -e "${BLUE}[3/8]${NC} Downloading Local LLM Models (this may take 15-30 minutes)..."
echo ""

# Essential models for NEWCO
models=(
    "deepseek-r1:latest"
    "phi4:latest"
    "qwen2.5:14b"
    "codellama:latest"
    "mistral:latest"
    "llama3.2:latest"
    "deepseek-coder:latest"
)

for model in "${models[@]}"; do
    echo "Downloading $model..."
    ollama pull $model
    echo -e "${GREEN}✓${NC} $model ready"
done

echo ""
echo -e "${BLUE}[4/8]${NC} Installing Python dependencies..."
echo ""

pip3 install flask flask-cors requests xgboost scikit-learn pandas numpy --quiet
echo -e "${GREEN}✓${NC} Python packages installed"

echo ""
echo -e "${BLUE}[5/8]${NC} Installing git (if needed)..."
echo ""

if command_exists git; then
    echo -e "${GREEN}✓${NC} Git already installed"
else
    brew install git
    echo -e "${GREEN}✓${NC} Git installed"
fi

echo ""
echo -e "${BLUE}[6/8]${NC} Cloning NEWCO repository from GitHub..."
echo ""

# Create NEWCO directory if it doesn't exist
mkdir -p ~/NEWCO
cd ~/NEWCO

# Clone or pull latest
if [ -d ".git" ]; then
    echo "Repository exists, pulling latest changes..."
    git pull origin main
    echo -e "${GREEN}✓${NC} Repository updated"
else
    echo "Enter GitHub repository URL:"
    read -r REPO_URL
    git clone "$REPO_URL" .
    echo -e "${GREEN}✓${NC} Repository cloned"
fi

echo ""
echo -e "${BLUE}[7/8]${NC} Configuring 24/7 operation..."
echo ""

echo "To run agents 24/7, you need to prevent sleep. Run these commands:"
echo ""
echo -e "${YELLOW}sudo pmset -a displaysleep 0 sleep 0 disksleep 0${NC}"
echo -e "${YELLOW}sudo pmset -a womp 1${NC}"
echo -e "${YELLOW}sudo systemsetup -setcomputersleep Never${NC}"
echo ""
read -p "Run these commands now? (requires password) [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo pmset -a displaysleep 0 sleep 0 disksleep 0
    sudo pmset -a womp 1
    sudo systemsetup -setcomputersleep Never
    echo -e "${GREEN}✓${NC} 24/7 mode configured"
else
    echo "⏭  Skipped - you can run these commands later"
fi

echo ""
echo -e "${BLUE}[8/8]${NC} Setting up Supabase integration..."
echo ""

# Create Supabase config template
cat > ~/NEWCO/.env << 'EOF'
# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=RufioRuff/newco-learning-projects

# Email Configuration
EMAIL_ADDRESS=rufioruff@icloud.com
EOF

echo -e "${GREEN}✓${NC} Configuration template created at ~/NEWCO/.env"
echo ""
echo -e "${YELLOW}⚠${NC} Please edit ~/NEWCO/.env with your Supabase and GitHub credentials"

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    SETUP COMPLETE! 🎉                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 What's Installed:"
echo "   ✓ Ollama (Local LLM server)"
echo "   ✓ 7 Local LLM models (33 GB)"
echo "   ✓ All Python dependencies"
echo "   ✓ NEWCO repository"
echo "   ✓ Configuration templates"
echo ""
echo "🚀 Next Steps:"
echo ""
echo "1. Edit configuration:"
echo "   nano ~/NEWCO/.env"
echo ""
echo "2. Start all agents:"
echo "   cd ~/NEWCO/agent-orchestrator"
echo "   ./start_all_agents.sh"
echo ""
echo "3. Start specialized PE agents:"
echo "   cd ~/NEWCO/specialized-agents"
echo "   ./START_ALL_SPECIALIZED_AGENTS.sh"
echo ""
echo "4. Monitor agents:"
echo "   cd ~/NEWCO/agent-orchestrator"
echo "   ./monitor_agents.sh"
echo ""
echo "5. View daily summary:"
echo "   cat ~/NEWCO/daily_summaries/summary_*.txt"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "For help: Check ~/NEWCO/FINAL_SUMMARY.txt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

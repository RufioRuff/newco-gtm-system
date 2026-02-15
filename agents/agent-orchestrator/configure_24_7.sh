#!/bin/bash
# NEWCO 24/7 Mac Mini Configuration
# ===================================
# Run this to configure Mac mini for continuous operation

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         NEWCO 24/7 MAC MINI CONFIGURATION                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "⚠️  This script requires sudo password to configure power settings"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}❌ Do not run this script as root/sudo${NC}"
    echo "Run it normally - it will ask for password when needed"
    exit 1
fi

echo -e "${BLUE}[1/6]${NC} Current power settings:"
echo ""
pmset -g
echo ""

read -p "Continue with 24/7 configuration? [y/N]: " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo -e "${BLUE}[2/6]${NC} Disabling all sleep modes..."
echo ""

# Disable display sleep
sudo pmset -a displaysleep 0
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Display sleep disabled"
else
    echo -e "${RED}✗${NC} Failed to disable display sleep"
    exit 1
fi

# Disable system sleep
sudo pmset -a sleep 0
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} System sleep disabled"
else
    echo -e "${RED}✗${NC} Failed to disable system sleep"
    exit 1
fi

# Disable disk sleep
sudo pmset -a disksleep 0
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Disk sleep disabled"
else
    echo -e "${RED}✗${NC} Failed to disable disk sleep"
    exit 1
fi

echo ""
echo -e "${BLUE}[3/6]${NC} Enabling Wake-on-LAN..."
echo ""

# Enable wake on network access
sudo pmset -a womp 1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Wake-on-LAN enabled"
else
    echo -e "${YELLOW}⚠${NC} Wake-on-LAN may not be supported on this Mac"
fi

echo ""
echo -e "${BLUE}[4/6]${NC} Setting computer sleep to Never..."
echo ""

# Set computer sleep to never
sudo systemsetup -setcomputersleep Never
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Computer sleep set to Never"
else
    echo -e "${RED}✗${NC} Failed to set computer sleep"
    exit 1
fi

echo ""
echo -e "${BLUE}[5/6]${NC} Configuring automatic restart after power failure..."
echo ""

# Enable automatic restart after power failure
sudo systemsetup -setrestartpowerfailure on
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Automatic restart enabled"
else
    echo -e "${YELLOW}⚠${NC} Could not enable automatic restart"
fi

echo ""
echo -e "${BLUE}[6/6]${NC} Verifying configuration..."
echo ""

# Show final settings
echo "Power Settings:"
pmset -g | grep -E "sleep|womp"
echo ""

echo "System Settings:"
sudo systemsetup -getcomputersleep
sudo systemsetup -getrestartpowerfailure
echo ""

# Create verification script
cat > /Users/rufio/NEWCO/agent-orchestrator/verify_24_7.sh << 'VERIFY_EOF'
#!/bin/bash
# Verify 24/7 configuration

echo "24/7 Configuration Status:"
echo "=========================="
echo ""

echo "Power Management:"
pmset -g | grep -E "sleep|womp"
echo ""

echo "Computer Sleep Setting:"
sudo systemsetup -getcomputersleep
echo ""

echo "Auto-Restart After Power Failure:"
sudo systemsetup -getrestartpowerfailure
echo ""

# Check if agents are running
echo "Agent Status:"
agent_count=0
for port in {8001..8010} {9001..9007}; do
    if nc -z localhost $port 2>/dev/null; then
        echo "✓ Port $port: Running"
        ((agent_count++))
    fi
done
echo ""
echo "Total agents running: $agent_count/17"
echo ""

# Check Ollama
if pgrep -x "ollama" > /dev/null; then
    echo "✓ Ollama: Running"
else
    echo "✗ Ollama: Not running"
fi
echo ""

# Check uptime
echo "System Uptime:"
uptime
VERIFY_EOF

chmod +x /Users/rufio/NEWCO/agent-orchestrator/verify_24_7.sh

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                 CONFIGURATION COMPLETE! ✅                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "24/7 Settings Applied:"
echo "  ✓ Display sleep: DISABLED"
echo "  ✓ System sleep: DISABLED"
echo "  ✓ Disk sleep: DISABLED"
echo "  ✓ Computer sleep: NEVER"
echo "  ✓ Wake-on-LAN: ENABLED"
echo "  ✓ Auto-restart after power failure: ENABLED"
echo ""
echo "Next Steps:"
echo ""
echo "1. Start all agents:"
echo "   cd /Users/rufio/NEWCO/agent-orchestrator && ./start_all_agents.sh"
echo ""
echo "2. Verify 24/7 status anytime:"
echo "   ./verify_24_7.sh"
echo ""
echo "3. Keep Mac mini:"
echo "   • Plugged into power"
echo "   • Connected to ethernet (more reliable than WiFi)"
echo "   • In a ventilated area"
echo ""
echo "To revert to normal power settings:"
echo "   sudo pmset -a displaysleep 10 sleep 10 disksleep 10"
echo "   sudo systemsetup -setcomputersleep 10"
echo ""
echo "✨ Your Mac mini is now configured for 24/7 operation!"

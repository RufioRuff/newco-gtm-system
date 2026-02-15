#!/bin/bash
#
# NEWCO Quick Launch Script
# Simplified launcher for the complete NEWCO system
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Navigate to NEWCO directory
cd ~/NEWCO

echo ""
echo "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo "${BOLD}║                                                              ║${NC}"
echo "${BOLD}║                     NEWCO QUICK LAUNCH                       ║${NC}"
echo "${BOLD}║              Network Analysis & GTM Platform                 ║${NC}"
echo "${BOLD}║                                                              ║${NC}"
echo "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Quick validation
echo "${BLUE}🔍 Running quick validation...${NC}"
if python3 validate_integration.py > /tmp/newco_validation.log 2>&1; then
    echo "${GREEN}✅ System validation passed${NC}"
else
    echo "${RED}❌ System validation failed. See /tmp/newco_validation.log${NC}"
    echo ""
    echo "Run this for full validation output:"
    echo "  python3 validate_integration.py"
    exit 1
fi

echo ""
echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
echo "${BOLD}SELECT WHAT TO LAUNCH${NC}"
echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "  ${BOLD}1)${NC} LinkedIn Network Analysis (Python scripts only)"
echo "  ${BOLD}2)${NC} Unified Platform (RedwoodJS web app)"
echo "  ${BOLD}3)${NC} Full System (LinkedIn + Platform)"
echo "  ${BOLD}4)${NC} Validation Report Only"
echo "  ${BOLD}5)${NC} Setup Guide"
echo ""
read -p "${BOLD}Choose option [1-5]:${NC} " choice

case $choice in
    1)
        echo ""
        echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
        echo "${BOLD}LINKEDIN NETWORK ANALYSIS${NC}"
        echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
        echo ""

        # Check credentials
        if [ -z "$LINKEDIN_EMAIL" ] || [ -z "$LINKEDIN_PASSWORD" ]; then
            echo "${YELLOW}⚠️  LinkedIn credentials not set${NC}"
            echo ""
            echo "To set credentials:"
            echo "  export LINKEDIN_EMAIL='your@email.com'"
            echo "  export LINKEDIN_PASSWORD='yourpassword'"
            echo ""
            echo "Add to ~/.zshrc or ~/.bash_profile to persist"
            echo ""
            read -p "Do you want to set them now? (y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                read -p "LinkedIn Email: " email
                read -s -p "LinkedIn Password: " password
                echo ""
                export LINKEDIN_EMAIL="$email"
                export LINKEDIN_PASSWORD="$password"
                echo "${GREEN}✅ Credentials set for this session${NC}"
            else
                echo "${YELLOW}⚠️  Skipping LinkedIn scraping${NC}"
                echo ""
                echo "You can still use the CLI and other features:"
                echo "  ./scripts/newco_cli.py contact list"
                echo "  ./scripts/newco_cli.py network analyze"
                exit 0
            fi
        else
            echo "${GREEN}✅ LinkedIn credentials found${NC}"
        fi

        echo ""
        echo "${BLUE}Starting LinkedIn Network Analysis...${NC}"
        echo ""
        ./scripts/run_full_network_analysis.sh
        ;;

    2)
        echo ""
        echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
        echo "${BOLD}UNIFIED PLATFORM${NC}"
        echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
        echo ""

        cd ~/NEWCO/newco-unified-platform

        # Check if node_modules exists
        if [ ! -d "node_modules" ]; then
            echo "${YELLOW}Installing dependencies (this may take a few minutes)...${NC}"
            yarn install
            echo "${GREEN}✅ Dependencies installed${NC}"
            echo ""
        fi

        echo "${BLUE}Starting development server...${NC}"
        echo ""
        echo "${BOLD}Access points:${NC}"
        echo "  Frontend: ${GREEN}http://localhost:8910${NC}"
        echo "  GraphQL:  ${GREEN}http://localhost:8911/graphql${NC}"
        echo ""
        echo "${YELLOW}Press Ctrl+C to stop${NC}"
        echo ""

        yarn rw dev
        ;;

    3)
        echo ""
        echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
        echo "${BOLD}FULL SYSTEM LAUNCH${NC}"
        echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
        echo ""

        # Check credentials
        if [ -z "$LINKEDIN_EMAIL" ] || [ -z "$LINKEDIN_PASSWORD" ]; then
            echo "${YELLOW}⚠️  LinkedIn credentials not set${NC}"
            echo "   Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD for full functionality"
            echo ""
        fi

        # Start unified platform in background
        echo "${BLUE}Starting Unified Platform...${NC}"
        cd ~/NEWCO/newco-unified-platform

        if [ ! -d "node_modules" ]; then
            echo "${YELLOW}Installing dependencies...${NC}"
            yarn install
        fi

        # Create logs directory
        mkdir -p ~/NEWCO/logs

        # Start dev server in background
        nohup yarn rw dev > ~/NEWCO/logs/platform.log 2>&1 &
        PLATFORM_PID=$!
        echo "${GREEN}✅ Platform started (PID: $PLATFORM_PID)${NC}"
        echo "   Logs: ~/NEWCO/logs/platform.log"

        # Wait for server to start
        echo ""
        echo "${BLUE}Waiting for server to start...${NC}"
        sleep 5

        echo ""
        echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
        echo "${GREEN}✅ SYSTEM RUNNING${NC}"
        echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo "${BOLD}Access Points:${NC}"
        echo "  Frontend: ${GREEN}http://localhost:8910${NC}"
        echo "  GraphQL:  ${GREEN}http://localhost:8911/graphql${NC}"
        echo ""
        echo "${BOLD}Available Commands:${NC}"
        echo "  ${BLUE}CLI:${NC}              cd ~/NEWCO && ./scripts/newco_cli.py --help"
        echo "  ${BLUE}Network Analysis:${NC} cd ~/NEWCO && ./scripts/run_full_network_analysis.sh"
        echo "  ${BLUE}View Logs:${NC}        tail -f ~/NEWCO/logs/platform.log"
        echo ""
        echo "${BOLD}Stop Services:${NC}"
        echo "  kill $PLATFORM_PID"
        echo ""
        echo "${YELLOW}Press Enter to stop all services...${NC}"
        read

        echo ""
        echo "${BLUE}Stopping services...${NC}"
        kill $PLATFORM_PID 2>/dev/null || true
        echo "${GREEN}✅ All services stopped${NC}"
        ;;

    4)
        echo ""
        echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
        echo "${BOLD}VALIDATION REPORT${NC}"
        echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
        echo ""
        python3 validate_integration.py
        ;;

    5)
        echo ""
        echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
        echo "${BOLD}SETUP GUIDE${NC}"
        echo "${BOLD}════════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo "${BOLD}📚 Key Documentation:${NC}"
        echo ""
        echo "  ${GREEN}START_HERE.md${NC}"
        echo "    → Overview of all documentation"
        echo ""
        echo "  ${GREEN}CO_FOUNDER_QUICK_START.md${NC}"
        echo "    → 5-minute quick start guide"
        echo ""
        echo "  ${GREEN}LINKEDIN_NETWORK_ANALYSIS_GUIDE.md${NC}"
        echo "    → Complete LinkedIn scraping & analysis guide (200+ lines)"
        echo ""
        echo "  ${GREEN}MASTER_INTEGRATION_PLAN.md${NC}"
        echo "    → 7-phase integration plan"
        echo ""
        echo "  ${GREEN}CLAUDE.md${NC}"
        echo "    → Instructions for AI assistants"
        echo ""
        echo ""
        echo "${BOLD}🚀 Quick Start Steps:${NC}"
        echo ""
        echo "  ${BOLD}1. Set LinkedIn Credentials (Optional)${NC}"
        echo "     export LINKEDIN_EMAIL='your@email.com'"
        echo "     export LINKEDIN_PASSWORD='yourpassword'"
        echo ""
        echo "  ${BOLD}2. Run LinkedIn Analysis${NC}"
        echo "     ./scripts/run_full_network_analysis.sh"
        echo ""
        echo "  ${BOLD}3. Use the CLI${NC}"
        echo "     ./scripts/newco_cli.py contact list"
        echo "     ./scripts/newco_cli.py network multipliers"
        echo "     ./scripts/newco_cli.py email generate <id>"
        echo ""
        echo "  ${BOLD}4. Start Web Platform${NC}"
        echo "     cd newco-unified-platform"
        echo "     yarn rw dev"
        echo ""
        echo ""
        echo "${BOLD}💡 Key Features:${NC}"
        echo ""
        echo "  ✓ LinkedIn network scraping (1-4 degrees)"
        echo "  ✓ Social network analysis (academic theory-based)"
        echo "  ✓ Network multipliers identification"
        echo "  ✓ Warm introduction path finding"
        echo "  ✓ Contact & relationship management"
        echo "  ✓ Email generation with templates"
        echo "  ✓ Pipeline tracking"
        echo "  ✓ RedwoodJS unified platform"
        echo ""
        ;;

    *)
        echo "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo ""
echo "${GREEN}Done!${NC}"
echo ""

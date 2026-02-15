#!/bin/bash
# NEWCO Quick Start Script

echo "================================================"
echo "NEWCO GTM Management System - Quick Start"
echo "================================================"
echo ""

# Check if in correct directory
if [ ! -f "scripts/newco_cli.py" ]; then
    echo "Error: Please run this from the NEWCO directory"
    echo "Usage: cd ~/NEWCO && ./scripts/quickstart.sh"
    exit 1
fi

# Check Python
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed"
    exit 1
fi
echo "✓ Python 3 found"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Check if contacts exist
echo ""
if [ ! -s "data/contacts.csv" ] || [ "$(wc -l < data/contacts.csv)" -le 1 ]; then
    echo "No contacts found in database."
    echo ""
    echo "Would you like to:"
    echo "1. Add sample contacts (for testing)"
    echo "2. Add contacts interactively"
    echo "3. Skip (you can add contacts later)"
    echo ""
    read -p "Select option (1-3): " choice

    case $choice in
        1)
            echo ""
            echo "Adding sample contacts..."
            echo "2" | ./scripts/import_contacts.py
            ;;
        2)
            echo ""
            ./scripts/import_contacts.py
            ;;
        3)
            echo "Skipping contact import."
            echo "You can add contacts later with: ./scripts/import_contacts.py"
            ;;
        *)
            echo "Invalid choice. Skipping."
            ;;
    esac
fi

# Show dashboard
echo ""
echo "================================================"
echo "Your NEWCO Dashboard"
echo "================================================"
./scripts/newco_cli.py report dashboard

# Show next steps
echo ""
echo "================================================"
echo "Next Steps"
echo "================================================"
echo ""
echo "1. Review your contacts:"
echo "   ./scripts/newco_cli.py contact list"
echo ""
echo "2. View top priorities:"
echo "   ./scripts/newco_cli.py contact prioritize"
echo ""
echo "3. Generate your first email:"
echo "   ./scripts/newco_cli.py email generate 1"
echo ""
echo "4. Read the playbook:"
echo "   cat docs/PLAYBOOK.md"
echo ""
echo "5. Review the 90-day plan:"
echo "   cat docs/90_Day_Plan.md"
echo ""
echo "For help: ./scripts/newco_cli.py --help"
echo ""
echo "================================================"
echo "You're ready to start! Good luck! 🚀"
echo "================================================"

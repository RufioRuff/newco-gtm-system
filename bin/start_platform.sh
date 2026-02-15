#!/bin/bash
#
# NEWCO Platform Startup Script
# Starts the Flask API server and opens the frontend
#

echo "════════════════════════════════════════════════════════"
echo "  NEWCO PLATFORM STARTUP"
echo "════════════════════════════════════════════════════════"
echo ""

# Check if demo data exists
if [ ! -f "data/portfolio/funds.csv" ]; then
    echo "⚠️  No demo data found. Creating demo data..."
    echo ""
    ./scripts/demo_portfolio.py
    ./scripts/demo_managers.py
    ./scripts/demo_public_markets.py
    ./scripts/demo_team.py
    ./scripts/demo_governance.py
    ./scripts/demo_budget.py
    ./scripts/demo_competitive.py
    echo ""
    echo "✓ Demo data created"
    echo ""
fi

# Start Flask API server in background
echo "🚀 Starting Flask API server..."
cd api
python3 server.py &
API_PID=$!
cd ..

# Wait for server to start
sleep 3

# Check if server is running
if ps -p $API_PID > /dev/null; then
    echo "✓ API server running (PID: $API_PID)"
    echo "   API endpoint: http://localhost:5000/api/health"
    echo ""
else
    echo "❌ Failed to start API server"
    exit 1
fi

# Open frontend in browser
echo "🌐 Opening frontend..."
open frontend/index.html || xdg-open frontend/index.html 2>/dev/null

echo ""
echo "════════════════════════════════════════════════════════"
echo "  ✅ NEWCO PLATFORM IS RUNNING"
echo "════════════════════════════════════════════════════════"
echo ""
echo "  Frontend:  file://$(pwd)/frontend/index.html"
echo "  API:       http://localhost:5000/api/health"
echo ""
echo "  Press Ctrl+C to stop the server"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping API server...'; kill $API_PID; echo '✓ Server stopped'; exit 0" INT
wait $API_PID

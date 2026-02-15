#!/bin/bash

echo "🚀 Launching NEWCO V10 Intelligence LP Platform"
echo "════════════════════════════════════════════════"
echo ""

# Check if Flask API is running
if curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
  echo "✓ Flask API is running on port 5001"
else
  echo "⚠️  Flask API not detected on port 5001"
  echo ""
  echo "Please start Flask API in another terminal first:"
  echo "  cd /Users/rufio/NEWCO"
  echo "  python3 api/server.py"
  echo ""
  read -p "Press Enter once Flask API is running..."
fi

echo ""
echo "Starting RedwoodJS platform..."
echo "  Web: http://localhost:8910"
echo "  API: http://localhost:8911"
echo ""
echo "Press Ctrl+C to stop"
echo "════════════════════════════════════════════════"
echo ""

# Start RedwoodJS dev server
yarn rw dev

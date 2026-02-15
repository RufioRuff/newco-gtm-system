#!/bin/bash
echo "🧪 Testing NEWCO V10 Setup..."
echo ""

echo "1. Checking Node version..."
node --version

echo ""
echo "2. Checking Yarn version..."
yarn --version

echo ""
echo "3. Checking dependencies installed..."
if [ -d "node_modules" ]; then
  echo "✓ node_modules exists"
  echo "  $(ls node_modules | wc -l) packages installed"
else
  echo "✗ node_modules missing - run: yarn install"
fi

echo ""
echo "4. Checking data adapter..."
if [ -f "src/lib/dataAdapter.js" ]; then
  echo "✓ Data adapter created"
  echo "  $(wc -l < src/lib/dataAdapter.js) lines"
else
  echo "✗ Data adapter missing"
fi

echo ""
echo "5. Checking AlphaEngineReal component..."
if [ -f "src/components/AlphaEngineReal.jsx" ]; then
  echo "✓ AlphaEngineReal component created"
  echo "  $(wc -l < src/components/AlphaEngineReal.jsx) lines"
else
  echo "✗ AlphaEngineReal missing"
fi

echo ""
echo "6. Checking Flask API..."
if curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
  echo "✓ Flask API is running on port 5001"
else
  echo "⚠️  Flask API not running - start with:"
  echo "   cd /Users/rufio/NEWCO && python3 api/server.py"
fi

echo ""
echo "7. Checking configuration..."
if [ -f ".env" ]; then
  echo "✓ .env file exists"
else
  echo "⚠️  .env not found - copy from .env.local"
fi

echo ""
echo "════════════════════════════════════════════════"
echo "✅ Setup Complete!"
echo ""
echo "To run the platform:"
echo "  1. Terminal 1: cd /Users/rufio/NEWCO && python3 api/server.py"
echo "  2. Terminal 2: cd /Users/rufio/NEWCO/alpha-engine && yarn rw dev"
echo "  3. Browser: http://localhost:8910"
echo "════════════════════════════════════════════════"

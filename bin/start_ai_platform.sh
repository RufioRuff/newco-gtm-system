#!/bin/bash

# Start NEWCO AI-Powered Platform
# This script starts the NEWCO API server with LLM integration

echo "=================================================="
echo "🤖 NEWCO AI-POWERED PLATFORM"
echo "=================================================="
echo ""

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  Ollama is not running. Starting Ollama service..."
    ollama serve &
    sleep 3
    echo "✅ Ollama started"
else
    echo "✅ Ollama is running"
fi

# Check available models
echo ""
echo "📊 Available AI Models:"
ollama list | grep -E "deepseek|phi4|qwen|mistral|llama|codellama"

echo ""
echo "=================================================="
echo "🚀 Starting NEWCO API Server..."
echo "=================================================="
echo ""
echo "API Endpoints:"
echo "  • Health Check:     http://localhost:5001/api/health"
echo "  • LLM Models:       http://localhost:5001/api/llm/models"
echo "  • Portfolio:        http://localhost:5001/api/portfolio/summary"
echo "  • AI Chat:          POST http://localhost:5001/api/llm/chat"
echo ""
echo "Documentation: /Users/rufio/NEWCO/LLM_INTEGRATION_GUIDE.md"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================================="
echo ""

# Change to API directory and start server
cd "$(dirname "$0")/api"
python3 server.py

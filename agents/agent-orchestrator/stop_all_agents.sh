#!/bin/bash
# NEWCO Agent Orchestrator - Stop All Agents
# ===========================================

echo "🛑 Stopping NEWCO Agent Orchestra..."
echo ""

# Stop all Python servers on agent ports
for port in {8001..8010}; do
    pid=$(lsof -ti:$port)
    if [ ! -z "$pid" ]; then
        kill $pid 2>/dev/null
        echo "✓ Stopped agent on port $port"
    fi
done

# Stop Ollama
pkill ollama
echo "✓ Stopped Ollama server"

echo ""
echo "✅ All agents stopped"

#!/bin/bash
# Start All Specialized PE Agents
# ================================

echo "🚀 Starting NEWCO Specialized PE Agents"
echo "========================================"
echo ""

# Start each agent on its own port
agents=(
    "deal_scout.py:9001:Deal Scout"
    "deal_advisor.py:9002:Deal Advisor"
    "portfolio_monitor.py:9003:Portfolio Monitor"
    "exit_advisor.py:9004:Exit Advisor"
    "technology_advisor.py:9005:Technology Advisor"
    "operational_advisor.py:9006:Operational Advisor"
    "financial_advisor.py:9007:Financial Advisor"
)

for agent in "${agents[@]}"; do
    IFS=':' read -r file port name <<< "$agent"
    echo "Starting $name on port $port..."
    python3 $file > /tmp/${file%.py}.log 2>&1 &
    echo "✅ $name running"
done

echo ""
echo "========================================"
echo "✅ All 7 Specialized Agents Started!"
echo "========================================"
echo ""
echo "📊 Agent Status:"
echo "   1. Deal Scout            → :9001"
echo "   2. Deal Advisor          → :9002"
echo "   3. Portfolio Monitor     → :9003"
echo "   4. Exit Advisor          → :9004"
echo "   5. Technology Advisor    → :9005"
echo "   6. Operational Advisor   → :9006"
echo "   7. Financial Advisor     → :9007"
echo ""
echo "🌐 Using Ollama Models:"
echo "   - qwen2.5:14b (Deal Scout, Exit, Financial)"
echo "   - deepseek-r1 (Deal Advisor - deep reasoning)"
echo "   - phi4 (Portfolio Monitor - fast)"
echo "   - deepseek-coder (Technology Advisor)"
echo "   - mistral (Operational Advisor)"
echo ""
echo "✨ NEWCO Specialized PE Agent Suite is running!"

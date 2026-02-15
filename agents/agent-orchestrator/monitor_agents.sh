#!/bin/bash
# NEWCO Agent Monitor - Real-time Status
# =======================================

while true; do
    clear
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║       NEWCO AGENT ORCHESTRA - LIVE STATUS                     ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    date
    echo ""

    # Check Ollama
    if pgrep -x "ollama" > /dev/null; then
        echo "🟢 Ollama Server       [RUNNING] localhost:11434"
    else
        echo "🔴 Ollama Server       [STOPPED]"
    fi

    # Check each agent port
    agents=(
        "8001:Secondary Pricing"
        "8002:Hiring Velocity"
        "8003:Burn Inference"
        "8004:IPO Predictor (96%)"
        "8005:Revenue Estimator"
        "8006:Gov Procurement"
        "8007:Portfolio Analyzer"
        "8008:Risk Assessor"
        "8009:ML Engineer"
        "8010:IC Memo Council"
    )

    echo ""
    echo "AGENTS:"
    for agent in "${agents[@]}"; do
        IFS=':' read -r port name <<< "$agent"
        if lsof -i:$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo "🟢 Agent #${port:3:1}: $name [RUNNING] :$port"
        else
            echo "🔴 Agent #${port:3:1}: $name [STOPPED]"
        fi
    done

    echo ""
    echo "SYSTEM:"
    echo "   CPU: $(top -l 1 | grep "CPU usage" | awk '{print $3}')"
    echo "   Memory: $(top -l 1 | grep PhysMem | awk '{print $2}')"
    echo "   Uptime: $(uptime | awk '{print $3,$4}' | sed 's/,//')"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "Press Ctrl+C to exit | Refreshing every 5 seconds..."

    sleep 5
done

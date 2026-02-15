# Metal.ai Quick Start Guide

## 🎉 What You Have

Your NEWCO platform now has **Metal.ai-inspired institutional intelligence** capabilities:

✅ **Document Intelligence** - Analyze pitch decks, LPAs, DD reports
✅ **Due Diligence Workflows** - 8-week DD automation, IC memos
✅ **Deal Intelligence** - Manager universe analysis, pattern detection
✅ **Knowledge Graph** - Natural language search
✅ **Market Intelligence** - Sector trends and insights
✅ **LP Reporting** - Automated quarterly letters

All powered by your **7 local LLM models** (100% private, no external APIs).

---

## 🚀 Quick Start (5 Minutes)

### 1. Analyze a Document

```bash
cd ~/NEWCO

# Create a sample pitch deck
cat > /tmp/sample_pitch.txt << 'EOF'
Company: TechCorp AI
Team: Jane Smith (ex-Google AI), John Doe (ex-Tesla)
Market: AI agents for customer service, $50B TAM
Traction: $2M ARR, 50 customers, 300% YoY growth
Product: AI-powered customer service automation
Ask: $10M Series A at $40M pre-money
EOF

# Analyze it
./scripts/metal_cli.py document analyze-pitch \
  --file /tmp/sample_pitch.txt \
  --name "TechCorp AI"
```

**Output:** Comprehensive analysis with team assessment, market opportunity, traction, risks, and investment recommendation.

---

### 2. Create a Due Diligence Workflow

```bash
# Create 8-week DD workflow for a manager
./scripts/metal_cli.py dd create-workflow \
  --manager "Sequoia Capital" \
  --fund "Fund XX"
```

**Output:** Week-by-week DD checklist with tasks and deadlines.

---

### 3. Generate DD Questions

```bash
# Get questions for team assessment
./scripts/metal_cli.py dd questions --focus team
```

**Output:** 15-20 specific due diligence questions about the team.

---

### 4. Search Your Data

```bash
# Natural language search
./scripts/metal_cli.py search "Show me all seed stage funds focusing on AI"
```

**Output:** Relevant results with supporting evidence.

---

### 5. Analyze Market Trends

```bash
# Get sector trend analysis
./scripts/metal_cli.py market sector-trends
```

**Output:** Hot sectors, cooling areas, emerging themes, recommendations.

---

## 📋 Common Use Cases

### Use Case 1: Analyze Manager Pitch Deck

**Scenario:** A VC manager sends you their fund pitch deck.

```bash
# Step 1: Save the pitch deck content to a file
cat > /tmp/manager_pitch.txt << 'EOF'
[Paste pitch deck content here]
EOF

# Step 2: Analyze it
./scripts/metal_cli.py document analyze-pitch \
  --file /tmp/manager_pitch.txt \
  --name "Acme Ventures"

# Step 3: Review the analysis
# - Executive summary
# - Team assessment
# - Investment highlights
# - Key risks
# - Recommendation
```

---

### Use Case 2: Full Due Diligence Process

**Scenario:** You're conducting due diligence on a manager.

```bash
# Step 1: Create DD workflow
./scripts/metal_cli.py dd create-workflow \
  --manager "Benchmark Capital" \
  --fund "Fund XI" > /tmp/dd_workflow.json

# Step 2: Generate questions for each focus area
./scripts/metal_cli.py dd questions --focus track_record > /tmp/questions_track_record.txt
./scripts/metal_cli.py dd questions --focus team > /tmp/questions_team.txt
./scripts/metal_cli.py dd questions --focus process > /tmp/questions_process.txt

# Step 3: After DD, analyze reference checks
cat > /tmp/references.json << 'EOF'
[
  {
    "name": "John Smith",
    "role": "LP at CalPERS",
    "feedback": "Best manager I've worked with. Returns consistently top quartile. Very transparent."
  },
  {
    "name": "Jane Doe",
    "role": "LP at Yale Endowment",
    "feedback": "Strong performer but communication could be better. Returns good, not great."
  }
]
EOF

./scripts/metal_cli.py dd analyze-refs \
  --data /tmp/references.json

# Step 4: Generate IC memo
cat > /tmp/dd_findings.json << 'EOF'
{
  "manager_name": "Benchmark Capital",
  "fund_name": "Fund XI",
  "track_record": "IRR 35%, Top quartile consistently",
  "team_assessment": "Strong team, 3 partners with 15+ years experience",
  "reference_checks": "Highly positive, 4/5 references enthusiastic",
  "portfolio_visits": "Visited 4 companies, all healthy with strong growth",
  "operations_review": "Best-in-class operations and reporting",
  "strengths": "Track record, team quality, process discipline",
  "risks": "Key person risk on founding partner, concentrated portfolio",
  "recommendation": "STRONG PROCEED"
}
EOF

./scripts/metal_cli.py dd generate-memo \
  --data /tmp/dd_findings.json > /tmp/ic_memo.txt

# Step 5: Review IC memo
cat /tmp/ic_memo.txt
```

---

### Use Case 3: Generate Quarterly LP Letter

**Scenario:** It's end of quarter and you need to send LP update.

```bash
# Step 1: Prepare portfolio data
cat > /tmp/portfolio_q1.json << 'EOF'
{
  "quarter": "Q1-2026",
  "nav": "$55M",
  "nav_change": "+$5M (+10%)",
  "contributions": "$2M",
  "distributions": "$1M",
  "tvpi": "1.45x",
  "dpi": "0.25x",
  "rvpi": "1.20x",
  "funds": [
    {
      "name": "Fund A",
      "performance": "Strong quarter, up 15%",
      "highlights": "Major exit from portfolio company X"
    },
    {
      "name": "Fund B",
      "performance": "Steady, up 5%",
      "highlights": "Deployed $1M in new companies"
    }
  ]
}
EOF

# Step 2: Write CEO notes
cat > /tmp/ceo_notes.txt << 'EOF'
Dear Limited Partners,

Q1 was a strong quarter for NEWCO. We're pleased to report solid performance
and continued progress on our fund commitments.

Key highlights:
- Completed due diligence on 3 new managers
- Made 2 new fund commitments totaling $8M
- Portfolio continues to perform well vs benchmarks

Market environment remains challenging but we see opportunities.

Best regards,
Ken Wallace, CEO
EOF

# Step 3: Generate letter
./scripts/metal_cli.py lp quarterly-letter \
  --quarter Q1-2026 \
  --data /tmp/portfolio_q1.json \
  --notes /tmp/ceo_notes.txt > /tmp/quarterly_letter.txt

# Step 4: Review and send
cat /tmp/quarterly_letter.txt
```

---

## 🛠️ All Commands Reference

### Document Intelligence

```bash
# Analyze pitch deck
./scripts/metal_cli.py document analyze-pitch --file <file> --name <company>

# Analyze LPA (Limited Partnership Agreement)
./scripts/metal_cli.py document analyze-lpa --file <file> --name <fund>

# Analyze due diligence report
./scripts/metal_cli.py document analyze-dd --file <file> --name <manager>

# Generate summary (short/medium/long)
./scripts/metal_cli.py document summary --file <file> --length medium
```

### Due Diligence Workflows

```bash
# Create 8-week DD workflow
./scripts/metal_cli.py dd create-workflow --manager <name> --fund <name>

# Generate IC memo
./scripts/metal_cli.py dd generate-memo --data <dd_findings.json>

# Analyze reference checks
./scripts/metal_cli.py dd analyze-refs --data <references.json>

# Identify red flags
./scripts/metal_cli.py dd red-flags --data <dd_data.json>

# Generate DD questions
./scripts/metal_cli.py dd questions --focus <area>
# Areas: track_record, team, process, operations, terms, portfolio
```

### Deal Intelligence

```bash
# Analyze manager universe
./scripts/metal_cli.py deal analyze-universe --data <managers.json>

# Identify deal patterns
./scripts/metal_cli.py deal patterns --data <deals.json>

# Analyze portfolio overlap
./scripts/metal_cli.py deal portfolio-overlap --data <funds.json>
```

### Knowledge Search

```bash
# Natural language search
./scripts/metal_cli.py search "your query here"

# Search with context data
./scripts/metal_cli.py search "your query" --data <context.txt>
```

### Market Intelligence

```bash
# Analyze sector trends
./scripts/metal_cli.py market sector-trends

# With market data
./scripts/metal_cli.py market sector-trends --data <market_data.txt>
```

### LP Reporting

```bash
# Generate quarterly letter
./scripts/metal_cli.py lp quarterly-letter \
  --quarter Q1-2026 \
  --data <portfolio.json> \
  --notes <ceo_notes.txt>
```

---

## 📊 Which LLM Model is Used?

The system automatically selects the best LLM for each task:

| Task | Model | Why |
|------|-------|-----|
| Document analysis | DeepSeek R1 | Best reasoning |
| Technical extraction | DeepSeek Coder | Data extraction |
| Writing (memos, letters) | Phi4 | Professional writing |
| Complex analysis | Qwen2.5 | Large context |
| Quick tasks | Mistral | Fast responses |

Configuration in `/Users/rufio/NEWCO/config/metal_ai_config.yaml`

---

## 🔧 Configuration

Edit `/Users/rufio/NEWCO/config/metal_ai_config.yaml` to:

- Change default models
- Adjust temperature settings
- Configure routing (local vs API)
- Enable/disable features

---

## 🚦 System Status

Check if Ollama is running:

```bash
ollama list
```

You should see:
- deepseek-r1
- deepseek-coder
- phi4
- qwen2.5
- mistral
- codellama
- llama3.2

If Ollama isn't running:

```bash
ollama serve
```

---

## 📁 Where Things Are

```
NEWCO/
├── scripts/
│   ├── metal_cli.py              # Main CLI tool
│   └── metal_ai/
│       ├── document_intelligence.py
│       ├── due_diligence.py
│       ├── deal_intelligence.py
│       ├── knowledge_graph.py
│       ├── market_intelligence.py
│       └── lp_reporting.py
│
├── config/
│   └── metal_ai_config.yaml      # Configuration
│
├── data/
│   └── metal_ai/                 # Processed documents
│
└── docs/
    ├── METAL_AI_INTEGRATION_PLAN.md    # Full plan
    └── METAL_AI_QUICK_START.md          # This file
```

---

## 🎯 Next Steps

### Week 1: Learn the Tools
- [ ] Try all document intelligence commands
- [ ] Create a DD workflow
- [ ] Generate some DD questions
- [ ] Run a market trends analysis

### Week 2: Real Usage
- [ ] Analyze actual pitch decks
- [ ] Start DD on real manager
- [ ] Generate your first IC memo
- [ ] Create quarterly LP letter

### Week 3: Integrate into Workflow
- [ ] Add to daily workflow
- [ ] Train team on usage
- [ ] Customize configuration
- [ ] Build custom templates

### Phase 2: Metal.ai API (Future)
When Metal.ai API access is available:
- [ ] Get API credentials
- [ ] Update `metal_ai_config.yaml`
- [ ] Enable hybrid mode
- [ ] Test API integration

---

## 💡 Tips

1. **Start Small:** Try one command at a time
2. **Use Real Data:** Test with actual documents for best results
3. **Review Output:** AI is a tool, not a replacement for judgment
4. **Iterate:** Refine prompts and configuration as you learn
5. **Local is Fast:** No API latency, instant results

---

## ❓ Troubleshooting

### "Command not found: ollama"
Ollama isn't installed or not in PATH. Reinstall or add to PATH.

### "Model not found"
Run `ollama pull <model-name>` to download missing models.

### "Import error"
Make sure you're running from NEWCO directory:
```bash
cd ~/NEWCO
./scripts/metal_cli.py --help
```

### Slow performance
Some models (DeepSeek R1, Qwen2.5) are slower. Use Mistral for quick tasks.

---

## 📚 Resources

- **Full Integration Plan:** `METAL_AI_INTEGRATION_PLAN.md`
- **Metal.ai Research:**
  - [Metal.ai Website](https://www.metal.ai/)
  - [Blog](https://www.metal.ai/blog)
  - [DealCloud Integration](https://www.metal.ai/blog/introducing-metals-dealcloud-integration)
  - [Berkshire Partners Case Study](https://www.metal.ai/blog/how-berkshire-partners-collaborative-approach-led-to-ai-adoption)

---

## 🤝 Getting Help

Questions? Issues?

1. Check this guide
2. Read `METAL_AI_INTEGRATION_PLAN.md`
3. Review code in `scripts/metal_ai/`
4. Modify configuration in `config/metal_ai_config.yaml`

---

**🎉 You're ready to use Metal.ai-inspired intelligence in NEWCO!**

Start with: `./scripts/metal_cli.py --help`

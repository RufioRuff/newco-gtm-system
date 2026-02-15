# 🤖 NEWCO LLM Integration Guide

## Overview

NEWCO Platform now has **7 local AI models** integrated via Ollama, providing AI-powered analysis, insights, and automation capabilities.

## 📊 Available Models

### 1. **DeepSeek R1** (5.2 GB) - *Advanced Reasoning*
- **Type:** Reasoning & Analysis
- **Best for:** Investment analysis, due diligence, strategic planning
- **Use Cases:**
  - Portfolio company evaluation
  - Investment thesis development
  - Due diligence reports
  - Strategic decision-making

### 2. **DeepSeek Coder** (776 MB) - *Technical Analysis*
- **Type:** Coding & Technical
- **Best for:** Technical due diligence, automation, code review
- **Use Cases:**
  - Technology stack evaluation
  - Technical team assessment
  - Portfolio company tech analysis
  - Automation script development

### 3. **Phi4** (9.1 GB) - *High Performance General*
- **Type:** General Purpose
- **Best for:** Email generation, reports, general analysis
- **Use Cases:**
  - Email drafting (LP communications, manager outreach)
  - Report generation
  - General business analysis
  - Document summarization

### 4. **Qwen2.5 14B** (9.0 GB) - *Large Scale Analysis*
- **Type:** Large General Purpose
- **Best for:** Complex market research, competitive intelligence
- **Use Cases:**
  - Market trend analysis
  - Competitive landscape mapping
  - Industry research
  - Multi-factor analysis

### 5. **Mistral** (4.4 GB) - *Fast Processing*
- **Type:** Fast & Efficient
- **Best for:** Quick summaries, categorization, extraction
- **Use Cases:**
  - Meeting notes extraction
  - Quick data summaries
  - Entity extraction
  - Real-time insights

### 6. **CodeLlama** (3.8 GB) - *Code Analysis*
- **Type:** Coding
- **Best for:** Code review, technical analysis
- **Use Cases:**
  - Portfolio company code review
  - Technical assessment
  - Development insights

### 7. **Llama3.2** (2.0 GB) - *Balanced*
- **Type:** General Purpose
- **Best for:** Various balanced tasks
- **Use Cases:**
  - General purpose queries
  - Balanced analysis

---

## 🚀 Quick Start

### Command Line Usage

#### 1. List all models:
```bash
cd /Users/rufio/NEWCO
python3 scripts/llm_service.py list
```

#### 2. Chat with a model:
```bash
python3 scripts/llm_service.py chat \
  --model deepseek-r1 \
  --prompt "What are key metrics for evaluating a Series B SaaS startup?"
```

#### 3. Test the integration:
```bash
python3 test_llm_integration.py
```

### Python Usage

```python
from llm_service import LLMService

# Initialize service
llm = LLMService()

# Simple chat
result = llm.chat(
    prompt="Analyze this investment opportunity...",
    model="deepseek-r1"
)
print(result['response'])

# Investment analysis
analysis = llm.analyze_investment(
    company_name="TechCorp",
    company_data={
        'sector': 'SaaS',
        'stage': 'Series B',
        'revenue': '$5M ARR',
        'growth': '150% YoY'
    }
)

# Generate email
email = llm.generate_email(
    contact_data={
        'name': 'John Smith',
        'company': 'Acme Ventures'
    },
    email_type='intro',
    context='Following up on Series B opportunity'
)
```

---

## 🌐 API Endpoints

### Base URL: `http://localhost:5001/api`

### 1. **List Models**
```http
GET /api/llm/models
```

**Response:**
```json
{
  "success": true,
  "models": [
    {
      "key": "deepseek-r1",
      "name": "deepseek-r1:latest",
      "type": "reasoning",
      "description": "Advanced reasoning and analysis model",
      "use_cases": ["investment_analysis", "due_diligence"]
    }
  ],
  "default_model": "deepseek-r1"
}
```

### 2. **Chat with Model**
```http
POST /api/llm/chat
Content-Type: application/json

{
  "prompt": "What are 3 key risks in this investment?",
  "model": "deepseek-r1",
  "context": "Series B SaaS company with $10M ARR"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Based on the context...",
  "model": "deepseek-r1:latest",
  "model_key": "deepseek-r1",
  "prompt_length": 150
}
```

### 3. **Analyze Investment**
```http
POST /api/llm/analyze/investment
Content-Type: application/json

{
  "company_name": "TechStartup Inc",
  "company_data": {
    "sector": "Enterprise SaaS",
    "stage": "Series B",
    "revenue": "$10M ARR",
    "growth_rate": "200% YoY",
    "burn_rate": "$1M/month"
  },
  "model": "deepseek-r1"
}
```

### 4. **Analyze Manager/Fund**
```http
POST /api/llm/analyze/manager
Content-Type: application/json

{
  "manager_name": "Acme Ventures Fund III",
  "manager_data": {
    "fund_size": "$500M",
    "vintage": "2024",
    "stage_focus": "Series B",
    "track_record": "2.5x TVPI on Fund II"
  }
}
```

### 5. **Generate Email**
```http
POST /api/llm/generate/email
Content-Type: application/json

{
  "contact_data": {
    "name": "Jane Doe",
    "company": "VC Partners",
    "title": "Partner"
  },
  "email_type": "follow_up",
  "context": "Following up on our discussion about co-investment",
  "model": "phi4"
}
```

### 6. **Summarize Market Data**
```http
POST /api/llm/summarize/market
Content-Type: application/json

{
  "market_data": {
    "sector": "AI/ML",
    "deal_volume": "150 deals",
    "avg_valuation": "$50M",
    "trend": "up 25%"
  },
  "model": "qwen2.5"
}
```

### 7. **Extract Insights from Text**
```http
POST /api/llm/extract/insights
Content-Type: application/json

{
  "text": "Meeting notes: Discussed $500M fund...",
  "task_type": "meeting_notes",
  "model": "mistral"
}
```

---

## 💡 Use Cases by Function

### Investment Team
- **Due Diligence**: Use `deepseek-r1` for comprehensive analysis
- **Technical DD**: Use `deepseek-coder` for tech stack evaluation
- **Quick Summaries**: Use `mistral` for fast meeting notes

### LP Relations
- **Quarterly Letters**: Use `phi4` for professional communications
- **Report Generation**: Use `qwen2.5` for comprehensive reports
- **Email Generation**: Use `phi4` for LP emails

### Portfolio Management
- **Company Analysis**: Use `deepseek-r1` for portfolio company insights
- **Market Research**: Use `qwen2.5` for sector analysis
- **Performance Review**: Use `phi4` for report generation

### Risk & Compliance
- **Risk Analysis**: Use `deepseek-r1` for risk assessment
- **Document Review**: Use `mistral` for quick extraction
- **Compliance Reports**: Use `phi4` for formatted reports

---

## ⚙️ Configuration

Configuration file: `/Users/rufio/NEWCO/config/llm_config.yaml`

```yaml
default_model: deepseek-r1
temperature: 0.7
max_tokens: 4096

task_model_mapping:
  investment_analysis: deepseek-r1
  due_diligence: deepseek-r1
  portfolio_analysis: qwen2.5
  email_generation: phi4
  technical_analysis: deepseek-coder
  quick_summary: mistral
  market_research: qwen2.5
  competitive_intel: qwen2.5
```

### Customize Models
Edit the config file to change default models or add new task mappings.

---

## 🔧 Integration with NEWCO CLI

### Add to CLI commands:
```bash
# Analyze a portfolio company
python3 scripts/newco_cli.py portfolio analyze-ai <company_id> --model deepseek-r1

# Generate LP email
python3 scripts/newco_cli.py lp email-ai <lp_id> --type quarterly --model phi4

# Analyze manager
python3 scripts/newco_cli.py managers analyze-ai <manager_id> --model deepseek-r1
```

---

## 🧪 Testing

Run comprehensive test:
```bash
cd /Users/rufio/NEWCO
python3 test_llm_integration.py
```

This will test:
- ✅ Model availability
- ✅ DeepSeek R1 reasoning
- ✅ Investment analysis
- ✅ Quick summaries with Mistral

---

## 📈 Performance Tips

1. **Fast Queries**: Use `mistral` for quick, simple tasks
2. **Complex Analysis**: Use `deepseek-r1` or `qwen2.5` for in-depth analysis
3. **Technical Tasks**: Use `deepseek-coder` or `codellama` for code/tech
4. **Balanced Tasks**: Use `phi4` or `llama3.2` for general purpose

### Model Selection Guide:
- **Speed**: mistral > llama3.2 > codellama > phi4 > qwen2.5 > deepseek-r1
- **Capability**: deepseek-r1 > qwen2.5 > phi4 > mistral
- **Technical**: deepseek-coder > codellama > deepseek-r1

---

## 🚀 Next Steps

1. **Start the API server**:
   ```bash
   cd /Users/rufio/NEWCO/api
   python3 server.py
   ```

2. **Test the API**:
   ```bash
   curl http://localhost:5001/api/llm/models
   ```

3. **Integrate with frontend** (if using React):
   - Add LLM widget to dashboard
   - Create AI-powered insights panel
   - Add "Ask AI" button to portfolio companies

4. **Automate workflows**:
   - Auto-generate weekly reports using `phi4`
   - Auto-analyze new investments using `deepseek-r1`
   - Auto-extract insights from emails using `mistral`

---

## 🔒 Security Notes

- All models run **locally** on your machine
- No data sent to external APIs
- Complete privacy and control
- No API keys or external dependencies required

---

## ❓ Troubleshooting

### Models not responding?
```bash
# Check Ollama status
ollama list

# Restart Ollama service
killall ollama
ollama serve
```

### Slow responses?
- Use smaller models (mistral, llama3.2) for faster results
- Reduce max_tokens in config
- Close other Ollama processes

### Import errors?
```bash
cd /Users/rufio/NEWCO
export PYTHONPATH="${PYTHONPATH}:/Users/rufio/NEWCO/scripts"
```

---

## 📚 Additional Resources

- **Ollama Documentation**: https://ollama.ai/docs
- **DeepSeek Models**: https://github.com/deepseek-ai
- **Model Cards**: Check individual model documentation for capabilities

---

**🎉 Your NEWCO platform is now AI-powered with 7 local models!**

For questions or support, refer to the main NEWCO documentation or test with:
```bash
python3 test_llm_integration.py
```

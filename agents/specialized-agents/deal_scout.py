#!/usr/bin/env python3
"""
NEWCO Deal Scout Agent
======================

Recreated from https://www.agenticprivatemarkets.ai/deal-scout

Capabilities:
- Identify hidden investment targets
- Scan industries for opportunities
- Qualify prospects based on criteria
- Manage deal pipeline
- Monitor and engage continuously

Uses local LLMs via Ollama (no API costs)
"""

import requests
import json
from datetime import datetime

class DealScoutAgent:
    def __init__(self, ollama_host="http://localhost:11434"):
        self.ollama_host = ollama_host
        self.model = "qwen2.5:14b"  # Best for market analysis
        self.pipeline = []

    def query_llm(self, prompt, system_prompt="You are an expert PE deal sourcing analyst."):
        """Query local LLM via Ollama"""
        response = requests.post(f"{self.ollama_host}/api/generate", json={
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        })
        return response.json()['response']

    def identify_targets(self, sector, criteria):
        """Identify hidden investment targets in a sector"""
        prompt = f"""
        Identify potential PE investment targets in the {sector} sector.

        Criteria:
        - Revenue: {criteria.get('revenue', '$10M-$100M')}
        - Growth: {criteria.get('growth', '>20% YoY')}
        - Stage: {criteria.get('stage', 'Growth/Mature')}
        - Geography: {criteria.get('geography', 'US/Global')}

        Provide:
        1. List of 10 potential targets
        2. Why each fits the criteria
        3. Key value drivers
        4. Competitive position
        5. Estimated valuation range
        """

        result = self.query_llm(prompt)

        return {
            "sector": sector,
            "criteria": criteria,
            "targets_identified": result,
            "timestamp": datetime.now().isoformat()
        }

    def market_analysis(self, sector):
        """Comprehensive industry landscape analysis"""
        prompt = f"""
        Analyze the {sector} sector for PE investment opportunities.

        Provide:
        1. Market size and growth rate
        2. Major players (top 10 companies)
        3. Industry trends and tailwinds
        4. Consolidation opportunities
        5. Regulatory environment
        6. Entry/exit multiples (typical)
        7. Key value creation levers
        8. Risks and headwinds
        """

        result = self.query_llm(prompt)

        return {
            "sector": sector,
            "analysis": result,
            "timestamp": datetime.now().isoformat()
        }

    def qualify_prospect(self, company_name, company_data):
        """Screen and qualify a prospect"""
        prompt = f"""
        Qualify {company_name} for PE investment.

        Company Data:
        - Revenue: {company_data.get('revenue', 'Unknown')}
        - Growth Rate: {company_data.get('growth', 'Unknown')}
        - EBITDA: {company_data.get('ebitda', 'Unknown')}
        - Employees: {company_data.get('employees', 'Unknown')}
        - Geography: {company_data.get('geography', 'Unknown')}

        Provide:
        1. Qualification score (0-100)
        2. Strengths (top 5)
        3. Concerns (top 5)
        4. Recommended next steps
        5. Estimated valuation range
        6. Comp set (3-5 companies)
        """

        result = self.query_llm(prompt)

        # Add to pipeline
        self.pipeline.append({
            "company": company_name,
            "qualification": result,
            "score": self._extract_score(result),
            "date_added": datetime.now().isoformat()
        })

        return {
            "company": company_name,
            "qualification": result,
            "pipeline_position": len(self.pipeline),
            "timestamp": datetime.now().isoformat()
        }

    def pipeline_status(self):
        """Get current pipeline status"""
        return {
            "total_companies": len(self.pipeline),
            "high_priority": len([c for c in self.pipeline if c.get('score', 0) > 80]),
            "medium_priority": len([c for c in self.pipeline if 60 < c.get('score', 0) <= 80]),
            "low_priority": len([c for c in self.pipeline if c.get('score', 0) <= 60]),
            "companies": self.pipeline,
            "timestamp": datetime.now().isoformat()
        }

    def monitor_and_engage(self, company_name):
        """Generate engagement strategy for prospect"""
        prompt = f"""
        Create an engagement strategy for {company_name}.

        Provide:
        1. Initial outreach message (CEO/founder)
        2. Value proposition (why partner with us?)
        3. Information requests (non-intrusive)
        4. Follow-up cadence (timeline)
        5. Relationship building tactics
        6. Red flags to watch for
        """

        result = self.query_llm(prompt)

        return {
            "company": company_name,
            "engagement_strategy": result,
            "timestamp": datetime.now().isoformat()
        }

    def _extract_score(self, text):
        """Extract qualification score from LLM response"""
        # Simple heuristic - look for number after "score"
        import re
        match = re.search(r'score.*?(\d+)', text, re.IGNORECASE)
        return int(match.group(1)) if match else 50


def main():
    """Demo Deal Scout Agent"""
    print("=" * 70)
    print("  NEWCO DEAL SCOUT AGENT")
    print("=" * 70)
    print()

    agent = DealScoutAgent()

    # 1. Market Analysis
    print("📊 Analyzing Defense Tech sector...")
    analysis = agent.market_analysis("Defense Tech & GovTech")
    print(analysis['analysis'][:500] + "...\n")

    # 2. Identify Targets
    print("🎯 Identifying investment targets...")
    targets = agent.identify_targets(
        sector="Defense Tech",
        criteria={
            "revenue": "$20M-$200M",
            "growth": ">30% YoY",
            "stage": "Growth",
            "geography": "US"
        }
    )
    print(targets['targets_identified'][:500] + "...\n")

    # 3. Qualify Prospect
    print("✅ Qualifying prospect...")
    qualification = agent.qualify_prospect(
        company_name="Acme Defense AI",
        company_data={
            "revenue": "$50M",
            "growth": "120% YoY",
            "ebitda": "$10M",
            "employees": 250,
            "geography": "US"
        }
    )
    print(f"Score: {qualification.get('score', 'N/A')}")
    print(qualification['qualification'][:500] + "...\n")

    # 4. Pipeline Status
    print("📈 Pipeline Status:")
    status = agent.pipeline_status()
    print(f"   Total Companies: {status['total_companies']}")
    print(f"   High Priority: {status['high_priority']}")
    print()

    # 5. Engagement Strategy
    print("🤝 Generating engagement strategy...")
    engagement = agent.monitor_and_engage("Acme Defense AI")
    print(engagement['engagement_strategy'][:500] + "...\n")

    print("=" * 70)
    print("✅ Deal Scout Agent Demo Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()

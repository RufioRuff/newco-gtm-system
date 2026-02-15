#!/usr/bin/env python3
"""
NEWCO Portfolio Monitor Agent
==============================

Real-time tracking of 42 portfolio companies.
KPIs, valuations, risk management.
"""

import requests
import json
from datetime import datetime

class PortfolioMonitorAgent:
    def __init__(self, ollama_host="http://localhost:11434"):
        self.ollama_host = ollama_host
        self.model = "phi4:latest"  # Fast for real-time analysis

    def query_llm(self, prompt):
        response = requests.post(f"{self.ollama_host}/api/generate", json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        return response.json()['response']

    def performance_tracking(self, company, metrics):
        """Track portco performance in real-time"""
        prompt = f"""
        Analyze {company} performance.

        Current Metrics:
        {json.dumps(metrics, indent=2)}

        Provide:
        1. Performance summary (vs plan)
        2. KPI trends (improving/declining)
        3. Red flags (if any)
        4. Action items for board
        5. Valuation impact
        6. Risk rating (1-10)
        """

        return self.query_llm(prompt)

    def valuation_rollover(self, company, financial_data):
        """Establish periodic valuation"""
        prompt = f"""
        Calculate valuation rollover for {company}.

        Financial Data:
        {json.dumps(financial_data, indent=2)}

        Calculate:
        1. Current NAV
        2. Valuation multiple
        3. Change from last quarter
        4. Key drivers of change
        5. Forward-looking adjustments
        6. Recommended mark
        """

        return self.query_llm(prompt)

    def board_report_summary(self, company, board_report):
        """Summarize board reports"""
        prompt = f"""
        Summarize board report for {company}.

        Report Length: {len(board_report)} chars

        Extract:
        1. Key highlights (top 5)
        2. Concerns raised (if any)
        3. Action items
        4. Financial performance
        5. Operational updates
        6. Strategic initiatives
        """

        return self.query_llm(prompt[:1000])  # Truncate if too long

    def risk_assessment(self, portfolio):
        """Real-time risk management across portfolio"""
        prompt = f"""
        Assess portfolio-wide risk.

        Portfolio:
        - Companies: {len(portfolio)}
        - Total NAV: ${sum(p.get('nav', 0) for p in portfolio)}M
        - Sectors: {len(set(p.get('sector') for p in portfolio))}

        Analyze:
        1. Concentration risk
        2. Sector exposure
        3. Performance outliers
        4. Liquidity concerns
        5. Top 5 risks
        6. Recommended actions
        """

        return self.query_llm(prompt)

if __name__ == "__main__":
    agent = PortfolioMonitorAgent()
    print("✅ Portfolio Monitor Agent Ready")

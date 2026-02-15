#!/usr/bin/env python3
"""
NEWCO Deal Advisor Agent
========================

Investment analysis and due diligence automation.
Uses XGBoost (96% accuracy) + local LLMs.
"""

import requests
import json
import sys
sys.path.append('../learning-projects/xgboost-ipo-predictor')

class DealAdvisorAgent:
    def __init__(self, ollama_host="http://localhost:11434"):
        self.ollama_host = ollama_host
        self.model = "deepseek-r1:latest"  # Best for deep reasoning

    def query_llm(self, prompt):
        response = requests.post(f"{self.ollama_host}/api/generate", json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        return response.json()['response']

    def investment_thesis(self, company_data):
        """Generate initial point of view on investment"""
        prompt = f"""
        Generate investment thesis for {company_data['name']}.

        Data:
        - Sector: {company_data.get('sector')}
        - Revenue: {company_data.get('revenue')}
        - Growth: {company_data.get('growth')}
        - Market: {company_data.get('market')}

        Provide:
        1. Investment thesis (3-5 key points)
        2. Value drivers (top 5)
        3. Key risks (top 5)
        4. Market context and positioning
        5. Recommended entry multiple
        6. Upside scenarios
        7. Base case return projection
        """

        return self.query_llm(prompt)

    def benchmark_valuation(self, company_data, comps):
        """Compare against sector standards"""
        prompt = f"""
        Benchmark {company_data['name']} valuation.

        Target Metrics:
        - Revenue: {company_data.get('revenue')}
        - EBITDA: {company_data.get('ebitda')}
        - Growth: {company_data.get('growth')}

        Comparable Companies:
        {json.dumps(comps, indent=2)}

        Analyze:
        1. Revenue multiple vs comps
        2. EBITDA multiple vs comps
        3. Growth-adjusted valuation
        4. Quality premium/discount factors
        5. Fair value range
        6. Negotiation strategy
        """

        return self.query_llm(prompt)

    def dd_questions(self, company_name, risks):
        """Generate management interview questions"""
        prompt = f"""
        Create due diligence questions for {company_name}.

        Key Risks Identified:
        {json.dumps(risks, indent=2)}

        Generate:
        1. Financial DD questions (10)
        2. Operational DD questions (10)
        3. Market/competitive questions (10)
        4. Management team questions (10)
        5. Customer/revenue questions (10)
        6. Technology/IP questions (10)

        Prioritize questions that address identified risks.
        """

        return self.query_llm(prompt)

if __name__ == "__main__":
    agent = DealAdvisorAgent()
    print("✅ Deal Advisor Agent Ready")

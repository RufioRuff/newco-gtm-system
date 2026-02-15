#!/usr/bin/env python3
"""
NEWCO Financial Advisor Agent
==============================

Financial modeling, projections, and analysis.
"""

import requests

class FinancialAdvisorAgent:
    def __init__(self, ollama_host="http://localhost:11434"):
        self.ollama_host = ollama_host
        self.model = "qwen2.5:14b"

    def query_llm(self, prompt):
        response = requests.post(f"{self.ollama_host}/api/generate", json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        return response.json()['response']

    def financial_model(self, company, historicals, assumptions):
        """Build 5-year financial model"""
        prompt = f"""
        Build financial model for {company}.

        Historicals:
        {historicals}

        Assumptions:
        {assumptions}

        Project (5 years):
        1. Revenue growth
        2. Gross margin expansion
        3. Operating leverage
        4. EBITDA progression
        5. CapEx requirements
        6. Working capital needs
        7. Free cash flow
        8. Exit valuation range
        9. Returns (MOIC/IRR)
        """

        return self.query_llm(prompt)

    def sensitivity_analysis(self, company, base_case, variables):
        """Analyze sensitivity to key assumptions"""
        prompt = f"""
        Sensitivity analysis for {company}.

        Base Case Returns: {base_case}

        Key Variables:
        {variables}

        Analyze:
        1. Revenue growth sensitivity
        2. Margin impact on returns
        3. Multiple sensitivity
        4. Hold period impact
        5. Downside scenarios
        6. Upside scenarios
        7. Risk-adjusted return
        8. Recommended entry multiple
        """

        return self.query_llm(prompt)

if __name__ == "__main__":
    agent = FinancialAdvisorAgent()
    print("✅ Financial Advisor Agent Ready")

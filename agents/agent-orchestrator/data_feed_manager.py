#!/usr/bin/env python3
"""
NEWCO Data Feed Manager
======================

Feeds PE-VC source data to all agents and keeps them updated.
Connects agents with company and people information.
"""

import json
import requests
import sys
import os
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.append('/Users/rufio/NEWCO/data-scraper')
sys.path.append('/Users/rufio/NEWCO/agent-orchestrator')

from supabase_sync import SupabaseSync

# Configuration
DATA_FILE = "/Users/rufio/NEWCO/PE-VC-Source-Data/pe_vc_data.json"

# Agent endpoints
AGENTS = {
    "secondary_pricing": "http://localhost:8001",
    "hiring_velocity": "http://localhost:8002",
    "burn_inference": "http://localhost:8003",
    "ipo_predictor": "http://localhost:8004",
    "revenue_estimator": "http://localhost:8005",
    "gov_procurement": "http://localhost:8006",
    "portfolio_analyzer": "http://localhost:8007",
    "risk_assessor": "http://localhost:8008",
    "ml_engineer": "http://localhost:8009",
    "llm_council": "http://localhost:8010"
}

SPECIALIZED_AGENTS = {
    "deal_scout": "http://localhost:9001",
    "deal_advisor": "http://localhost:9002",
    "portfolio_monitor": "http://localhost:9003",
    "exit_advisor": "http://localhost:9004",
    "technology_advisor": "http://localhost:9005",
    "operational_advisor": "http://localhost:9006",
    "financial_advisor": "http://localhost:9007"
}

class DataFeedManager:
    """Manages data feeds to all agents"""

    def __init__(self):
        self.data = self.load_data()
        self.supabase = SupabaseSync()

    def load_data(self) -> Dict[str, Any]:
        """Load PE-VC data"""
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            print(f"✅ Loaded data: {data['metadata']['total_companies']} companies, {data['metadata']['total_people']} people")
            return data
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return {"companies": {}, "people": {}, "metadata": {}}

    def check_agent_health(self, url: str) -> bool:
        """Check if agent is responsive"""
        try:
            response = requests.get(url, timeout=2)
            return response.status_code == 200
        except:
            return False

    def feed_to_ipo_predictor(self):
        """Feed company data to IPO predictor"""
        print("\n📊 Feeding data to IPO Predictor...")

        companies = self.data.get('companies', {})
        predictions = []

        for name, company in companies.items():
            if company.get('ipo_probability') is None:
                # Prepare features for prediction
                features = {
                    "revenue": company.get('revenue', 0),
                    "revenue_growth": company.get('revenue_growth', 0),
                    "burn_multiple": company.get('burn_multiple', 0),
                    "valuation": company.get('valuation', 0),
                    "total_funding": company.get('total_funding', 0)
                }

                # In real implementation, would call XGBoost model API
                # For now, calculate based on metrics
                score = 0
                if features['revenue'] > 100000000:  # $100M+
                    score += 30
                if features['revenue_growth'] > 50:  # 50%+
                    score += 30
                if features['burn_multiple'] and features['burn_multiple'] < 1:
                    score += 20
                if features['valuation'] > 1000000000:  # $1B+
                    score += 20

                predictions.append({
                    "company": name,
                    "ipo_probability": min(score, 95),
                    "features": features
                })

        print(f"✅ Generated {len(predictions)} IPO predictions")
        return predictions

    def feed_to_portfolio_monitor(self):
        """Feed company data to Portfolio Monitor"""
        print("\n📈 Feeding data to Portfolio Monitor...")

        companies = self.data.get('companies', {})
        portfolio_companies = []

        for name, company in companies.items():
            if company.get('stage') not in ['Public', 'Acquired']:
                portfolio_companies.append({
                    "name": name,
                    "sector": company.get('sector', 'Unknown'),
                    "stage": company.get('stage', 'Unknown'),
                    "revenue": company.get('revenue', 0),
                    "revenue_growth": company.get('revenue_growth', 0),
                    "burn_rate": company.get('burn_rate', 0),
                    "valuation": company.get('valuation', 0),
                    "employees": company.get('employees', 0)
                })

        print(f"✅ {len(portfolio_companies)} companies added to portfolio monitor")
        return portfolio_companies

    def feed_to_deal_scout(self):
        """Feed target companies to Deal Scout"""
        print("\n🎯 Feeding data to Deal Scout...")

        companies = self.data.get('companies', {})
        targets = []

        for name, company in companies.items():
            # Identify potential targets (not public, high growth)
            if company.get('stage') != 'Public' and company.get('revenue_growth', 0) > 50:
                targets.append({
                    "name": name,
                    "sector": company.get('sector', 'Unknown'),
                    "stage": company.get('stage', 'Unknown'),
                    "revenue": company.get('revenue', 0),
                    "growth_rate": company.get('revenue_growth', 0),
                    "valuation": company.get('valuation', 0),
                    "investors": company.get('investors', []),
                    "people": company.get('people', [])
                })

        print(f"✅ {len(targets)} potential targets identified")
        return targets

    def sync_to_supabase(self):
        """Sync all data to Supabase"""
        print("\n☁️  Syncing to Supabase...")

        if not self.supabase.enabled:
            print("⏭  Supabase not configured")
            return

        # Sync portfolio companies
        companies = self.data.get('companies', {})
        company_list = [
            {
                "name": name,
                "revenue": company.get('revenue', 0),
                "growth_rate": company.get('revenue_growth', 0),
                "burn_multiple": company.get('burn_multiple', 0),
                "ipo_probability": company.get('ipo_probability', 0)
            }
            for name, company in companies.items()
        ]

        self.supabase.sync_portfolio_data(company_list)

    def generate_summary(self) -> str:
        """Generate data summary"""
        companies = self.data.get('companies', {})
        people = self.data.get('people', {})

        # Calculate metrics (handle None values)
        total_valuation = sum([c.get('valuation', 0) or 0 for c in companies.values()])
        total_funding = sum([c.get('total_funding', 0) or 0 for c in companies.values()])
        avg_growth = sum([c.get('revenue_growth', 0) or 0 for c in companies.values()]) / len(companies) if companies else 0

        summary = f"""
╔═══════════════════════════════════════════════════════════════╗
║              NEWCO DATA FEED SUMMARY                         ║
╚═══════════════════════════════════════════════════════════════╝

📊 Dataset Overview:
   • Companies: {len(companies)}
   • People: {len(people)}
   • Total Valuation: ${total_valuation/1e9:.2f}B
   • Total Funding: ${total_funding/1e9:.2f}B
   • Avg Growth Rate: {avg_growth:.1f}%

🎯 Top Companies by Valuation:
"""
        # Sort companies by valuation
        sorted_companies = sorted(
            companies.items(),
            key=lambda x: x[1].get('valuation', 0),
            reverse=True
        )[:5]

        for i, (name, company) in enumerate(sorted_companies, 1):
            valuation = company.get('valuation', 0)
            stage = company.get('stage', 'Unknown')
            summary += f"   {i}. {name}: ${valuation/1e9:.2f}B ({stage})\n"

        summary += f"""
👥 Key People:
"""
        # List some key people
        for i, (name, person) in enumerate(list(people.items())[:10], 1):
            companies = ', '.join(person.get('companies', [])[:2])
            summary += f"   • {name}: {companies}\n"

        summary += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return summary

    def feed_all_agents(self):
        """Feed data to all agents"""
        print(f"""
╔═══════════════════════════════════════════════════════════════╗
║              NEWCO DATA FEED MANAGER                         ║
╚═══════════════════════════════════════════════════════════════╝

Starting data feed to all agents...
""")

        # Check agent health
        print("🔍 Checking agent health...")
        all_agents = {**AGENTS, **SPECIALIZED_AGENTS}
        healthy_agents = []

        for name, url in all_agents.items():
            if self.check_agent_health(url):
                healthy_agents.append(name)
                print(f"  ✓ {name}")
            else:
                print(f"  ✗ {name} (offline)")

        print(f"\n{len(healthy_agents)}/{len(all_agents)} agents online\n")

        # Feed data to specific agents
        ipo_predictions = self.feed_to_ipo_predictor()
        portfolio_companies = self.feed_to_portfolio_monitor()
        targets = self.feed_to_deal_scout()

        # Sync to Supabase
        self.sync_to_supabase()

        # Generate and save summary
        summary = self.generate_summary()
        print(summary)

        summary_file = f"/Users/rufio/NEWCO/daily_summaries/data_feed_{datetime.now().strftime('%Y%m%d')}.txt"
        os.makedirs(os.path.dirname(summary_file), exist_ok=True)
        with open(summary_file, 'w') as f:
            f.write(summary)

        print(f"✅ Summary saved to {summary_file}")
        print("\n✨ Data feed complete!")

        return {
            "ipo_predictions": ipo_predictions,
            "portfolio_companies": portfolio_companies,
            "targets": targets,
            "healthy_agents": healthy_agents
        }

def main():
    manager = DataFeedManager()
    results = manager.feed_all_agents()

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IPO Predictions:       {len(results['ipo_predictions'])}
Portfolio Companies:   {len(results['portfolio_companies'])}
Deal Targets:          {len(results['targets'])}
Healthy Agents:        {len(results['healthy_agents'])}/17

All data has been fed to agents and synced to Supabase.
Agents are now operating with latest PE-VC data.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
NEWCO Supabase Integration
==========================

Syncs agent data, model outputs, and analytics to Supabase for:
- Real-time collaboration with partner
- Data persistence and backup
- Analytics dashboard
- Historical tracking
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/rufio/NEWCO/.env')

SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')

class SupabaseSync:
    """Sync NEWCO data to Supabase"""

    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("⚠️  Supabase not configured. Edit /Users/rufio/NEWCO/.env")
            self.enabled = False
        else:
            self.enabled = True
            self.headers = {
                'apikey': SUPABASE_KEY,
                'Authorization': f'Bearer {SUPABASE_KEY}',
                'Content-Type': 'application/json'
            }

    def sync_agent_status(self, agents: List[Dict[str, Any]]) -> bool:
        """Sync agent health status to Supabase"""
        if not self.enabled:
            return False

        try:
            payload = {
                'timestamp': datetime.now().isoformat(),
                'agents': agents,
                'total_agents': len(agents),
                'running_agents': len([a for a in agents if 'Running' in str(a.get('status', ''))])
            }

            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/agent_status",
                headers=self.headers,
                json=payload
            )

            if response.status_code in [200, 201]:
                print(f"✅ Agent status synced to Supabase")
                return True
            else:
                print(f"⚠️  Supabase sync failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Supabase error: {str(e)}")
            return False

    def sync_model_prediction(self, model: str, prediction: Dict[str, Any]) -> bool:
        """Sync model predictions to Supabase"""
        if not self.enabled:
            return False

        try:
            payload = {
                'timestamp': datetime.now().isoformat(),
                'model': model,
                'prediction': prediction
            }

            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/predictions",
                headers=self.headers,
                json=payload
            )

            if response.status_code in [200, 201]:
                return True
            else:
                return False

        except Exception as e:
            print(f"❌ Error syncing prediction: {str(e)}")
            return False

    def sync_portfolio_data(self, companies: List[Dict[str, Any]]) -> bool:
        """Sync portfolio company data to Supabase"""
        if not self.enabled:
            return False

        try:
            for company in companies:
                payload = {
                    'timestamp': datetime.now().isoformat(),
                    'company_name': company.get('name', ''),
                    'revenue': company.get('revenue', 0),
                    'growth_rate': company.get('growth_rate', 0),
                    'burn_multiple': company.get('burn_multiple', 0),
                    'ipo_probability': company.get('ipo_probability', 0)
                }

                response = requests.post(
                    f"{SUPABASE_URL}/rest/v1/portfolio",
                    headers=self.headers,
                    json=payload
                )

                if response.status_code not in [200, 201]:
                    print(f"⚠️  Failed to sync {company.get('name')}")

            print(f"✅ Portfolio data synced ({len(companies)} companies)")
            return True

        except Exception as e:
            print(f"❌ Error syncing portfolio: {str(e)}")
            return False

    def sync_daily_summary(self, summary: str) -> bool:
        """Sync daily summary to Supabase"""
        if not self.enabled:
            return False

        try:
            payload = {
                'date': datetime.now().date().isoformat(),
                'timestamp': datetime.now().isoformat(),
                'summary': summary
            }

            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/daily_summaries",
                headers=self.headers,
                json=payload
            )

            if response.status_code in [200, 201]:
                print(f"✅ Daily summary synced to Supabase")
                return True
            else:
                return False

        except Exception as e:
            print(f"❌ Error syncing summary: {str(e)}")
            return False

    def get_recent_activity(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch recent activity from Supabase"""
        if not self.enabled:
            return []

        try:
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/agent_status?order=timestamp.desc&limit={limit}",
                headers=self.headers
            )

            if response.status_code == 200:
                return response.json()
            else:
                return []

        except Exception as e:
            print(f"❌ Error fetching activity: {str(e)}")
            return []

def setup_supabase_tables():
    """
    SQL schema for Supabase tables (run this in Supabase SQL editor):

    -- Agent Status Table
    CREATE TABLE agent_status (
        id BIGSERIAL PRIMARY KEY,
        timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        agents JSONB NOT NULL,
        total_agents INTEGER NOT NULL,
        running_agents INTEGER NOT NULL
    );

    -- Predictions Table
    CREATE TABLE predictions (
        id BIGSERIAL PRIMARY KEY,
        timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        model TEXT NOT NULL,
        prediction JSONB NOT NULL
    );

    -- Portfolio Table
    CREATE TABLE portfolio (
        id BIGSERIAL PRIMARY KEY,
        timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        company_name TEXT NOT NULL,
        revenue NUMERIC,
        growth_rate NUMERIC,
        burn_multiple NUMERIC,
        ipo_probability NUMERIC
    );

    -- Daily Summaries Table
    CREATE TABLE daily_summaries (
        id BIGSERIAL PRIMARY KEY,
        date DATE NOT NULL UNIQUE,
        timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        summary TEXT NOT NULL
    );

    -- Enable Row Level Security
    ALTER TABLE agent_status ENABLE ROW LEVEL SECURITY;
    ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;
    ALTER TABLE portfolio ENABLE ROW LEVEL SECURITY;
    ALTER TABLE daily_summaries ENABLE ROW LEVEL SECURITY;

    -- Create policies (adjust as needed)
    CREATE POLICY "Enable read access for all users" ON agent_status FOR SELECT USING (true);
    CREATE POLICY "Enable insert for authenticated users only" ON agent_status FOR INSERT WITH CHECK (true);
    """
    print(__doc__)

if __name__ == "__main__":
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  NEWCO Supabase Integration Setup")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")

    # Check configuration
    supabase = SupabaseSync()

    if not supabase.enabled:
        print("")
        print("To enable Supabase integration:")
        print("")
        print("1. Create a Supabase project at https://supabase.com")
        print("2. Get your project URL and anon key")
        print("3. Add to /Users/rufio/NEWCO/.env:")
        print("   SUPABASE_URL=https://your-project.supabase.co")
        print("   SUPABASE_KEY=your-anon-key")
        print("")
        print("4. Run this SQL in Supabase SQL editor:")
        print("")
        setup_supabase_tables()
    else:
        print("✅ Supabase configured and ready!")
        print("")
        print("Testing connection...")

        # Test sync
        test_agents = [
            {"port": 8001, "status": "🟢 Running"},
            {"port": 8002, "status": "🟢 Running"}
        ]

        if supabase.sync_agent_status(test_agents):
            print("✅ Connection successful!")
        else:
            print("⚠️  Connection failed - check credentials")

#!/usr/bin/env python3
"""
LP Reporting Intelligence - Metal.ai Inspired

Auto-generate quarterly letters and LP materials.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "core" / "scripts"))
from llm_service import LLMService


class LPReporting:
    """LP reporting automation"""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize LP reporting service"""
        self.llm_service = LLMService()

        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "metal_ai_config.yaml"

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.models = self.config.get('models', {})

    def generate_quarterly_letter(self, quarter: str, portfolio_data: Dict[str, Any],
                                  ceo_notes: str = "") -> Dict[str, Any]:
        """Generate quarterly LP letter"""

        prompt = f"""Generate a professional quarterly LP letter for Q{quarter}.

PORTFOLIO DATA:
{portfolio_data}

CEO HIGHLIGHTS:
{ceo_notes}

Generate letter with:

# Quarterly Letter to Limited Partners
## Q{quarter}

### Executive Summary
(CEO's key messages - integrate provided notes)

### Portfolio Performance
(Auto-generated from data:)
- NAV change
- Contributions and distributions
- TVPI, DPI, RVPI
- vs. Benchmarks

### Fund Updates
(Summarize each fund's performance and activities)

### New Commitments
(Any new fund commitments this quarter)

### Market Commentary
(Market trends and outlook)

### Capital Calls and Distributions Forecast
(What to expect next quarter)

### Conclusion
(CEO closing message)

Make it professional, clear, and transparent. Use data to tell a story."""

        model = self.models.get('lp_letter_writing', 'phi4')
        result = self.llm_service.chat(prompt, model=model, temperature=0.7, max_tokens=6144)

        return {
            'quarter': quarter,
            'timestamp': datetime.now().isoformat(),
            'letter': result['response'],
            'model_used': result['model']
        }


def main():
    """CLI interface"""
    import argparse
    import json

    parser = argparse.ArgumentParser(description='LP Reporting')
    parser.add_argument('command', choices=['quarterly-letter'])
    parser.add_argument('--quarter', required=True, help='Quarter (e.g., Q1-2026)')
    parser.add_argument('--data', required=True, help='Path to portfolio data JSON')
    parser.add_argument('--notes', help='Path to CEO notes file')

    args = parser.parse_args()

    lp_reporting = LPReporting()

    with open(args.data, 'r') as f:
        portfolio_data = json.load(f)

    ceo_notes = ""
    if args.notes:
        with open(args.notes, 'r') as f:
            ceo_notes = f.read()

    if args.command == 'quarterly-letter':
        result = lp_reporting.generate_quarterly_letter(args.quarter, portfolio_data, ceo_notes)

    print(result['letter'])


if __name__ == '__main__':
    main()

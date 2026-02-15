#!/usr/bin/env python3
"""
Market Intelligence Dashboard - Metal.ai Inspired

Real-time intelligence on VC manager landscape and market trends.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "core" / "scripts"))
from llm_service import LLMService


class MarketIntelligence:
    """Market intelligence and trends analysis"""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize market intelligence service"""
        self.llm_service = LLMService()

        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "metal_ai_config.yaml"

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.models = self.config.get('models', {})

    def analyze_sector_trends(self, market_data: str = "") -> Dict[str, Any]:
        """Analyze sector trends and hot areas"""

        prompt = f"""Analyze current VC market trends and identify hot sectors.

{f"MARKET DATA: {market_data}" if market_data else ""}

Provide:

1. **Hot Sectors** (Top 5):
   - Why they're hot
   - Investment activity
   - Key players
   - Outlook

2. **Cooling Sectors**:
   - What's slowing down
   - Why
   - Implications

3. **Emerging Themes**:
   - New trends to watch
   - Early signals
   - Opportunities

4. **Investment Recommendations**:
   - Where to focus
   - Where to avoid
   - Timing considerations

5. **Market Outlook**:
   - Next 6-12 months
   - Key risks
   - Key opportunities"""

        model = self.models.get('market_analysis', 'qwen2.5')
        result = self.llm_service.chat(prompt, model=model, temperature=0.6, max_tokens=4096)

        return {
            'timestamp': datetime.now().isoformat(),
            'analysis': result['response'],
            'model_used': result['model']
        }


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Market Intelligence')
    parser.add_argument('command', choices=['sector-trends'])
    parser.add_argument('--data', help='Path to market data file')

    args = parser.parse_args()

    market_intel = MarketIntelligence()

    market_data = ""
    if args.data:
        with open(args.data, 'r') as f:
            market_data = f.read()

    if args.command == 'sector-trends':
        result = market_intel.analyze_sector_trends(market_data)

    print(result['analysis'])


if __name__ == '__main__':
    main()

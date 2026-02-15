#!/usr/bin/env python3
"""
Deal Intelligence Engine - Metal.ai Inspired

Aggregate and analyze deal data across managers, funds, and portfolio companies.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "core" / "scripts"))
from llm_service import LLMService


class DealIntelligence:
    """Deal data aggregation and intelligence"""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize deal intelligence service"""
        self.llm_service = LLMService()

        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "metal_ai_config.yaml"

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.models = self.config.get('models', {})

    def analyze_manager_universe(self, managers_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze entire universe of managers and their relationships"""

        prompt = f"""Analyze this universe of VC fund managers and identify patterns, clusters, and insights.

MANAGERS DATA:
{json.dumps(managers_data, indent=2)[:10000]}...

Provide:

1. **Market Landscape**:
   - Total managers tracked
   - Total AUM across all managers
   - Stage distribution (seed/A/B/growth)
   - Sector concentration

2. **Clustering Analysis**:
   - Natural clusters (by stage, sector, geography)
   - Competitive sets
   - Differentiated positions

3. **Performance Patterns**:
   - Top performers (if performance data available)
   - Consistent performers
   - Emerging managers to watch

4. **Network Effects**:
   - Managers who co-invest frequently
   - Portfolio overlap patterns
   - Syndicate relationships

5. **White Space Opportunities**:
   - Underserved segments
   - Gaps in our coverage
   - Emerging opportunities

6. **Strategic Recommendations**:
   - Which managers to prioritize
   - Portfolio construction suggestions
   - Diversification opportunities"""

        model = self.models.get('deal_analysis', 'deepseek-r1')
        result = self.llm_service.chat(prompt, model=model, temperature=0.3, max_tokens=6144)

        return {
            'timestamp': datetime.now().isoformat(),
            'managers_analyzed': len(managers_data),
            'analysis': result['response'],
            'model_used': result['model']
        }

    def identify_deal_patterns(self, deals_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify patterns in deal flow and investment trends"""

        prompt = f"""Analyze these investment deals and identify key patterns and trends.

DEALS DATA:
{json.dumps(deals_data, indent=2)[:10000]}...

Identify:

1. **Hot Sectors**: Which sectors are getting most investment?
2. **Stage Trends**: Which stages are most active?
3. **Valuation Trends**: Are valuations up/down?
4. **Deal Size Trends**: Average deal sizes by stage
5. **Geographic Patterns**: Where are deals concentrated?
6. **Emerging Trends**: What new themes are appearing?
7. **Syndicate Patterns**: Who's investing together?
8. **Timing Patterns**: When are most deals happening?

Provide actionable insights and recommendations."""

        model = self.models.get('deal_patterns', 'qwen2.5')
        result = self.llm_service.chat(prompt, model=model, temperature=0.5, max_tokens=4096)

        return {
            'timestamp': datetime.now().isoformat(),
            'deals_analyzed': len(deals_data),
            'analysis': result['response'],
            'model_used': result['model']
        }

    def analyze_portfolio_overlap(self, funds: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze portfolio company overlap across our funds"""

        prompt = f"""Analyze portfolio overlap across these funds to assess diversification and correlation risk.

FUNDS DATA:
{json.dumps(funds, indent=2)[:10000]}...

Analyze:

1. **Portfolio Overlap**:
   - Which companies appear in multiple portfolios?
   - Level of overlap (high/medium/low)

2. **Correlation Risk**:
   - Are our funds correlated?
   - Concentration in specific companies
   - Sector correlation

3. **Diversification Assessment**:
   - Are we actually diversified?
   - Hidden concentrations
   - Recommendations to improve diversification

4. **Co-Investment Analysis**:
   - Which managers co-invest most frequently?
   - Quality of co-investment partners

5. **Risk Assessment**:
   - What if a major portfolio company fails?
   - Correlated failure scenarios
   - Mitigation strategies"""

        model = self.models.get('deal_analysis', 'deepseek-r1')
        result = self.llm_service.chat(prompt, model=model, temperature=0.3, max_tokens=4096)

        return {
            'timestamp': datetime.now().isoformat(),
            'funds_analyzed': len(funds),
            'analysis': result['response'],
            'model_used': result['model']
        }


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Deal Intelligence')
    parser.add_argument('command', choices=['analyze-universe', 'deal-patterns', 'portfolio-overlap'])
    parser.add_argument('--data', required=True, help='Path to data JSON file')

    args = parser.parse_args()

    deal_intel = DealIntelligence()

    with open(args.data, 'r') as f:
        data = json.load(f)

    if args.command == 'analyze-universe':
        result = deal_intel.analyze_manager_universe(data)
    elif args.command == 'deal-patterns':
        result = deal_intel.identify_deal_patterns(data)
    elif args.command == 'portfolio-overlap':
        result = deal_intel.analyze_portfolio_overlap(data)

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Document Intelligence Module - Metal.ai Inspired

Process financial documents (pitch decks, LPAs, DD reports) and extract insights.
Uses local LLMs for analysis.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "core" / "scripts"))
from llm_service import LLMService


class DocumentIntelligence:
    """Document analysis using AI/LLM capabilities"""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize document intelligence service"""
        self.llm_service = LLMService()

        # Load Metal AI config
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "metal_ai_config.yaml"

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.models = self.config.get('models', {})

    def analyze_pitch_deck(self, deck_content: str, company_name: str = "Unknown") -> Dict[str, Any]:
        """
        Analyze a pitch deck and extract key information

        Args:
            deck_content: Text content of the pitch deck
            company_name: Name of the company

        Returns:
            Dict with extracted information
        """
        prompt = f"""Analyze this pitch deck for {company_name} and extract key information.

PITCH DECK CONTENT:
{deck_content}

Please provide a structured analysis covering:

1. **Executive Summary** (2-3 sentences)
2. **Team**:
   - Founders and key team members
   - Relevant experience
   - Team gaps (if any)

3. **Market Opportunity**:
   - Target market size (TAM/SAM/SOM if mentioned)
   - Market trends
   - Growth drivers

4. **Product/Service**:
   - What they do (in plain English)
   - Key features
   - Competitive advantages

5. **Traction**:
   - Revenue metrics
   - User/customer metrics
   - Growth rates
   - Key milestones

6. **Business Model**:
   - How they make money
   - Unit economics (if provided)
   - Revenue streams

7. **Competition**:
   - Key competitors
   - Differentiation

8. **The Ask**:
   - Funding amount requested
   - Use of funds
   - Valuation (if mentioned)

9. **Investment Highlights** (3-5 bullets of most compelling points)

10. **Key Risks** (3-5 main concerns or red flags)

11. **Investment Recommendation**:
    - Rating: Strong Pass / Pass / Consider / Interesting / Strong Interest
    - Rationale: 2-3 sentences

Format the response as structured JSON."""

        model = self.models.get('document_analysis', 'deepseek-r1')
        result = self.llm_service.chat(prompt, model=model, temperature=0.3, max_tokens=8192)

        return {
            'company': company_name,
            'timestamp': datetime.now().isoformat(),
            'analysis': result['response'],
            'model_used': result['model'],
            'document_type': 'pitch_deck'
        }

    def analyze_lpa(self, lpa_content: str, fund_name: str = "Unknown Fund") -> Dict[str, Any]:
        """
        Analyze a Limited Partnership Agreement (LPA) and extract key terms

        Args:
            lpa_content: Text content of the LPA
            fund_name: Name of the fund

        Returns:
            Dict with extracted information
        """
        prompt = f"""Analyze this Limited Partnership Agreement (LPA) for {fund_name} and extract key terms.

LPA CONTENT:
{lpa_content}

Please provide a structured analysis covering:

1. **Fund Structure**:
   - Fund size (total commitments)
   - Investment period
   - Fund term
   - Extension options

2. **Economics**:
   - Management fee (rate, calculation basis, step-downs)
   - Carried interest (rate, hurdle, catch-up)
   - GP commitment
   - Key person clause

3. **Investment Restrictions**:
   - Maximum position size
   - Geographic restrictions
   - Sector restrictions
   - Stage restrictions
   - Follow-on reserves

4. **Governance**:
   - Advisory board rights
   - LP approval rights (major decisions)
   - GP removal provisions
   - LPAC role

5. **Distribution Waterfall**:
   - Deal-by-deal or fund-level
   - Preferred return (hurdle rate)
   - Catch-up provisions
   - Carry distribution

6. **LP Rights**:
   - Information rights
   - Co-investment rights
   - Transfer restrictions
   - Withdrawal rights

7. **Red Flags** (if any):
   - Unusual terms
   - GP-favorable provisions
   - Missing standard protections

8. **Compared to Market Standards**:
   - Terms better than market
   - Terms worse than market
   - Standard terms

9. **Negotiation Opportunities** (3-5 terms we might negotiate)

10. **Overall Assessment**:
    - Rating: Strong Pass / Pass / Fair / Good / Excellent
    - Key concerns (if any)
    - Recommendation

Format the response as structured JSON where possible."""

        model = self.models.get('document_analysis', 'deepseek-r1')
        result = self.llm_service.chat(prompt, model=model, temperature=0.3, max_tokens=8192)

        return {
            'fund': fund_name,
            'timestamp': datetime.now().isoformat(),
            'analysis': result['response'],
            'model_used': result['model'],
            'document_type': 'lpa'
        }

    def analyze_dd_report(self, report_content: str, manager_name: str = "Unknown") -> Dict[str, Any]:
        """
        Analyze a due diligence report and extract key findings

        Args:
            report_content: Text content of the DD report
            manager_name: Name of the manager

        Returns:
            Dict with extracted information
        """
        prompt = f"""Analyze this due diligence report for {manager_name} and extract key findings.

DUE DILIGENCE REPORT:
{report_content}

Please provide a structured analysis covering:

1. **Executive Summary** (3-4 sentences)

2. **Investment Strengths** (5-7 key positives):
   - Rank by importance
   - Provide evidence/specifics

3. **Investment Concerns** (5-7 key risks):
   - Rank by severity
   - Mitigation strategies (if mentioned)

4. **Track Record Analysis**:
   - Historical performance (IRR, MOIC, DPI)
   - vs. Benchmark
   - Consistency across vintages
   - Notable exits
   - Notable failures

5. **Team Assessment**:
   - Key strengths
   - Team gaps or concerns
   - Organizational structure
   - Compensation structure

6. **Investment Process**:
   - Deal sourcing (quality of pipeline)
   - Decision-making process
   - Value-add capabilities
   - Portfolio support

7. **Operations Review**:
   - Back-office capabilities
   - Compliance/legal
   - Fund administration
   - Reporting quality

8. **Reference Check Summary**:
   - Overall sentiment
   - Key themes
   - Red flags (if any)
   - Enthusiastic supporters

9. **Portfolio Company Visits**:
   - Key takeaways
   - Portfolio quality
   - Manager value-add evidence

10. **Competitive Positioning**:
    - Differentiation vs. peers
    - Sustainable competitive advantages

11. **Red Flags** (if any):
    - Critical concerns
    - Deal-breakers
    - Items requiring follow-up

12. **Investment Committee Recommendation**:
    - Recommendation: Strong Pass / Pass / More DD Needed / Proceed / Strong Proceed
    - Conviction level: Low / Medium / High
    - Proposed commitment size
    - Key conditions or contingencies
    - Rationale (3-5 sentences)

Format the response as structured analysis."""

        model = self.models.get('document_analysis', 'deepseek-r1')
        result = self.llm_service.chat(prompt, model=model, temperature=0.3, max_tokens=8192)

        return {
            'manager': manager_name,
            'timestamp': datetime.now().isoformat(),
            'analysis': result['response'],
            'model_used': result['model'],
            'document_type': 'dd_report'
        }

    def extract_key_metrics(self, document_content: str, doc_type: str = 'general') -> Dict[str, Any]:
        """
        Extract key financial metrics from any document

        Args:
            document_content: Text content
            doc_type: Type of document (pitch_deck, quarterly_report, etc.)

        Returns:
            Dict with extracted metrics
        """
        prompt = f"""Extract all key financial and performance metrics from this document.

DOCUMENT CONTENT:
{doc_content}

Extract and structure:

1. **Financial Metrics**:
   - Revenue (ARR, MRR, total)
   - Growth rates
   - Burn rate / runway
   - Profitability metrics
   - Unit economics

2. **Performance Metrics**:
   - IRR, MOIC, DPI, TVPI, RVPI (if VC/PE fund)
   - Customer metrics (CAC, LTV, churn)
   - User metrics
   - Market share

3. **Fund Metrics** (if applicable):
   - AUM
   - Fund size
   - Management fee
   - Carry
   - Vintage year

4. **Valuation**:
   - Current valuation
   - Last round details
   - Revenue multiples

Return as structured JSON with all numerical values."""

        model = self.models.get('document_extraction', 'deepseek-coder')
        result = self.llm_service.chat(prompt, model=model, temperature=0.1, max_tokens=4096)

        return {
            'timestamp': datetime.now().isoformat(),
            'metrics': result['response'],
            'model_used': result['model'],
            'doc_type': doc_type
        }

    def compare_documents(self, documents: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Compare multiple documents side-by-side

        Args:
            documents: List of dicts with 'name' and 'content' keys

        Returns:
            Comparative analysis
        """
        # Build comparison prompt
        doc_summaries = []
        for i, doc in enumerate(documents, 1):
            doc_summaries.append(f"### Document {i}: {doc['name']}\n{doc['content'][:3000]}...")

        prompt = f"""Compare these documents side-by-side and provide a structured analysis.

{chr(10).join(doc_summaries)}

Provide:

1. **Key Similarities** (5-7 points)
2. **Key Differences** (5-7 points)
3. **Relative Strengths** (which document/entity is stronger in what areas)
4. **Competitive Positioning** (how do they compare to each other)
5. **Investment Ranking** (if these are investment opportunities, rank them with rationale)
6. **Summary Recommendation** (which would you choose and why)

Be specific and quantitative where possible."""

        model = self.models.get('document_analysis', 'deepseek-r1')
        result = self.llm_service.chat(prompt, model=model, temperature=0.3, max_tokens=8192)

        return {
            'timestamp': datetime.now().isoformat(),
            'documents_compared': [doc['name'] for doc in documents],
            'comparison': result['response'],
            'model_used': result['model']
        }

    def generate_summary(self, document_content: str, max_length: str = 'medium') -> Dict[str, Any]:
        """
        Generate an executive summary of a document

        Args:
            document_content: Text content
            max_length: short (1 paragraph), medium (2-3 paragraphs), long (1 page)

        Returns:
            Summary
        """
        length_instructions = {
            'short': '1 paragraph (3-5 sentences)',
            'medium': '2-3 paragraphs (8-12 sentences)',
            'long': '1 page executive summary (4-5 paragraphs)'
        }

        prompt = f"""Generate a {length_instructions.get(max_length, 'medium')} executive summary of this document.

DOCUMENT:
{document_content}

Focus on:
- What is this document about?
- What are the key takeaways?
- What are the most important points a busy executive should know?
- Any critical risks or opportunities?

Write clearly and concisely."""

        model = self.models.get('document_summary', 'phi4')
        result = self.llm_service.chat(prompt, model=model, temperature=0.7, max_tokens=2048)

        return {
            'timestamp': datetime.now().isoformat(),
            'summary': result['response'],
            'length': max_length,
            'model_used': result['model']
        }


def main():
    """CLI interface for testing"""
    import argparse

    parser = argparse.ArgumentParser(description='Document Intelligence - Metal.ai Style')
    parser.add_argument('command', choices=['analyze-pitch', 'analyze-lpa', 'analyze-dd', 'extract-metrics', 'summary'])
    parser.add_argument('--file', required=True, help='Path to document file')
    parser.add_argument('--name', help='Company/Fund/Manager name')
    parser.add_argument('--type', help='Document type', default='general')
    parser.add_argument('--length', help='Summary length', choices=['short', 'medium', 'long'], default='medium')

    args = parser.parse_args()

    # Read document
    with open(args.file, 'r') as f:
        content = f.read()

    # Initialize service
    doc_intel = DocumentIntelligence()

    # Execute command
    if args.command == 'analyze-pitch':
        result = doc_intel.analyze_pitch_deck(content, args.name or "Unknown")
    elif args.command == 'analyze-lpa':
        result = doc_intel.analyze_lpa(content, args.name or "Unknown Fund")
    elif args.command == 'analyze-dd':
        result = doc_intel.analyze_dd_report(content, args.name or "Unknown Manager")
    elif args.command == 'extract-metrics':
        result = doc_intel.extract_key_metrics(content, args.type)
    elif args.command == 'summary':
        result = doc_intel.generate_summary(content, args.length)

    # Print result
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

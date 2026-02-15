#!/usr/bin/env python3
"""
Due Diligence Workflows - Metal.ai Inspired

Automated DD checklists, analysis, and IC memo generation for fund managers.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import yaml
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "core" / "scripts"))
from llm_service import LLMService


class DueDiligenceWorkflow:
    """Due diligence workflow management and automation"""

    # Standard 8-week DD checklist
    DD_CHECKLIST = {
        "Week 1-2: Initial Screening": [
            "Initial call with GP (1-2 hours)",
            "Review fund marketing materials",
            "Review track record data",
            "Preliminary team assessment",
            "Investment thesis validation",
            "Screen for red flags",
            "Go/No-Go decision"
        ],
        "Week 3-4: Deep Dive": [
            "Track record verification (3rd party data)",
            "Detailed performance analysis",
            "Investment strategy deep dive",
            "Portfolio construction review",
            "Operations assessment",
            "Reference checks initiated (3-5 LPs)",
            "Legal/compliance review started"
        ],
        "Week 5-6: Field Work": [
            "Portfolio company visits (3-5 companies)",
            "Management team meetings",
            "Co-investor interviews",
            "Competitive landscape analysis",
            "Market positioning assessment",
            "Value-add validation"
        ],
        "Week 7-8: IC Preparation": [
            "Reference checks completed",
            "Legal review completed (LPA, side letters)",
            "IC memo drafted",
            "Risk analysis finalized",
            "Terms negotiation",
            "IC presentation prep",
            "IC meeting scheduled"
        ]
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize DD workflow service"""
        self.llm_service = LLMService()

        # Load Metal AI config
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "metal_ai_config.yaml"

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.models = self.config.get('models', {})

    def create_dd_workflow(self, manager_name: str, fund_name: str,
                          start_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Create an 8-week DD workflow with checklist

        Args:
            manager_name: Name of the manager
            fund_name: Name of the fund
            start_date: ISO format date (defaults to today)

        Returns:
            DD workflow with timeline and checklist
        """
        if start_date is None:
            start_date = datetime.now()
        else:
            start_date = datetime.fromisoformat(start_date)

        workflow = {
            'manager': manager_name,
            'fund': fund_name,
            'start_date': start_date.isoformat(),
            'end_date': (start_date + timedelta(weeks=8)).isoformat(),
            'status': 'not_started',
            'created_at': datetime.now().isoformat(),
            'phases': []
        }

        # Build phase-by-phase workflow
        current_date = start_date
        for phase_name, tasks in self.DD_CHECKLIST.items():
            phase = {
                'phase': phase_name,
                'start': current_date.isoformat(),
                'end': (current_date + timedelta(weeks=2)).isoformat(),
                'tasks': [
                    {
                        'task': task,
                        'status': 'pending',
                        'assigned_to': None,
                        'due_date': (current_date + timedelta(weeks=1)).isoformat(),
                        'completed_date': None,
                        'notes': ''
                    }
                    for task in tasks
                ]
            }
            workflow['phases'].append(phase)
            current_date += timedelta(weeks=2)

        return workflow

    def generate_ic_memo(self, dd_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Investment Committee memo from DD data

        Args:
            dd_data: Dictionary with all DD findings
                - manager_name
                - fund_name
                - track_record
                - team_assessment
                - reference_checks
                - portfolio_visits
                - operations_review
                - strengths
                - risks
                - recommendation

        Returns:
            IC memo content
        """
        prompt = f"""Generate a comprehensive Investment Committee memo for a fund-of-funds investment decision.

MANAGER: {dd_data.get('manager_name', 'Unknown')}
FUND: {dd_data.get('fund_name', 'Unknown Fund')}

DUE DILIGENCE FINDINGS:

**Track Record:**
{dd_data.get('track_record', 'Not provided')}

**Team Assessment:**
{dd_data.get('team_assessment', 'Not provided')}

**Reference Checks:**
{dd_data.get('reference_checks', 'Not provided')}

**Portfolio Company Visits:**
{dd_data.get('portfolio_visits', 'Not provided')}

**Operations Review:**
{dd_data.get('operations_review', 'Not provided')}

**Key Strengths:**
{dd_data.get('strengths', 'Not provided')}

**Key Risks:**
{dd_data.get('risks', 'Not provided')}

Generate a professional IC memo with:

# Investment Committee Memorandum

## Executive Summary
(3-4 paragraphs covering: who, what, why, recommendation)

## Investment Thesis
(Why this manager/fund? What's the opportunity?)

## Manager Overview
- Firm background
- Investment strategy
- Target returns
- Differentiation

## Team Assessment
- Key team members and backgrounds
- Team strengths
- Team gaps or concerns
- Organizational structure

## Track Record Analysis
- Historical performance (IRR, MOIC, DPI)
- Performance vs. benchmark
- Consistency across vintages
- Notable exits and realizations
- Attribution analysis

## Investment Process
- Deal sourcing
- Investment decision-making
- Portfolio management
- Value creation strategies

## Reference Check Summary
- Number of references checked
- Overall sentiment
- Key themes
- Notable endorsements
- Concerns raised (if any)

## Portfolio Quality Assessment
- Companies visited
- Portfolio health
- Manager value-add evidence
- Exit prospects

## Operations & Governance
- Fund administration
- Compliance and legal
- Reporting capabilities
- Back-office assessment

## Terms Summary
- Fund size
- Management fee
- Carried interest
- GP commit
- Key terms
- Notable provisions

## Risk Assessment

### Key Risks:
1. [Risk 1] - Severity: High/Medium/Low
   - Mitigation: [How to address]

2. [Risk 2] - Severity: High/Medium/Low
   - Mitigation: [How to address]

(Continue for all major risks)

## Competitive Positioning
- How does this manager compare to peers?
- Sustainable competitive advantages
- Market positioning

## Investment Highlights
1. [Most compelling reason]
2. [Second compelling reason]
3. [Third compelling reason]
(Continue for 5-7 key highlights)

## Proposed Terms
- Commitment size: $X million
- Target ownership: X% of fund
- Special provisions requested (if any)

## Investment Recommendation

**Recommendation:** PASS / PROCEED / STRONG PROCEED

**Conviction Level:** LOW / MEDIUM / HIGH

**Rationale:**
(3-5 paragraphs explaining the recommendation, balancing risks and opportunities)

**Vote Request:**
We request IC approval to commit $X million to [Fund Name] by [Manager Name].

---

Make this memo professional, thorough, and balanced. Include both positives and concerns.
Use clear section headers and bullet points where appropriate."""

        model = self.models.get('dd_memo_writing', 'phi4')
        result = self.llm_service.chat(prompt, model=model, temperature=0.7, max_tokens=8192)

        return {
            'manager': dd_data.get('manager_name'),
            'fund': dd_data.get('fund_name'),
            'timestamp': datetime.now().isoformat(),
            'memo': result['response'],
            'model_used': result['model'],
            'recommendation': dd_data.get('recommendation', 'PROCEED')
        }

    def analyze_reference_checks(self, references: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Synthesize multiple reference check interviews

        Args:
            references: List of dicts with 'name', 'role', 'feedback' keys

        Returns:
            Synthesized analysis
        """
        ref_summaries = []
        for i, ref in enumerate(references, 1):
            ref_summaries.append(f"""
**Reference {i}: {ref.get('name', 'Anonymous')} - {ref.get('role', 'LP')}**

{ref.get('feedback', 'No feedback provided')}
""")

        prompt = f"""Analyze these reference check interviews and provide a comprehensive synthesis.

REFERENCE CHECKS:
{chr(10).join(ref_summaries)}

Provide:

## Reference Check Summary

### Overall Sentiment
(Positive / Mixed / Negative with explanation)

### Consensus Themes
(3-5 themes that appeared across multiple references)

### Key Strengths Identified
(5-7 strengths mentioned by references)

### Concerns Raised
(Any concerns or criticisms, even minor ones)

### Notable Endorsements
(Particularly strong endorsements or testimonials)

### Outlier Views
(Any reference that disagreed with the consensus)

### Questions for Follow-up
(3-5 questions raised by reference checks that need clarification)

### Red Flags
(Any serious concerns that would affect investment decision)

### Reference Quality Assessment
(Were these high-quality references? Any bias concerns?)

### Bottom Line
(What do these references tell us about this manager? Should we proceed?)

Be objective and highlight both positive and negative feedback."""

        model = self.models.get('dd_analysis', 'deepseek-r1')
        result = self.llm_service.chat(prompt, model=model, temperature=0.3, max_tokens=4096)

        return {
            'timestamp': datetime.now().isoformat(),
            'references_analyzed': len(references),
            'analysis': result['response'],
            'model_used': result['model']
        }

    def identify_red_flags(self, dd_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify potential red flags from all DD data

        Args:
            dd_data: All due diligence data collected

        Returns:
            Red flag analysis with severity ratings
        """
        prompt = f"""Analyze this due diligence data and identify any red flags or concerns.

DUE DILIGENCE DATA:
{json.dumps(dd_data, indent=2)}

For each red flag identified, provide:

1. **Red Flag Description**
2. **Severity**: Critical / High / Medium / Low
3. **Evidence**: What specifically suggests this is a concern?
4. **Potential Impact**: What could go wrong?
5. **Mitigation**: Can this be addressed? How?
6. **Recommendation**: Pass / Proceed with caution / Acceptable risk

Categories to consider:
- Track record issues (performance, consistency)
- Team risks (departures, experience gaps, key person)
- Process concerns (deal sourcing, decision-making)
- Operations issues (compliance, reporting, administration)
- Terms problems (unfavorable provisions)
- Reference check concerns
- Portfolio quality issues
- Market/competitive risks
- Financial risks (fund size, economics)

Be thorough but balanced. Not every concern is a deal-breaker.

Conclude with:
- **Critical Red Flags** (deal-breakers)
- **Manageable Concerns** (proceed with caution)
- **Overall Risk Assessment**: Pass / High Risk / Medium Risk / Low Risk
- **Proceed/No-Go Recommendation**"""

        model = self.models.get('dd_analysis', 'deepseek-r1')
        result = self.llm_service.chat(prompt, model=model, temperature=0.3, max_tokens=4096)

        return {
            'timestamp': datetime.now().isoformat(),
            'analysis': result['response'],
            'model_used': result['model']
        }

    def generate_dd_questions(self, focus_area: str, context: str = "") -> Dict[str, Any]:
        """
        Generate due diligence questions for specific focus areas

        Args:
            focus_area: track_record, team, process, operations, terms, portfolio
            context: Additional context about the manager

        Returns:
            List of DD questions
        """
        focus_prompts = {
            'track_record': 'performance history, MOIC, IRR, DPI, consistency across funds',
            'team': 'team composition, experience, track record, compensation, retention',
            'process': 'deal sourcing, investment decision-making, portfolio management, value creation',
            'operations': 'fund administration, compliance, reporting, back-office',
            'terms': 'LPA terms, fees, carry, GP commit, rights and restrictions',
            'portfolio': 'portfolio company quality, exits, current holdings, company visits'
        }

        prompt = f"""Generate comprehensive due diligence questions focused on: {focus_area}

Context: {focus_prompts.get(focus_area, focus_area)}

{f"Additional context: {context}" if context else ""}

Generate 15-20 specific, probing questions organized by sub-topic.
Questions should be:
- Specific and actionable (not vague)
- Designed to reveal risks and strengths
- Open-ended to encourage detailed responses
- Focused on facts and evidence
- Appropriate for GP interviews or LP references

Format as organized list with sub-categories."""

        model = self.models.get('dd_updates', 'mistral')
        result = self.llm_service.chat(prompt, model=model, temperature=0.7, max_tokens=2048)

        return {
            'focus_area': focus_area,
            'timestamp': datetime.now().isoformat(),
            'questions': result['response'],
            'model_used': result['model']
        }


def main():
    """CLI interface for testing"""
    import argparse

    parser = argparse.ArgumentParser(description='Due Diligence Workflows')
    parser.add_argument('command', choices=['create-workflow', 'generate-memo', 'analyze-refs', 'red-flags', 'questions'])
    parser.add_argument('--manager', help='Manager name')
    parser.add_argument('--fund', help='Fund name')
    parser.add_argument('--data', help='Path to DD data JSON file')
    parser.add_argument('--focus', help='Focus area for questions',
                       choices=['track_record', 'team', 'process', 'operations', 'terms', 'portfolio'])

    args = parser.parse_args()

    dd_workflow = DueDiligenceWorkflow()

    if args.command == 'create-workflow':
        result = dd_workflow.create_dd_workflow(args.manager or "Test Manager",
                                               args.fund or "Test Fund")
    elif args.command == 'generate-memo':
        with open(args.data, 'r') as f:
            dd_data = json.load(f)
        result = dd_workflow.generate_ic_memo(dd_data)
    elif args.command == 'analyze-refs':
        with open(args.data, 'r') as f:
            references = json.load(f)
        result = dd_workflow.analyze_reference_checks(references)
    elif args.command == 'red-flags':
        with open(args.data, 'r') as f:
            dd_data = json.load(f)
        result = dd_workflow.identify_red_flags(dd_data)
    elif args.command == 'questions':
        result = dd_workflow.generate_dd_questions(args.focus or 'team')

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

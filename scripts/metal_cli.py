#!/usr/bin/env python3
"""
Metal AI CLI - Unified interface for Metal.ai capabilities

Usage:
    ./metal_cli.py document analyze-pitch --file deck.txt --name "TechCorp"
    ./metal_cli.py dd create-workflow --manager "Sequoia" --fund "Fund XX"
    ./metal_cli.py dd generate-memo --data dd_findings.json
    ./metal_cli.py deal analyze-universe --data managers.json
    ./metal_cli.py search "Show me all seed stage AI funds"
    ./metal_cli.py market sector-trends
    ./metal_cli.py lp quarterly-letter --quarter Q1-2026 --data portfolio.json
"""

import sys
import argparse
import json
from pathlib import Path

# Add metal_ai to path
sys.path.insert(0, str(Path(__file__).parent))

from metal_ai.document_intelligence import DocumentIntelligence
from metal_ai.due_diligence import DueDiligenceWorkflow
from metal_ai.deal_intelligence import DealIntelligence
from metal_ai.knowledge_graph import KnowledgeGraph
from metal_ai.market_intelligence import MarketIntelligence
from metal_ai.lp_reporting import LPReporting


def setup_parser():
    """Setup argument parser with all commands"""
    parser = argparse.ArgumentParser(
        description='Metal AI CLI - Institutional Intelligence for NEWCO',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Document Intelligence
  ./metal_cli.py document analyze-pitch --file pitch_deck.txt --name "Acme Inc"
  ./metal_cli.py document analyze-lpa --file lpa.txt --name "Fund X"
  ./metal_cli.py document analyze-dd --file dd_report.txt --name "Manager Y"
  ./metal_cli.py document summary --file document.txt --length medium

  # Due Diligence
  ./metal_cli.py dd create-workflow --manager "Sequoia" --fund "Fund XX"
  ./metal_cli.py dd generate-memo --data dd_findings.json
  ./metal_cli.py dd analyze-refs --data references.json
  ./metal_cli.py dd red-flags --data dd_data.json
  ./metal_cli.py dd questions --focus team

  # Deal Intelligence
  ./metal_cli.py deal analyze-universe --data managers.json
  ./metal_cli.py deal patterns --data deals.json
  ./metal_cli.py deal portfolio-overlap --data funds.json

  # Knowledge Search
  ./metal_cli.py search "Show me all seed stage SaaS funds with IRR > 25%"

  # Market Intelligence
  ./metal_cli.py market sector-trends
  ./metal_cli.py market sector-trends --data market_data.txt

  # LP Reporting
  ./metal_cli.py lp quarterly-letter --quarter Q1-2026 --data portfolio.json --notes ceo_notes.txt
        """
    )

    subparsers = parser.add_subparsers(dest='module', help='Module to use')

    # Document Intelligence
    doc_parser = subparsers.add_parser('document', help='Document intelligence')
    doc_sub = doc_parser.add_subparsers(dest='command')

    doc_pitch = doc_sub.add_parser('analyze-pitch', help='Analyze pitch deck')
    doc_pitch.add_argument('--file', required=True, help='Path to document')
    doc_pitch.add_argument('--name', required=True, help='Company name')

    doc_lpa = doc_sub.add_parser('analyze-lpa', help='Analyze LPA')
    doc_lpa.add_argument('--file', required=True, help='Path to LPA')
    doc_lpa.add_argument('--name', required=True, help='Fund name')

    doc_dd = doc_sub.add_parser('analyze-dd', help='Analyze DD report')
    doc_dd.add_argument('--file', required=True, help='Path to DD report')
    doc_dd.add_argument('--name', required=True, help='Manager name')

    doc_summary = doc_sub.add_parser('summary', help='Generate summary')
    doc_summary.add_argument('--file', required=True, help='Path to document')
    doc_summary.add_argument('--length', choices=['short', 'medium', 'long'], default='medium')

    # Due Diligence
    dd_parser = subparsers.add_parser('dd', help='Due diligence workflows')
    dd_sub = dd_parser.add_subparsers(dest='command')

    dd_workflow = dd_sub.add_parser('create-workflow', help='Create DD workflow')
    dd_workflow.add_argument('--manager', required=True, help='Manager name')
    dd_workflow.add_argument('--fund', required=True, help='Fund name')

    dd_memo = dd_sub.add_parser('generate-memo', help='Generate IC memo')
    dd_memo.add_argument('--data', required=True, help='Path to DD data JSON')

    dd_refs = dd_sub.add_parser('analyze-refs', help='Analyze reference checks')
    dd_refs.add_argument('--data', required=True, help='Path to references JSON')

    dd_flags = dd_sub.add_parser('red-flags', help='Identify red flags')
    dd_flags.add_argument('--data', required=True, help='Path to DD data JSON')

    dd_questions = dd_sub.add_parser('questions', help='Generate DD questions')
    dd_questions.add_argument('--focus', required=True,
                             choices=['track_record', 'team', 'process', 'operations', 'terms', 'portfolio'])

    # Deal Intelligence
    deal_parser = subparsers.add_parser('deal', help='Deal intelligence')
    deal_sub = deal_parser.add_subparsers(dest='command')

    deal_universe = deal_sub.add_parser('analyze-universe', help='Analyze manager universe')
    deal_universe.add_argument('--data', required=True, help='Path to managers data JSON')

    deal_patterns = deal_sub.add_parser('patterns', help='Identify deal patterns')
    deal_patterns.add_argument('--data', required=True, help='Path to deals data JSON')

    deal_overlap = deal_sub.add_parser('portfolio-overlap', help='Analyze portfolio overlap')
    deal_overlap.add_argument('--data', required=True, help='Path to funds data JSON')

    # Search
    search_parser = subparsers.add_parser('search', help='Knowledge graph search')
    search_parser.add_argument('query', help='Natural language query')
    search_parser.add_argument('--data', help='Path to context data file')

    # Market Intelligence
    market_parser = subparsers.add_parser('market', help='Market intelligence')
    market_sub = market_parser.add_subparsers(dest='command')

    market_trends = market_sub.add_parser('sector-trends', help='Analyze sector trends')
    market_trends.add_argument('--data', help='Path to market data file')

    # LP Reporting
    lp_parser = subparsers.add_parser('lp', help='LP reporting')
    lp_sub = lp_parser.add_subparsers(dest='command')

    lp_letter = lp_sub.add_parser('quarterly-letter', help='Generate quarterly letter')
    lp_letter.add_argument('--quarter', required=True, help='Quarter (e.g., Q1-2026)')
    lp_letter.add_argument('--data', required=True, help='Path to portfolio data JSON')
    lp_letter.add_argument('--notes', help='Path to CEO notes file')

    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()

    if not args.module:
        parser.print_help()
        sys.exit(1)

    try:
        # Document Intelligence
        if args.module == 'document':
            doc_intel = DocumentIntelligence()

            with open(args.file, 'r') as f:
                content = f.read()

            if args.command == 'analyze-pitch':
                result = doc_intel.analyze_pitch_deck(content, args.name)
            elif args.command == 'analyze-lpa':
                result = doc_intel.analyze_lpa(content, args.name)
            elif args.command == 'analyze-dd':
                result = doc_intel.analyze_dd_report(content, args.name)
            elif args.command == 'summary':
                result = doc_intel.generate_summary(content, args.length)

            print(json.dumps(result, indent=2))

        # Due Diligence
        elif args.module == 'dd':
            dd_workflow = DueDiligenceWorkflow()

            if args.command == 'create-workflow':
                result = dd_workflow.create_dd_workflow(args.manager, args.fund)
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
                result = dd_workflow.generate_dd_questions(args.focus)

            print(json.dumps(result, indent=2))

        # Deal Intelligence
        elif args.module == 'deal':
            deal_intel = DealIntelligence()

            with open(args.data, 'r') as f:
                data = json.load(f)

            if args.command == 'analyze-universe':
                result = deal_intel.analyze_manager_universe(data)
            elif args.command == 'patterns':
                result = deal_intel.identify_deal_patterns(data)
            elif args.command == 'portfolio-overlap':
                result = deal_intel.analyze_portfolio_overlap(data)

            print(json.dumps(result, indent=2))

        # Search
        elif args.module == 'search':
            kg = KnowledgeGraph()

            context = ""
            if args.data:
                with open(args.data, 'r') as f:
                    context = f.read()

            result = kg.search(args.query, context)
            print(result['answer'])

        # Market Intelligence
        elif args.module == 'market':
            market_intel = MarketIntelligence()

            market_data = ""
            if hasattr(args, 'data') and args.data:
                with open(args.data, 'r') as f:
                    market_data = f.read()

            if args.command == 'sector-trends':
                result = market_intel.analyze_sector_trends(market_data)
                print(result['analysis'])

        # LP Reporting
        elif args.module == 'lp':
            lp_reporting = LPReporting()

            with open(args.data, 'r') as f:
                portfolio_data = json.load(f)

            ceo_notes = ""
            if hasattr(args, 'notes') and args.notes:
                with open(args.notes, 'r') as f:
                    ceo_notes = f.read()

            if args.command == 'quarterly-letter':
                result = lp_reporting.generate_quarterly_letter(args.quarter, portfolio_data, ceo_notes)
                print(result['letter'])

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

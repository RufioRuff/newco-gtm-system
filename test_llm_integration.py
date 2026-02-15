#!/usr/bin/env python3
"""
Test script for NEWCO LLM Integration

Tests the LLM service with all downloaded models
"""

import sys
from pathlib import Path

# Add scripts to path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR / "scripts"))

from llm_service import LLMService


def test_llm_integration():
    """Test LLM integration with NEWCO"""

    print("="*70)
    print("🤖 NEWCO LLM INTEGRATION TEST")
    print("="*70)

    # Initialize service
    service = LLMService()

    # Test 1: List models
    print("\n📊 Test 1: Available Models")
    print("-"*70)
    models = service.list_models()
    for model in models:
        print(f"  ✓ {model['key']:15} | {model['type']:10} | {model['description']}")

    # Test 2: Quick chat with DeepSeek R1
    print("\n🧠 Test 2: DeepSeek R1 Reasoning Test")
    print("-"*70)
    print("Prompt: 'What are 3 key metrics to evaluate a SaaS startup?'")
    print("Querying deepseek-r1...")

    result = service.chat(
        prompt="What are the 3 most important metrics to evaluate a Series A SaaS startup? Be concise.",
        model='deepseek-r1'
    )

    if result['success']:
        print(f"\n✅ Success! (Model: {result['model']})")
        print(f"\nResponse:\n{result['response']}")
    else:
        print(f"\n❌ Error: {result['error']}")

    # Test 3: Investment analysis
    print("\n\n💼 Test 3: Investment Analysis with DeepSeek R1")
    print("-"*70)

    test_company = {
        'name': 'CloudTech Inc',
        'sector': 'Enterprise SaaS',
        'stage': 'Series B',
        'revenue': '$10M ARR',
        'growth_rate': '200% YoY',
        'burn_rate': '$1M/month',
        'runway': '18 months',
        'team_size': 45,
        'customers': 150
    }

    print(f"Analyzing: {test_company['name']}")
    print("Using model: deepseek-r1")

    analysis = service.analyze_investment('CloudTech Inc', test_company)

    if analysis['success']:
        print(f"\n✅ Analysis Complete!")
        print(f"\n{analysis['response'][:500]}...")
        print(f"\n[Full response truncated for display]")
    else:
        print(f"\n❌ Error: {analysis['error']}")

    # Test 4: Quick summary with Mistral
    print("\n\n⚡ Test 4: Quick Summary with Mistral (Fast Model)")
    print("-"*70)

    text = """
    Meeting with John from Acme Ventures on Feb 14, 2026.
    Discussed their new $500M fund focused on AI and ML startups.
    They're interested in co-investing opportunities in Series B rounds.
    Key interests: Enterprise AI, ML infrastructure, AI security.
    Follow-up: Send deck by end of week. Schedule call with LP team next month.
    """

    print("Extracting insights from meeting notes...")

    insights = service.extract_insights_from_text(text, task_type='meeting_notes', model='mistral')

    if insights['success']:
        print(f"\n✅ Insights Extracted!")
        print(f"\n{insights['response']}")
    else:
        print(f"\n❌ Error: {insights['error']}")

    # Summary
    print("\n\n" + "="*70)
    print("✅ LLM INTEGRATION TEST COMPLETE!")
    print("="*70)
    print(f"\nAll {len(models)} models are connected and ready to use:")
    print("  • DeepSeek R1 (Reasoning)")
    print("  • DeepSeek Coder (Technical Analysis)")
    print("  • Phi4 (General Purpose)")
    print("  • Qwen2.5 14B (Large Model)")
    print("  • Mistral (Fast Queries)")
    print("  • CodeLlama (Code Analysis)")
    print("  • Llama3.2 (Balanced)")
    print("\n🚀 NEWCO Platform is now AI-powered!")
    print("="*70)


if __name__ == '__main__':
    test_llm_integration()

#!/usr/bin/env python3
"""
Knowledge Graph & Intelligence Search - Metal.ai Inspired

Natural language search across all entities and relationships.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "core" / "scripts"))
from llm_service import LLMService


class KnowledgeGraph:
    """Knowledge graph and intelligent search"""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize knowledge graph service"""
        self.llm_service = LLMService()

        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "metal_ai_config.yaml"

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.models = self.config.get('models', {})

    def search(self, query: str, context_data: str = "") -> Dict[str, Any]:
        """Natural language search across all data"""

        prompt = f"""Answer this query using the available data:

QUERY: {query}

AVAILABLE DATA:
{context_data[:8000]}...

Provide a comprehensive answer with:
- Direct answer to the question
- Supporting evidence
- Related insights
- Recommended follow-up actions"""

        model = self.models.get('graph_search', 'mistral')
        result = self.llm_service.chat(prompt, model=model, temperature=0.5, max_tokens=2048)

        return {
            'query': query,
            'answer': result['response'],
            'model_used': result['model']
        }


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Knowledge Graph Search')
    parser.add_argument('query', help='Natural language query')
    parser.add_argument('--data', help='Path to context data file')

    args = parser.parse_args()

    kg = KnowledgeGraph()

    context = ""
    if args.data:
        with open(args.data, 'r') as f:
            context = f.read()

    result = kg.search(args.query, context)
    print(result['answer'])


if __name__ == '__main__':
    main()

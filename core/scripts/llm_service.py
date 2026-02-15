#!/usr/bin/env python3
"""
LLM Service for NEWCO Platform

Integrates local Ollama models (DeepSeek, Phi, Qwen, etc.) with NEWCO
for AI-powered analysis, insights, and automation.
"""

import json
import subprocess
from typing import Dict, List, Optional, Any
from pathlib import Path
import yaml


class LLMService:
    """Service for interacting with local Ollama LLM models"""

    AVAILABLE_MODELS = {
        'deepseek-r1': {
            'name': 'deepseek-r1:latest',
            'type': 'reasoning',
            'description': 'Advanced reasoning and analysis model',
            'use_cases': ['investment_analysis', 'due_diligence', 'strategic_planning']
        },
        'deepseek-coder': {
            'name': 'deepseek-coder:latest',
            'type': 'coding',
            'description': 'Specialized coding and technical analysis',
            'use_cases': ['portfolio_tech_analysis', 'technical_dd', 'automation']
        },
        'phi4': {
            'name': 'phi4:latest',
            'type': 'general',
            'description': 'General purpose high-performance model',
            'use_cases': ['general_analysis', 'email_generation', 'reporting']
        },
        'qwen2.5': {
            'name': 'qwen2.5:14b',
            'type': 'general',
            'description': 'Large general-purpose model for complex tasks',
            'use_cases': ['market_analysis', 'competitive_intel', 'research']
        },
        'mistral': {
            'name': 'mistral:latest',
            'type': 'fast',
            'description': 'Fast, efficient model for quick tasks',
            'use_cases': ['quick_summaries', 'categorization', 'entity_extraction']
        },
        'codellama': {
            'name': 'codellama:latest',
            'type': 'coding',
            'description': 'Code analysis and generation',
            'use_cases': ['code_review', 'technical_analysis']
        },
        'llama3.2': {
            'name': 'llama3.2:latest',
            'type': 'general',
            'description': 'Balanced model for various tasks',
            'use_cases': ['general_purpose']
        }
    }

    def __init__(self, default_model: str = 'deepseek-r1'):
        """Initialize LLM service with default model"""
        self.default_model = default_model
        self.config_file = Path(__file__).parent.parent / "config" / "llm_config.yaml"
        self.load_config()

    def load_config(self):
        """Load LLM configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            # Default configuration
            self.config = {
                'default_model': 'deepseek-r1',
                'temperature': 0.7,
                'max_tokens': 4096,
                'task_model_mapping': {
                    'investment_analysis': 'deepseek-r1',
                    'due_diligence': 'deepseek-r1',
                    'portfolio_analysis': 'qwen2.5',
                    'email_generation': 'phi4',
                    'technical_analysis': 'deepseek-coder',
                    'quick_summary': 'mistral',
                    'market_research': 'qwen2.5',
                    'competitive_intel': 'qwen2.5'
                }
            }
            # Save default config
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                yaml.dump(self.config, f)

    def list_models(self) -> List[Dict[str, Any]]:
        """List all available models"""
        return [
            {
                'key': key,
                'name': info['name'],
                'type': info['type'],
                'description': info['description'],
                'use_cases': info['use_cases']
            }
            for key, info in self.AVAILABLE_MODELS.items()
        ]

    def chat(self,
             prompt: str,
             model: Optional[str] = None,
             context: Optional[str] = None,
             temperature: float = 0.7,
             max_tokens: int = 4096) -> Dict[str, Any]:
        """
        Send a chat request to Ollama model

        Args:
            prompt: The prompt to send to the model
            model: Model key (e.g., 'deepseek-r1', 'phi4'). If None, uses default
            context: Additional context to provide
            temperature: Model temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Dict with 'response', 'model', 'tokens' keys
        """
        # Get model name
        if model is None:
            model = self.config.get('default_model', 'deepseek-r1')

        model_info = self.AVAILABLE_MODELS.get(model)
        if not model_info:
            raise ValueError(f"Unknown model: {model}. Available: {list(self.AVAILABLE_MODELS.keys())}")

        model_name = model_info['name']

        # Build full prompt with context
        full_prompt = prompt
        if context:
            full_prompt = f"{context}\n\n{prompt}"

        # Call Ollama using subprocess
        try:
            # Use ollama run command for simplicity
            result = subprocess.run(
                ['ollama', 'run', model_name, full_prompt],
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )

            if result.returncode != 0:
                return {
                    'success': False,
                    'error': result.stderr,
                    'model': model_name
                }

            response_text = result.stdout.strip()

            return {
                'success': True,
                'response': response_text,
                'model': model_name,
                'model_key': model,
                'prompt_length': len(full_prompt)
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Request timed out after 120 seconds',
                'model': model_name
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'model': model_name
            }

    def analyze_investment(self,
                          company_name: str,
                          company_data: Dict[str, Any],
                          model: str = 'deepseek-r1') -> Dict[str, Any]:
        """
        Analyze an investment opportunity using LLM

        Args:
            company_name: Name of the company
            company_data: Dictionary with company information
            model: Model to use for analysis

        Returns:
            Analysis results
        """
        context = f"""You are an investment analyst for a venture capital fund.
Analyze the following portfolio company and provide insights."""

        prompt = f"""
Company: {company_name}

Company Data:
{json.dumps(company_data, indent=2)}

Please provide:
1. Investment Thesis Summary
2. Key Strengths
3. Key Risks
4. Competitive Position
5. Growth Potential (Rate 1-10)
6. Overall Assessment

Format your response in clear sections.
"""

        return self.chat(prompt, model=model, context=context)

    def analyze_manager(self,
                       manager_name: str,
                       manager_data: Dict[str, Any],
                       model: str = 'deepseek-r1') -> Dict[str, Any]:
        """
        Analyze a fund manager using LLM

        Args:
            manager_name: Name of the manager/fund
            manager_data: Dictionary with manager information
            model: Model to use for analysis

        Returns:
            Analysis results
        """
        context = f"""You are a due diligence analyst for a fund of funds.
Analyze the following fund manager and provide insights."""

        prompt = f"""
Manager/Fund: {manager_name}

Manager Data:
{json.dumps(manager_data, indent=2)}

Please provide:
1. Track Record Assessment
2. Investment Strategy Analysis
3. Team Evaluation
4. Risk Factors
5. Portfolio Fit (how well this fits our portfolio)
6. Due Diligence Priority (High/Medium/Low)

Format your response in clear sections.
"""

        return self.chat(prompt, model=model, context=context)

    def generate_email(self,
                      contact_data: Dict[str, Any],
                      email_type: str,
                      context: Optional[str] = None,
                      model: str = 'phi4') -> Dict[str, Any]:
        """
        Generate an email using LLM

        Args:
            contact_data: Contact information
            email_type: Type of email (intro, follow_up, update, etc.)
            context: Additional context
            model: Model to use

        Returns:
            Generated email
        """
        prompt = f"""
Generate a professional email for the following:

Email Type: {email_type}
Recipient: {contact_data.get('name', 'N/A')}
Company: {contact_data.get('company', 'N/A')}
Title: {contact_data.get('title', 'N/A')}

{f'Context: {context}' if context else ''}

Please generate a professional, concise email. Include:
- Appropriate subject line
- Professional greeting
- Clear message body
- Call to action
- Professional closing

Format as:
Subject: [subject line]

[email body]
"""

        return self.chat(prompt, model=model)

    def summarize_market_data(self,
                            market_data: Dict[str, Any],
                            model: str = 'qwen2.5') -> Dict[str, Any]:
        """
        Summarize market data and trends

        Args:
            market_data: Market information to summarize
            model: Model to use

        Returns:
            Market summary
        """
        context = "You are a market analyst. Provide clear, actionable insights."

        prompt = f"""
Analyze this market data and provide a concise summary:

{json.dumps(market_data, indent=2)}

Provide:
1. Key Trends (3-5 bullet points)
2. Market Sentiment
3. Risks to Watch
4. Opportunities
5. Recommendation (Bullish/Neutral/Bearish)
"""

        return self.chat(prompt, model=model, context=context)

    def extract_insights_from_text(self,
                                  text: str,
                                  task_type: str = 'general',
                                  model: str = 'mistral') -> Dict[str, Any]:
        """
        Extract insights from text (emails, documents, etc.)

        Args:
            text: Text to analyze
            task_type: Type of extraction (meeting_notes, email, document, etc.)
            model: Model to use

        Returns:
            Extracted insights
        """
        prompt = f"""
Analyze this {task_type} and extract key information:

{text}

Extract:
1. Key Points (bullet list)
2. Action Items (if any)
3. Important Dates/Deadlines (if any)
4. People/Companies Mentioned
5. Sentiment (Positive/Neutral/Negative)
6. Priority Level (High/Medium/Low)
"""

        return self.chat(prompt, model=model)

    def get_model_for_task(self, task_type: str) -> str:
        """Get the recommended model for a specific task type"""
        return self.config.get('task_model_mapping', {}).get(
            task_type,
            self.config.get('default_model', 'deepseek-r1')
        )


# CLI interface for testing
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='NEWCO LLM Service')
    parser.add_argument('command', choices=['list', 'chat', 'test'], help='Command to run')
    parser.add_argument('--model', help='Model to use')
    parser.add_argument('--prompt', help='Prompt to send')

    args = parser.parse_args()

    service = LLMService()

    if args.command == 'list':
        print("\n📊 Available Models:\n")
        for model in service.list_models():
            print(f"  {model['key']} ({model['name']})")
            print(f"    Type: {model['type']}")
            print(f"    Description: {model['description']}")
            print(f"    Use Cases: {', '.join(model['use_cases'])}")
            print()

    elif args.command == 'chat':
        if not args.prompt:
            print("Error: --prompt is required")
            exit(1)

        print(f"\n🤖 Querying {args.model or 'default model'}...\n")
        result = service.chat(args.prompt, model=args.model)

        if result['success']:
            print(result['response'])
            print(f"\n[Model: {result['model']}]")
        else:
            print(f"Error: {result['error']}")

    elif args.command == 'test':
        print("\n🧪 Testing LLM Service...\n")

        # Test simple query
        result = service.chat(
            "What are the top 3 factors to consider when evaluating a Series A SaaS startup?",
            model=args.model or 'deepseek-r1'
        )

        if result['success']:
            print("✅ Test successful!")
            print(f"\nModel: {result['model']}")
            print(f"\nResponse:\n{result['response']}")
        else:
            print(f"❌ Test failed: {result['error']}")

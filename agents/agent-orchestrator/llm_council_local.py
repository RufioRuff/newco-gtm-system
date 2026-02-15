#!/usr/bin/env python3
"""
NEWCO Local LLM Council - Agent #10
===================================

Multi-model deliberation system using local Ollama models.
Port: 8010

Stage 1: Multiple models provide initial responses
Stage 2: Models review and rank each other's work (anonymized)
Stage 3: Chairman model synthesizes final answer

Based on karpathy's llm-council but adapted for local Ollama.
"""

import requests
import json
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
OLLAMA_HOST = "http://localhost:11434"
PORT = 8010

# Council configuration
COUNCIL_MODELS = [
    "deepseek-r1:latest",      # Deep reasoning
    "phi4:latest",              # Fast analysis
    "qwen2.5:14b",             # Financial analysis
    "mistral:latest"           # General purpose
]

CHAIRMAN_MODEL = "deepseek-r1:latest"  # Deep reasoning for synthesis

def query_ollama(model: str, prompt: str, system: str = None) -> str:
    """Query local Ollama model"""
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        if system:
            payload["system"] = system

        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            return result.get('response', '')
        else:
            return f"[Error querying {model}]"

    except Exception as e:
        return f"[Error: {str(e)}]"

def stage1_collect_responses(query: str) -> Dict[str, str]:
    """Stage 1: Collect initial responses from all council models"""
    print("📊 Stage 1: Collecting responses from council members...")

    responses = {}
    system_prompt = "You are a financial and private equity expert. Provide detailed, insightful analysis."

    for model in COUNCIL_MODELS:
        print(f"  Querying {model}...")
        response = query_ollama(model, query, system_prompt)
        responses[model] = response

    return responses

def stage2_collect_rankings(query: str, stage1_responses: Dict[str, str]) -> Dict[str, Any]:
    """Stage 2: Models review and rank each other's work (anonymized)"""
    print("🔍 Stage 2: Collecting peer reviews...")

    # Anonymize responses
    response_labels = {}
    label_to_model = {}

    for i, (model, response) in enumerate(stage1_responses.items()):
        label = f"Response {chr(65 + i)}"  # A, B, C, D...
        response_labels[label] = response
        label_to_model[label] = model

    # Create evaluation prompt
    eval_text = "\n\n".join([f"{label}:\n{text}" for label, text in response_labels.items()])

    eval_prompt = f"""Original Query: {query}

Here are responses from different analysts (labeled anonymously):

{eval_text}

Please evaluate each response for:
1. Accuracy and factual correctness
2. Depth of insight and analysis
3. Actionability for private equity decisions
4. Completeness

Provide your evaluation, then give a FINAL RANKING of the responses from best to worst.
Format your final ranking as:
FINAL RANKING:
1. Response X
2. Response Y
3. Response Z
(etc.)"""

    rankings = {}
    system_prompt = "You are an expert evaluator. Be objective and thorough in your assessment."

    for model in COUNCIL_MODELS:
        print(f"  {model} evaluating...")
        evaluation = query_ollama(model, eval_prompt, system_prompt)
        rankings[model] = {
            "raw_evaluation": evaluation,
            "parsed_ranking": parse_ranking(evaluation)
        }

    return {
        "rankings": rankings,
        "label_to_model": label_to_model
    }

def parse_ranking(evaluation: str) -> List[str]:
    """Extract ranking from evaluation text"""
    lines = evaluation.split('\n')
    ranking = []

    in_ranking = False
    for line in lines:
        if "FINAL RANKING" in line.upper():
            in_ranking = True
            continue

        if in_ranking:
            # Look for numbered rankings like "1. Response A"
            import re
            match = re.search(r'\d+\.\s*(Response\s+[A-Z])', line)
            if match:
                ranking.append(match.group(1))

    return ranking

def calculate_aggregate_rankings(stage2_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Calculate aggregate rankings across all evaluations"""
    rankings = stage2_results["rankings"]
    label_to_model = stage2_results["label_to_model"]

    # Count positions for each response
    position_sums = {}
    vote_counts = {}

    for model, ranking_data in rankings.items():
        parsed = ranking_data["parsed_ranking"]
        for position, label in enumerate(parsed, 1):
            if label not in position_sums:
                position_sums[label] = 0
                vote_counts[label] = 0
            position_sums[label] += position
            vote_counts[label] += 1

    # Calculate averages
    aggregated = []
    for label in label_to_model.keys():
        if label in position_sums and vote_counts[label] > 0:
            avg_position = position_sums[label] / vote_counts[label]
            aggregated.append({
                "label": label,
                "model": label_to_model[label],
                "avg_position": avg_position,
                "vote_count": vote_counts[label]
            })

    # Sort by average position (lower is better)
    aggregated.sort(key=lambda x: x["avg_position"])

    return aggregated

def stage3_synthesize_final(query: str, stage1_responses: Dict[str, str],
                            stage2_results: Dict[str, Any]) -> str:
    """Stage 3: Chairman synthesizes final answer"""
    print("🎯 Stage 3: Chairman synthesizing final answer...")

    # Prepare context for chairman
    responses_text = "\n\n".join([
        f"{model}:\n{response}"
        for model, response in stage1_responses.items()
    ])

    aggregate_rankings = calculate_aggregate_rankings(stage2_results)
    rankings_text = "\n".join([
        f"{i+1}. {item['model']} (avg rank: {item['avg_position']:.2f})"
        for i, item in enumerate(aggregate_rankings)
    ])

    synthesis_prompt = f"""Original Query: {query}

COUNCIL MEMBER RESPONSES:
{responses_text}

AGGREGATE RANKINGS (by peer review):
{rankings_text}

As Chairman of the Council, synthesize the best insights from all responses into a single, comprehensive answer.
Give more weight to higher-ranked responses, but incorporate valuable insights from all members.
Provide a clear, actionable recommendation for private equity decision-making."""

    system_prompt = "You are the Chairman of an expert council. Synthesize the collective wisdom into clear recommendations."

    final_answer = query_ollama(CHAIRMAN_MODEL, synthesis_prompt, system_prompt)

    return final_answer

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "agent": "LLM Council (Local)",
        "status": "running",
        "port": PORT,
        "council_models": COUNCIL_MODELS,
        "chairman": CHAIRMAN_MODEL,
        "backend": "Ollama Local"
    })

@app.route('/query', methods=['POST'])
def query():
    """Main query endpoint - 3-stage deliberation"""
    try:
        data = request.json
        user_query = data.get('query', '')

        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        print(f"\n{'='*70}")
        print(f"  LLM COUNCIL - NEW QUERY")
        print(f"{'='*70}")
        print(f"Query: {user_query}\n")

        # Stage 1: Initial responses
        stage1 = stage1_collect_responses(user_query)

        # Stage 2: Peer reviews
        stage2 = stage2_collect_rankings(user_query, stage1)

        # Stage 3: Final synthesis
        stage3 = stage3_synthesize_final(user_query, stage1, stage2)

        # Calculate aggregate rankings
        aggregate = calculate_aggregate_rankings(stage2)

        print(f"\n{'='*70}")
        print("✅ Council deliberation complete!")
        print(f"{'='*70}\n")

        return jsonify({
            "query": user_query,
            "stage1": stage1,
            "stage2": stage2,
            "stage3": stage3,
            "aggregate_rankings": aggregate,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def main():
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║           NEWCO LOCAL LLM COUNCIL - AGENT #10                ║
╚═══════════════════════════════════════════════════════════════╝

🎯 Multi-model deliberation system for IC memo analysis
🧠 Council: {len(COUNCIL_MODELS)} local models
👔 Chairman: {CHAIRMAN_MODEL}
🌐 Port: {PORT}
💰 Cost: $0 (all local!)

Council Members:
""")
    for i, model in enumerate(COUNCIL_MODELS, 1):
        print(f"  {i}. {model}")

    print(f"\nChairman: {CHAIRMAN_MODEL}")
    print(f"\nStarting server on port {PORT}...")
    print("="*70)

    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == "__main__":
    main()

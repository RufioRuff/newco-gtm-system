#!/usr/bin/env python3
"""
NEWCO Local ML Engineer Agent - Agent #9
========================================

Agentic ML engineer using local Ollama for model training and optimization.
Port: 8009

Capabilities:
- Train ML models (XGBoost, neural networks, etc.)
- Hyperparameter optimization
- Feature engineering suggestions
- Model evaluation and analysis

Based on karpathy-agent concept but adapted for local Ollama.
"""

import requests
import json
import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
OLLAMA_HOST = "http://localhost:11434"
PORT = 8009
MODEL = "codellama:latest"  # Best for code generation
WORKSPACE = "/Users/rufio/NEWCO/ml_workspace"

# Ensure workspace exists
os.makedirs(WORKSPACE, exist_ok=True)

def query_ollama(prompt: str, system: str = None) -> str:
    """Query local Ollama model"""
    try:
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }

        if system:
            payload["system"] = system

        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json=payload,
            timeout=180  # 3 minutes for complex code generation
        )

        if response.status_code == 200:
            result = response.json()
            return result.get('response', '')
        else:
            return f"[Error querying {MODEL}]"

    except Exception as e:
        return f"[Error: {str(e)}]"

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "agent": "ML Engineer (Local)",
        "status": "running",
        "port": PORT,
        "model": MODEL,
        "workspace": WORKSPACE,
        "backend": "Ollama Local"
    })

@app.route('/train', methods=['POST'])
def train_model():
    """Train ML model based on specifications"""
    try:
        data = request.json
        task = data.get('task', '')
        dataset_info = data.get('dataset', {})
        model_type = data.get('model_type', 'xgboost')

        print(f"\n{'='*70}")
        print(f"  ML ENGINEER - TRAINING REQUEST")
        print(f"{'='*70}")
        print(f"Task: {task}")
        print(f"Model: {model_type}\n")

        system_prompt = """You are an expert ML engineer. Generate complete, production-ready Python code.
Include all necessary imports, error handling, and best practices.
Focus on XGBoost, scikit-learn, and PyTorch."""

        prompt = f"""Task: {task}

Dataset: {json.dumps(dataset_info, indent=2)}
Model Type: {model_type}

Generate a complete Python script to:
1. Load and preprocess the data
2. Train the {model_type} model
3. Evaluate performance with cross-validation
4. Save the trained model
5. Print feature importance (if applicable)

Make it production-ready with proper error handling."""

        print("🤖 Generating training code...")
        code = query_ollama(prompt, system_prompt)

        # Save generated code
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"train_{model_type}_{timestamp}.py"
        filepath = os.path.join(WORKSPACE, filename)

        with open(filepath, 'w') as f:
            f.write(code)

        print(f"✅ Code saved to: {filepath}\n")

        return jsonify({
            "task": task,
            "model_type": model_type,
            "code": code,
            "filepath": filepath,
            "status": "ready",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/optimize', methods=['POST'])
def optimize_hyperparameters():
    """Suggest hyperparameter optimization strategy"""
    try:
        data = request.json
        model_type = data.get('model_type', 'xgboost')
        current_params = data.get('current_params', {})
        current_performance = data.get('performance', {})

        print(f"\n{'='*70}")
        print(f"  ML ENGINEER - OPTIMIZATION REQUEST")
        print(f"{'='*70}")
        print(f"Model: {model_type}\n")

        system_prompt = """You are an expert in ML model optimization and hyperparameter tuning.
Provide specific, actionable recommendations based on current performance."""

        prompt = f"""Model Type: {model_type}

Current Hyperparameters:
{json.dumps(current_params, indent=2)}

Current Performance:
{json.dumps(current_performance, indent=2)}

Provide:
1. Analysis of current hyperparameters
2. Specific recommendations for improvement
3. Suggested hyperparameter search space
4. Expected performance gains
5. Python code for hyperparameter optimization (using optuna or GridSearchCV)"""

        print("🤖 Generating optimization strategy...")
        recommendations = query_ollama(prompt, system_prompt)

        print(f"✅ Optimization recommendations generated\n")

        return jsonify({
            "model_type": model_type,
            "recommendations": recommendations,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/feature-engineering', methods=['POST'])
def feature_engineering():
    """Suggest feature engineering improvements"""
    try:
        data = request.json
        features = data.get('features', [])
        target = data.get('target', '')
        domain = data.get('domain', 'finance')

        print(f"\n{'='*70}")
        print(f"  ML ENGINEER - FEATURE ENGINEERING")
        print(f"{'='*70}")
        print(f"Domain: {domain}\n")

        system_prompt = f"""You are an expert in feature engineering for {domain}.
Provide creative, domain-specific feature suggestions."""

        prompt = f"""Domain: {domain}
Target Variable: {target}

Current Features:
{json.dumps(features, indent=2)}

Suggest:
1. Derived features (ratios, interactions, polynomials)
2. Domain-specific engineered features
3. Time-based features (if applicable)
4. Feature selection strategy
5. Python code to implement top 5 feature engineering ideas"""

        print("🤖 Generating feature engineering suggestions...")
        suggestions = query_ollama(prompt, system_prompt)

        print(f"✅ Feature engineering suggestions generated\n")

        return jsonify({
            "domain": domain,
            "suggestions": suggestions,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/evaluate', methods=['POST'])
def evaluate_model():
    """Evaluate model and provide analysis"""
    try:
        data = request.json
        model_type = data.get('model_type', '')
        metrics = data.get('metrics', {})
        confusion_matrix = data.get('confusion_matrix', None)

        print(f"\n{'='*70}")
        print(f"  ML ENGINEER - MODEL EVALUATION")
        print(f"{'='*70}")
        print(f"Model: {model_type}\n")

        system_prompt = """You are an expert in ML model evaluation and interpretation.
Provide detailed analysis of model performance and actionable recommendations."""

        prompt = f"""Model Type: {model_type}

Performance Metrics:
{json.dumps(metrics, indent=2)}

{f"Confusion Matrix: {json.dumps(confusion_matrix, indent=2)}" if confusion_matrix else ""}

Provide:
1. Analysis of model performance
2. Identification of strengths and weaknesses
3. Comparison to expected performance for this task
4. Specific recommendations for improvement
5. Potential overfitting/underfitting diagnosis
6. Next steps"""

        print("🤖 Analyzing model performance...")
        analysis = query_ollama(prompt, system_prompt)

        print(f"✅ Model evaluation complete\n")

        return jsonify({
            "model_type": model_type,
            "analysis": analysis,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def main():
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║           NEWCO LOCAL ML ENGINEER - AGENT #9                 ║
╚═══════════════════════════════════════════════════════════════╝

🤖 Agentic ML Engineer using local LLMs
🧠 Model: {MODEL}
🌐 Port: {PORT}
📁 Workspace: {WORKSPACE}
💰 Cost: $0 (all local!)

Capabilities:
  • Train ML models (XGBoost, neural networks)
  • Hyperparameter optimization
  • Feature engineering suggestions
  • Model evaluation and analysis
  • Code generation for ML tasks

Starting server on port {PORT}...
{'='*70}
""")

    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == "__main__":
    main()

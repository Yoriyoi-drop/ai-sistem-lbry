#!/usr/bin/env python3

# 📦 NEXAFORGE - OLLAMA MODEL SCRIPT (L2 Layer)

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional

class ModelDownloader:
    """Handles Ollama model management for L2: Model AI Layer"""

    def __init__(self, models_path: str = "~/nexaforge/models"):
        self.models_path = Path(models_path).expanduser()
        # Note: With Ollama, models are stored in Ollama's directory, not this path
        # This path is kept for compatibility but not actively used for model storage

        # Ollama model repository information
        self.model_repos = {
            "qwen:7b-instruct": {
                "name": "Qwen 7B Instruct",
                "size": "7B",
                "type": "general",
                "description": "General purpose instruction-following model",
                "ollama_name": "qwen:7b-instruct"
            },
            "qwen:14b-instruct": {
                "name": "Qwen 14B Instruct",
                "size": "14B",
                "type": "general",
                "description": "Larger general purpose instruction-following model",
                "ollama_name": "qwen:14b-instruct"
            },
            "qwen:32b-instruct": {
                "name": "Qwen 32B Instruct",
                "size": "32B",
                "type": "coding",
                "description": "Advanced coding & development model",
                "ollama_name": "qwen:32b-instruct"
            },
            "llama3:70b-instruct": {
                "name": "Llama 3 70B Instruct",
                "size": "70B",
                "type": "reasoning",
                "description": "Advanced reasoning & analysis model",
                "ollama_name": "llama3:70b-instruct"
            },
            "llama3:8b-instruct": {
                "name": "Llama 3 8B Instruct",
                "size": "8B",
                "type": "general",
                "description": "Efficient general assistant model",
                "ollama_name": "llama3:8b-instruct"
            },
            "mistral:7b-instruct": {
                "name": "Mistral 7B Instruct",
                "size": "7B",
                "type": "efficient",
                "description": "Efficient inference model",
                "ollama_name": "mistral:7b-instruct"
            },
            "phi3:instruct": {
                "name": "Phi-3 Instruct",
                "size": "3.8B",
                "type": "efficient",
                "description": "Lightweight efficient model",
                "ollama_name": "phi3:instruct"
            },
            "gemma2:9b": {
                "name": "Gemma 2 9B",
                "size": "9B",
                "type": "efficient",
                "description": "Google's efficient model",
                "ollama_name": "gemma2:9b"
            },
            "codellama:7b-instruct": {
                "name": "CodeLlama 7B Instruct",
                "size": "7B",
                "type": "coding",
                "description": "Specialized coding model",
                "ollama_name": "codellama:7b-instruct"
            },
            "securitybert:latest": {
                "name": "SecurityBERT",
                "size": "110M",
                "type": "security",
                "description": "Specialized security analysis model",
                "ollama_name": "securitybert:latest"  # Placeholder - would need a security-focused model
            }
        }

    def list_available_models(self) -> Dict:
        """List all available Ollama models"""
        return self.model_repos

    def get_local_models(self) -> List[str]:
        """Get list of models available in Ollama (placeholder)"""
        # In a real implementation, this would call the Ollama API to list local models
        # For now, return a generic message
        return ["Run 'ollama list' to see available models"]

    def create_pull_script(self, model_name: str) -> str:
        """Create a shell script to pull a specific model using Ollama"""
        if model_name not in self.model_repos:
            # Check if it's a generic ollama model name
            if ':' in model_name:
                ollama_name = model_name
                model_info = {
                    "name": model_name,
                    "size": "Unknown",
                    "type": "custom",
                    "description": f"Custom Ollama model: {model_name}"
                }
            else:
                raise ValueError(f"Model {model_name} not found in repository")
        else:
            model_info = self.model_repos[model_name]
            ollama_name = model_info["ollama_name"]

        script_content = f"""#!/bin/bash

# Ollama model pull script for {model_info['name']}
# Ollama model name: {ollama_name}
# Type: {model_info['type']} ({model_info['size']})

echo "🚀 Pulling Ollama model: {ollama_name}..."
echo "Name: {model_info['name']}"
echo "Type: {model_info['type']} ({model_info['size']})"
echo "Description: {model_info['description']}"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running. Please start Ollama first:"
    echo "   docker run -d --name ollama -p 11434:11434 ollama/ollama"
    echo "   OR"
    echo "   ollama serve"
    exit 1
fi

# Pull the model from Ollama
echo "Starting download/pull..."
ollama pull {ollama_name}

# Verify the model was pulled
if ollama list | grep -q "{ollama_name}"; then
    echo "✅ {model_info['name']} ({ollama_name}) pulled successfully!"
    echo "To use this model, run: ollama run {ollama_name}"
    ollama show {ollama_name}
else
    echo "❌ Failed to pull {model_info['name']} ({ollama_name})"
    exit 1
fi

echo "Model pull completed for {ollama_name}"
"""

        script_path = f"pull_{model_name.lower().replace(':', '_').replace('-', '_')}.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)

        # Make script executable
        os.chmod(script_path, 0o755)

        return script_path

    def create_all_pull_scripts(self) -> List[str]:
        """Create pull scripts for all available models"""
        scripts = []
        for model_name in self.model_repos.keys():
            script_path = self.create_pull_script(model_name)
            scripts.append(script_path)
            print(f"✅ Created pull script: {script_path}")

        return scripts

def main():
    """Main function for Ollama model manager"""
    print("📦 NEXAFORGE - OLLAMA MODEL MANAGER (L2 Layer)")
    print("=" * 50)

    downloader = ModelDownloader()

    print("\n🤖 AVAILABLE OLLAMA MODELS:")
    models = downloader.list_available_models()
    for model, info in models.items():
        print(f"  • {info['name']} ({info['size']}) - {info['description']}")

    print(f"\n📋 Total available models: {len(models)}")

    print("\n🔄 Creating pull scripts...")
    scripts = downloader.create_all_pull_scripts()

    print(f"\n📝 Created {len(scripts)} pull scripts:")
    for script in scripts:
        print(f"  • {script}")

    print("\n💡 To pull a model, run: bash <script_name>")
    print("   Example: bash pull_qwen_7b_instruct.sh")
    print("\n⚠️  WARNING: These are large models (3B to 70B parameters)")
    print("   Make sure you have sufficient disk space and internet bandwidth")
    print("\n📋 Before pulling models, ensure Ollama is installed and running:")
    print("   1. Install Ollama: https://ollama.ai")
    print("   2. Start Ollama: ollama serve")
    print("   OR run: docker run -d --name ollama -p 11434:11434 ollama/ollama")

if __name__ == "__main__":
    main()
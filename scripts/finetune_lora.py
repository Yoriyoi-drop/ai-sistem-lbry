#!/usr/bin/env python3
"""Ollama Model Fine-tuning Script

This script demonstrates how to create custom Ollama models using model
parameterization and prompt engineering. With Ollama, fine-tuning happens
through Modelfile definitions rather than LoRA adapters.

For actual Ollama model customization, create a Modelfile with your
training data and run: ollama create <model_name> -f Modelfile
"""

import os
import json
from pathlib import Path

def create_ollama_modelfile():
    """Create an Ollama Modelfile for custom model training"""

    model_name = os.environ.get("MODEL_NAME", "qwen:7b-instruct")
    output_dir = os.environ.get("OUTPUT_DIR", "outputs/ollama_modelfile")

    data_path = Path("data") / "train.jsonl"
    if not data_path.exists():
        print("Warning: No training data found at data/train.jsonl. Creating template only.")

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Create a Modelfile template for Ollama
    modelfile_content = f"""# Ollama Modelfile for Security AI Model
FROM {model_name}

# Set parameters
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx 4096

# System message for security-focused behavior
TEMPLATE """ + '"""{{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

{{ .Response }}<|eot_id|>"""' + """

# Example system prompt for security AI
SYSTEM "You are a security-focused AI assistant specialized in cybersecurity analysis, threat detection, and security implementation guidance."
"""

    modelfile_path = Path(output_dir) / "Modelfile"
    with open(modelfile_path, 'w') as f:
        f.write(modelfile_content)

    print(f"Ollama Modelfile created at: {modelfile_path}")
    print(f"Example usage: ollama create my-security-model -f {modelfile_path}")

    # Create a sample training script
    training_script = f"""#!/bin/bash
# Ollama Model Training Script

# Check if Ollama is running
if ! curl -s http://localhost:11434 > /dev/null; then
    echo "Error: Ollama server is not running"
    exit 1
fi

# Create custom security model
echo "Creating custom security model..."
ollama create my-security-model -f {modelfile_path}

# Test the model
echo "Testing the model..."
ollama run my-security-model "What is AI security?"

echo "Model creation completed!"
"""

    script_path = Path(output_dir) / "train_model.sh"
    with open(script_path, 'w') as f:
        f.write(training_script)

    # Make script executable
    os.chmod(script_path, 0o755)

    print(f"Training script created at: {script_path}")
    print("Run the script with: bash " + str(script_path))


def finetune():
    """Ollama-based fine-tuning (modelfile approach)"""
    print("Using Ollama for model customization...")
    create_ollama_modelfile()


if __name__ == "__main__":
    finetune()

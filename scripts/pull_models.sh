#!/bin/bash

# Script to pull all AI Team A models into the Ollama container
echo "Starting to pull AI Team A models..."

# Pull each model as specified in the plan
ollama pull qwen2.5-coder
ollama pull llama3.1:70b
ollama pull deepseek-r1:32b
ollama pull phi3-vision
ollama pull qwen2-vl
ollama pull smollm:3b
ollama pull gemma2:27b
ollama pull llama-guard3

echo "All AI Team A models have been pulled successfully!"
echo "Run 'ollama list' to verify all models are installed."
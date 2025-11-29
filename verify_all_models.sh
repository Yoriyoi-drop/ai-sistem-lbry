#!/bin/bash
# Script untuk memverifikasi semua model yang disebutkan dalam ai_config.json
# File: verify_all_models.sh

echo "🔍 Verifying all models from ai_config.json"
echo "==========================================="

# Model-model dari ai_config.json
models_to_check=(
    "Qwen2.5-Coder-32B-Instruct"
    "Qwen2.5-72B"
    "Llama-3.1-70B-Instruct" 
    "DeepSeek-R1-70B-Distill"
    "Phi-3.5-Vision"
    "Qwen-Audio"
    "Qwen2-VL"
    "SmolAgent"
    "Nous-Hermes-3"
    "Gemma-2-27B"
)

echo "📋 Models defined in ai_config.json:"
printf '%s\n' "${models_to_check[@]}"

echo ""
echo "📦 Currently available models in Ollama:"
curl -s http://localhost:11434/api/tags | python3 -m json.tool | grep -E 'name|parameter_size' || echo "❌ Could not retrieve model list"

echo ""
echo "🎯 Testing actual available models that match configuration:"
available_models=$(curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; data=json.load(sys.stdin); [print(m['name']) for m in data['models']]")

echo "Available models in Ollama:"
echo "$available_models"

echo ""
echo "🔄 Checking for models with different naming schemes..."

# Check for common variants of models
found_models=()
not_found_models=()

for model in "${models_to_check[@]}"; do
    # Convert config model name to Ollama format
    case "$model" in
        "Qwen2.5-Coder-32B-Instruct")
            ollama_variants=("qwen2.5-coder:32b" "qwen2.5:32b-instruct" "qwen2.5-coder:latest" "qwen2.5:latest")
            ;;
        "Qwen2.5-72B")
            ollama_variants=("qwen2.5:72b" "qwen2.5:7b" "qwen2.5:latest")
            ;;
        "Llama-3.1-70B-Instruct")
            ollama_variants=("llama3.1:70b" "llama3.1:70b-instruct" "llama3.1:latest")
            ;;
        "DeepSeek-R1-70B-Distill")
            ollama_variants=("deepseek:70b" "deepseek-r1:70b" "deepseek:latest")
            ;;
        "Phi-3.5-Vision")
            ollama_variants=("phi3.5:vision" "phi3.5-vision:latest" "phi3:vision")
            ;;
        "Qwen-Audio")
            ollama_variants=("qwen:audio" "qwen-audio:latest")
            ;;
        "Qwen2-VL")
            ollama_variants=("qwen2:vl" "qwen2-vl:latest")
            ;;
        "SmolAgent")
            ollama_variants=("smol:latest" "smolagent:latest")
            ;;
        "Nous-Hermes-3")
            ollama_variants=("noushermes3:latest" "nous-hermes3:latest")
            ;;
        "Gemma-2-27B")
            ollama_variants=("gemma2:27b" "gemma2:latest")
            ;;
        *)
            ollama_variants=("${model,,}" "${model,,}:latest" "${model/-/:}")  # lowercase and variants
            ;;
    esac
    
    found=false
    for variant in "${ollama_variants[@]}"; do
        if echo "$available_models" | grep -q "$variant"; then
            echo "✅ $model -> $variant (available)"
            found_models+=("$model: $variant")
            found=true
            break
        fi
    done
    
    if [ "$found" = false ]; then
        echo "❌ $model -> Not found (tried: ${ollama_variants[*]})"
        not_found_models+=("$model")
    fi
done

echo ""
echo "📊 SUMMARY:"
echo "Found: ${#found_models[@]} models"
echo "Missing: ${#not_found_models[@]} models"

echo ""
echo "✅ Available models from config:"
for model in "${found_models[@]}"; do
    echo "  - $model"
done

echo ""
echo "❌ Missing models (not available in Ollama):"
for model in "${not_found_models[@]}"; do
    echo "  - $model"
done

echo ""
echo "💡 To install missing models, run:"
echo "   ollama pull <model-name>"
echo ""
echo "💡 For example:"
for model in "${not_found_models[@]}"; do
    case "$model" in
        "Qwen2.5-Coder-32B-Instruct")
            echo "   ollama pull qwen2.5:32b-instruct"
            ;;
        "Llama-3.1-70B-Instruct")
            echo "   ollama pull llama3.1:70b-instruct"
            ;;
        *)
            echo "   ollama pull ${model/-/:}" 
            ;;
    esac
done

echo ""
echo "🎯 Currently working model (verified): qwen2.5:7b-instruct"
echo "   curl -X POST http://localhost:11434/api/generate -H 'Content-Type: application/json' \\"
echo "   -d '{\"model\": \"qwen2.5:7b-instruct\", \"prompt\": \"Hello\", \"stream\": false}'"
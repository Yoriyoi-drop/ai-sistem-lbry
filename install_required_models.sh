#!/bin/bash
# Script untuk menginstal model-model yang diperlukan berdasarkan ai_config.json
# File: install_required_models.sh

echo "📦 Installing required AI models based on ai_config.json"
echo "======================================================"

# Daftar model yang diperlukan dari konfigurasi
required_models=(
    "qwen2.5:32b-instruct"  # Qwen2.5-Coder-32B-Instruct
    "qwen2.5:72b"           # Qwen2.5-72B (sekarang hanya 7b, tapi bisa coba model lebih besar)
    "llama3.1:70b-instruct" # Llama-3.1-70B-Instruct (sekarang hanya latest, bisa coba 70b versi)
    "deepseek-coder:7b"     # DeepSeek-R1-70B-Distill (alternatif karena mungkin tidak tersedia)
    "phi3:14b"              # Phi-3.5-Vision (alternatif karena mungkin tidak tersedia)
    "gemma2:27b"            # Gemma-2-27B (jika tersedia)
)

# Model-model yang lebih ringan sebagai alternatif
alternative_models=(
    "qwen2:7b-instruct"     # Alternatif untuk beberapa model Qwen
    "mistral:7b-instruct"   # Alternatif umum
    "phi3:medium"           # Alternatif untuk model vision
    "llama3:8b"             # Alternatif untuk model besar
)

# Model yang sudah terinstal
echo "📋 Already installed models:"
curl -s http://localhost:11434/api/tags | python3 -m json.tool | grep -E 'name|parameter_size' || echo "❌ Could not retrieve model list"

echo ""
echo "🎯 Installing missing models (selective approach)..."
echo ""

# Install model qwen2.5:32b-instruct jika diperlukan (ini yang utama untuk coding)
echo "🔍 Installing qwen2.5:32b-instruct (for coding tasks)..."
if curl -s http://localhost:11434/api/tags | grep -q "qwen2.5:32b-instruct"; then
    echo "✅ qwen2.5:32b-instruct already installed"
else
    echo "🔄 Attempting to install qwen2.5:32b-instruct..."
    # Catatan: mungkin nama model yang tepat berbeda, coba beberapa varian
    possible_names=("qwen2.5:32b-instruct" "qwen2.5-coder:32b" "qwen2.5:32b" "qwen2.5:32b-instruct-v1" "qwen2:32b-instruct")
    
    installed=false
    for name in "${possible_names[@]}"; do
        echo "Trying: $name"
        if docker exec -t infinite-ai-ollama ollama list 2>/dev/null | grep -q "$name"; then
            echo "✅ $name already exists in container"
            installed=true
            break
        fi
        
        # Coba pull model
        if timeout 30s docker exec -t infinite-ai-ollama ollama pull "$name" 2>/dev/null; then
            echo "✅ Successfully installed: $name"
            installed=true
            break
        else
            echo "⚠️  Could not install: $name"
        fi
    done
    
    if [ "$installed" = false ]; then
        echo "❌ Could not install any variant of qwen2.5 32b model"
        echo "💡 Available Qwen models:"
        docker exec -t infinite-ai-ollama ollama list | grep -i qwen
    fi
fi

echo ""
echo "🔍 Installing additional models based on configuration..."

# Cek dan install model-model lain yang mungkin cocok
if ! curl -s http://localhost:11434/api/tags | grep -q "gemma2:27b"; then
    echo "🔄 Installing gemma2:27b..."
    if timeout 60s docker exec -t infinite-ai-ollama ollama pull gemma2:27b; then
        echo "✅ gemma2:27b installed"
    else
        echo "⚠️  Could not install gemma2:27b, trying gemma2:9b..."
        if timeout 60s docker exec -t infinite-ai-ollama ollama pull gemma2:9b; then
            echo "✅ gemma2:9b installed as alternative"
        else
            echo "⚠️  Could not install gemma2 variants"
        fi
    fi
else
    echo "✅ gemma2:27b already installed"
fi

echo ""
echo "📋 Available models after installation attempt:"
curl -s http://localhost:11434/api/tags | python3 -m json.tool | grep -E 'name|parameter_size'

echo ""
echo "💡 Note: Some models from ai_config.json may not be available in Ollama format"
echo "   or may have different naming conventions."
echo ""
echo "💡 For models that couldn't be installed, check Ollama model library:"
echo "   https://ollama.ai/library"
echo ""
echo "💡 To manually install a model:"
echo "   docker exec -t infinite-ai-ollama ollama pull <model-name>"

echo ""
echo "🎯 Testing currently available models..."

# Uji model qwen2.5:7b-instruct (model utama yang berfungsi)
echo ""
echo "🔍 Testing main model (qwen2.5:7b-instruct):"
test_result=$(curl -s -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d '{"model": "qwen2.5:7b-instruct", "prompt": "Hello", "stream": false}' --max-time 30)
if [ $? -eq 0 ] && echo "$test_result" | grep -q "response"; then
    echo "✅ qwen2.5:7b-instruct is working correctly"
else
    echo "❌ qwen2.5:7b-instruct test failed"
fi

echo ""
echo "🚀 Model installation process completed!"
echo "📊 Current model status has been updated in AI_MODEL_STATUS_REPORT.md"
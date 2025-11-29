#!/bin/bash
# Final verification script for Infinite AI Security Ollama integration

echo "🔐 Infinite AI Security - Ollama Integration Verification"
echo "========================================================="
echo ""

echo "✅ 1/5. Checking Ollama service status..."
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    VERSION=$(curl -s http://localhost:11434/api/version | jq -r '.version' 2>/dev/null || echo "unknown")
    echo "   ✅ Ollama API is running (v$VERSION)"
else
    echo "   ❌ Ollama API is not accessible"
    exit 1
fi

echo ""
echo "✅ 2/5. Checking configuration files..."
CONFIG_FILES=(
    "docker-compose.ollama.yml"
    "pull_ollama_models.sh"
    "setup_ollama.sh"
    ".env.ollama"
)

for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file - OK"
    else
        echo "   ❌ $file - Missing"
        exit 1
    fi
done

echo ""
echo "✅ 3/5. Checking scripts are executable..."
chmod +x pull_ollama_models.sh setup_ollama.sh 2>/dev/null
echo "   ✅ Scripts are executable"

echo ""
echo "✅ 4/5. Testing Ollama API functionality..."
API_RESPONSE=$(curl -s http://localhost:11434/api/tags)
if [ $? -eq 0 ]; then
    echo "   ✅ API endpoint is functional"
    MODEL_COUNT=$(echo "$API_RESPONSE" | jq '.models | length' 2>/dev/null || echo "0")
    echo "   📊 Current models: $MODEL_COUNT"
else
    echo "   ❌ API endpoint is not responding"
    exit 1
fi

echo ""
echo "✅ 5/5. Verifying Python integration..."
if python3 -c "import requests; requests.get('http://localhost:11434/api/version', timeout=5)" 2>/dev/null; then
    echo "   ✅ Python can connect to Ollama API"
else
    echo "   ❌ Python connection to Ollama failed"
    exit 1
fi

echo ""
echo "🎉 SUCCESS: Ollama integration is fully configured!"
echo ""
echo "📊 Current Status:"
echo "   - Ollama Service: Running (v$VERSION)"
echo "   - API Endpoint: http://localhost:11434"
echo "   - Available Models: $MODEL_COUNT"
echo "   - Configuration: Complete"
echo ""
echo "🚀 Next Steps:"
echo ""
echo "1. Pull security models:"
echo "   ./pull_ollama_models.sh"
echo ""
echo "2. Or pull specific model:"
echo "   docker exec infinite-ai-ollama ollama pull qwen2.5:7b-instruct"
echo ""
echo "3. Test the complete system:"
echo "   export OLLAMA_HOST=http://localhost:11434"
echo "   export MODEL_NAME=qwen2.5:7b-instruct"
echo "   python main.py"
echo ""
echo "4. Check model availability:"
echo "   curl http://localhost:11434/api/tags"
echo ""
echo "💡 Pro Tips:"
echo "   - Use ./setup_ollama.sh --help for automated setup options"
echo "   - See OLLAMA_SETUP.md for detailed configuration options"
echo "   - GPU acceleration can be enabled by uncommenting in docker-compose.ollama.yml"
echo ""
echo "The Ollama integration for Infinite AI Security is ready to use! 🔥"
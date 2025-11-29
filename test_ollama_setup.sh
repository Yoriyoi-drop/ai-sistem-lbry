#!/bin/bash
# Test script for Infinite AI Security Ollama integration
# This script verifies that all configuration files are properly set up

echo "🔍 Infinite AI Security - Ollama Integration Test"
echo "================================================"

# Check required files exist
echo ""
echo "📋 Checking required configuration files..."

files=(
    "docker-compose.ollama.yml"
    "pull_ollama_models.sh"
    "setup_ollama.sh"
    ".env.ollama"
    "OLLAMA_SETUP.md"
    "OLLAMA_INTEGRATION.md"
)

all_found=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file"
        all_found=false
    fi
done

if [ "$all_found" = false ]; then
    echo ""
    echo "❌ Some required files are missing. Please run the setup again."
    exit 1
fi

echo ""
echo "✅ All configuration files are in place"

# Check if scripts are executable
echo ""
echo "🔧 Checking script permissions..."

if [ -x "pull_ollama_models.sh" ]; then
    echo "  ✅ pull_ollama_models.sh is executable"
else
    echo "  ⚠ pull_ollama_models.sh is not executable, making executable..."
    chmod +x pull_ollama_models.sh
fi

if [ -x "setup_ollama.sh" ]; then
    echo "  ✅ setup_ollama.sh is executable"
else
    echo "  ⚠ setup_ollama.sh is not executable, making executable..."
    chmod +x setup_ollama.sh
fi

# Test Docker availability
echo ""
echo "🐳 Checking Docker availability..."

if ! command -v docker &> /dev/null; then
    echo "  ❌ Docker is not installed or not in PATH"
    echo "     Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
else
    echo "  ✅ Docker is available"
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "  ❌ Docker Compose is not installed or not in PATH"
    echo "     Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
else
    echo "  ✅ Docker Compose is available"
fi

# Check if Docker daemon is running
if docker info > /dev/null 2>&1; then
    echo "  ✅ Docker daemon is running"
else
    echo "  ⚠ Docker daemon may not be running"
    echo "     Please start Docker before running the services"
    echo "     On Linux: sudo systemctl start docker"
    echo "     On Windows/Mac: Start Docker Desktop application"
fi

# Show summary
echo ""
echo "🎉 Configuration verification complete!"
echo ""
echo "You're ready to use Ollama with Infinite AI Security!"
echo ""
echo "To start using it:"
echo ""
echo "1. Ensure Docker is running:"
echo "   docker ps  # should not show any errors"
echo ""
echo "2. Start Ollama service:"
echo "   docker-compose -f docker-compose.ollama.yml up -d ollama"
echo ""
echo "3. Pull required models:"
echo "   ./pull_ollama_models.sh"
echo ""
echo "4. Check the API status:"
echo "   curl http://localhost:11434/api/version"
echo ""
echo "For full setup instructions, see OLLAMA_SETUP.md"
echo ""
echo "💡 Pro tip: Use the setup script for complete setup:"
echo "   ./setup_ollama.sh --help"
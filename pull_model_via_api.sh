#!/bin/bash
# Simple model pull script that works with pre-running Ollama container
# This approach uses the Ollama API directly for model pulling

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Infinite AI Security - Model Pull via API                ║"
echo "║  Pull models using Ollama API (no docker exec needed)     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

OLLAMA_HOST="http://localhost:11434"
MODEL_NAME="${1:-qwen2.5:7b-instruct}"

echo -e "${YELLOW}[1/3]${NC} Checking Ollama API availability..."
if curl -s "$OLLAMA_HOST/api/version" > /dev/null; then
    VERSION=$(curl -s "$OLLAMA_HOST/api/version" | jq -r '.version' 2>/dev/null || echo "unknown")
    echo -e "${GREEN}✓ Ollama API is available (v$VERSION)${NC}"
else
    echo -e "${RED}✗ Ollama API is not accessible at $OLLAMA_HOST${NC}"
    exit 1
fi

echo -e "${YELLOW}[2/3]${NC} Pulling model '$MODEL_NAME' via API..."

# Create a named pipe for progress updates
FIFO=$(mktemp -u)
mkfifo "$FIFO"

# Function to read progress in background
{
    while read -r line; do
        if [ -n "$line" ]; then
            echo -n "."
            # Extract and display progress if available
            status=$(echo "$line" | jq -r '.status' 2>/dev/null)
            if [ "$status" != "null" ] && [ -n "$status" ]; then
                echo -e "\n  Status: $status"
            fi
        fi
    done < "$FIFO"
} &
PROGRESS_PID=$!

# Start pulling the model
echo -e "${CYAN}Pulling $MODEL_NAME... this may take 5-15 minutes depending on model size and internet speed${NC}"

# Use curl with streaming to get progress updates
curl -X POST "$OLLAMA_HOST/api/pull" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$MODEL_NAME\"}" \
    > "$FIFO" 2>/dev/null &

CURL_PID=$!

# Wait for curl to complete
wait $CURL_PID

# Kill progress reader
kill $PROGRESS_PID 2>/dev/null
rm -f "$FIFO"

echo ""
echo -e "${GREEN}✓ Model pull completed${NC}"

echo -e "${YELLOW}[3/3]${NC} Verifying model availability..."

# Check if the model is now available
if curl -s "$OLLAMA_HOST/api/tags" | grep -q "$MODEL_NAME"; then
    echo -e "${GREEN}✓ Model $MODEL_NAME is now available${NC}"
    
    # Show the available model details
    echo ""
    echo "Model details:"
    curl -s "$OLLAMA_HOST/api/tags" | jq ".models[] | select(.name == \"$MODEL_NAME\")" 2>/dev/null || echo "  $MODEL_NAME"
else
    echo -e "${RED}✗ Model $MODEL_NAME is not available after pulling${NC}"
    echo "Available models:"
    curl -s "$OLLAMA_HOST/api/tags" | jq '.models[].name' 2>/dev/null || echo "  (none)"
    exit 1
fi

echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✓ MODEL SUCCESSFULLY INSTALLED                           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo ""
echo -e "${CYAN}📋 Next Steps:${NC}"
echo ""
echo "1. Test the model:"
echo "   curl $OLLAMA_HOST/api/chat \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"model\": \"$MODEL_NAME\", \"messages\": [{\"role\": \"user\", \"content\": \"Hello, what security capabilities do you have?\"}]}'"
echo ""
echo "2. Use with your security system:"
echo "   export OLLAMA_HOST=http://localhost:11434"
echo "   export MODEL_NAME=$MODEL_NAME"
echo ""
echo "3. Check all available models:"
echo "   curl $OLLAMA_HOST/api/tags"
echo ""

exit 0
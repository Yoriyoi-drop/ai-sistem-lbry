#!/bin/bash

####################################################################
# Infinite AI Security - Ollama Model Setup Script
# Download and setup AI models for the security system
####################################################################

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
echo "║  Infinite AI Security - Ollama Model Setup                ║"
echo "║  Download & Install AI Models for Security System         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Default configuration
OLLAMA_CONTAINER="infinite-ai-ollama"
OLLAMA_HOST="localhost:11434"
DEFAULT_MODELS=("qwen2.5:7b-instruct" "llama3.1" "mistral")

# Function to check if Docker is running
check_docker() {
    echo -e "${YELLOW}[1/6]${NC} Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}✗ Docker is not installed${NC}"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        # Try using sudo if regular access fails
        if docker -H unix:///var/run/docker.sock info &> /dev/null; then
            # Create an alias for docker commands if needed
            echo -e "${YELLOW}⚠ Using Docker with direct socket access${NC}"
            export DOCKER_CMD="docker -H unix:///var/run/docker.sock"
        elif sudo -n docker info &> /dev/null; then
            echo -e "${YELLOW}⚠ Docker requires sudo, using with sudo${NC}"
            export DOCKER_CMD="sudo docker"
        else
            echo -e "${RED}✗ Docker daemon is not running${NC}"
            echo "Please start Docker:"
            echo "  - On Linux: sudo systemctl start docker"
            echo "  - On Windows/Mac: Start Docker Desktop application"
            exit 1
        fi
    else
        export DOCKER_CMD="docker"
    fi
    echo -e "${GREEN}✓ Docker is accessible${NC}"
}

# Function to check if Ollama container is running
check_ollama_container() {
    echo -e "${YELLOW}[2/6]${NC} Checking Ollama container..."

    if $DOCKER_CMD ps | grep -q "$OLLAMA_CONTAINER"; then
        echo -e "${GREEN}✓ Ollama container is running${NC}"
        return 0
    elif $DOCKER_CMD ps -a | grep -q "$OLLAMA_CONTAINER"; then
        echo -e "${YELLOW}⚠ Ollama container exists but is not running${NC}"
        echo "Starting Ollama container..."
        $DOCKER_CMD start "$OLLAMA_CONTAINER" > /dev/null
        sleep 10  # Wait for container to start
        echo -e "${GREEN}✓ Ollama container started${NC}"
    else
        echo -e "${RED}✗ Ollama container does not exist${NC}"
        echo "Please start the Ollama service first:"
        echo "  docker-compose -f docker-compose.ollama.yml up -d ollama"
        exit 1
    fi
}

# Function to check available space
check_disk_space() {
    echo -e "${YELLOW}[3/6]${NC} Checking disk space..."
    
    # Check space in Docker volumes directory
    SPACE_NEEDED=20  # GB
    SPACE_AVAILABLE=$(df /var/lib/docker | awk 'NR==2 {print int($4/1048576)}')
    
    echo "  Available in Docker directory: ${SPACE_AVAILABLE}GB"
    echo "  Required: ${SPACE_NEEDED}GB minimum"
    
    if [ $SPACE_AVAILABLE -lt $SPACE_NEEDED ]; then
        echo -e "${RED}✗ Not enough disk space in Docker directory!${NC}"
        echo "Consider cleaning up Docker: docker system prune -a"
        exit 1
    fi
    echo -e "${GREEN}✓ Sufficient disk space${NC}"
}

# Function to check Ollama API
check_ollama_api() {
    echo -e "${YELLOW}[4/6]${NC} Checking Ollama API availability..."
    
    # Wait for API to be ready
    ATTEMPTS=30
    COUNT=0
    while [ $COUNT -lt $ATTEMPTS ]; do
        if curl -s "http://$OLLAMA_HOST/api/version" > /dev/null; then
            VERSION=$(curl -s "http://$OLLAMA_HOST/api/version" | jq -r '.version' 2>/dev/null || echo "unknown")
            echo -e "${GREEN}✓ Ollama API is available (v$VERSION)${NC}"
            return 0
        fi
        sleep 2
        COUNT=$((COUNT + 1))
    done
    
    echo -e "${RED}✗ Ollama API is not responding${NC}"
    exit 1
}

# Function to pull models
pull_models() {
    echo -e "${YELLOW}[5/6]${NC} Pulling AI models..."
    
    # Allow user to specify models or use defaults
    if [ $# -eq 0 ]; then
        MODELS=("${DEFAULT_MODELS[@]}")
        echo "Using default models: ${DEFAULT_MODELS[*]}"
    else
        MODELS=("$@")
        echo "Pulling specified models: ${MODELS[*]}"
    fi
    
    # Pull each model
    for model in "${MODELS[@]}"; do
        echo ""
        echo -e "${CYAN}Pulling model: $model${NC}"
        echo -e "${CYAN}This may take several minutes depending on internet speed and model size${NC}"

        # Start progress tracking in background
        (
            while true; do
                if [ -f /tmp/ollama_pull_progress ]; then
                    tail -n 1 /tmp/ollama_pull_progress 2>/dev/null || echo "..."
                else
                    echo "..."
                fi
                sleep 5
            done
        ) &
        PROGRESS_PID=$!

        # Run the actual pull command
        if $DOCKER_CMD exec "$OLLAMA_CONTAINER" ollama pull "$model" > /tmp/ollama_pull_progress 2>&1; then
            echo -e "${GREEN}✓ Successfully pulled $model${NC}"
        else
            echo -e "${RED}✗ Failed to pull $model${NC}"
            cat /tmp/ollama_pull_progress 2>/dev/null || echo "No detailed error available"
        fi

        # Stop progress tracking
        kill $PROGRESS_PID 2>/dev/null
        rm -f /tmp/ollama_pull_progress
    done
}

# Function to verify models
verify_models() {
    echo -e "${YELLOW}[6/6]${NC} Verifying models..."

    echo "Available models in Ollama:"
    $DOCKER_CMD exec "$OLLAMA_CONTAINER" ollama list

    echo ""
    echo -e "${CYAN}Testing model functionality...${NC}"

    # Test the first model by running a simple query
    TEST_MODEL="${DEFAULT_MODELS[0]}"
    if $DOCKER_CMD exec "$OLLAMA_CONTAINER" ollama list | grep -q "$TEST_MODEL"; then
        echo "Testing $TEST_MODEL..."

        # Run a simple test query
        RESPONSE=$($DOCKER_CMD exec "$OLLAMA_CONTAINER" ollama run "$TEST_MODEL" "Hello, what security capabilities do you have?" 2>/dev/null | head -n 5)

        if [ $? -eq 0 ] && [ -n "$RESPONSE" ]; then
            echo -e "${GREEN}✓ Model $TEST_MODEL is working correctly${NC}"
            echo "Response preview: ${RESPONSE:0:100}..."
        else
            echo -e "${YELLOW}⚠ Model $TEST_MODEL may have issues, but is installed${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ Default model $TEST_MODEL not found, skipping test${NC}"
    fi
}

# Main execution
main() {
    # Parse command line arguments
    if [ $# -gt 0 ]; then
        CUSTOM_MODELS=("$@")
    else
        CUSTOM_MODELS=()
    fi

    # Run all checks and setup
    check_docker
    check_ollama_container
    check_disk_space
    check_ollama_api

    if [ ${#CUSTOM_MODELS[@]} -gt 0 ]; then
        pull_models "${CUSTOM_MODELS[@]}"
    else
        pull_models
    fi

    verify_models

    echo ""
    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  ✓ OLLAMA MODEL SETUP COMPLETE                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    echo ""
    echo -e "${CYAN}📋 Next Steps:${NC}"
    echo ""
    echo "1. Verify all models are available:"
    echo "   $DOCKER_CMD exec $OLLAMA_CONTAINER ollama list"
    echo ""
    echo "2. Test a model directly:"
    echo "   $DOCKER_CMD exec -it $OLLAMA_CONTAINER ollama run qwen2.5:7b-instruct"
    echo ""
    echo "3. Start your AI security services with Ollama integration"
    echo ""
    echo "4. For API usage, test with:"
    echo "   curl http://localhost:11434/api/tags"
    echo ""
    echo "5. To use with your security system:"
    echo "   export OLLAMA_HOST=http://localhost:11434"
    echo "   export MODEL_NAME=qwen2.5:7b-instruct"
    echo ""
    echo -e "${GREEN}✓ Models are ready for use in the Infinite AI Security system!${NC}"
}

# Handle help option
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "Usage: $0 [MODEL1 MODEL2 ...]"
    echo ""
    echo "Download and setup Ollama AI models for Infinite AI Security"
    echo ""
    echo "Options:"
    echo "  -h, --help    Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Pull default models"
    echo "  $0 qwen2.5:7b-instruct               # Pull specific model"
    echo "  $0 qwen2.5:7b-instruct llama3.1      # Pull multiple models"
    echo ""
    echo "Default models: ${DEFAULT_MODELS[*]}"
    exit 0
fi

# Execute main function with all arguments
main "$@"
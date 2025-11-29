#!/bin/bash

####################################################################
# Infinite AI Security - Complete Ollama Setup Script
# Complete setup for Ollama integration with security system
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
echo "║  Infinite AI Security - Complete Ollama Setup             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Default values
OLLAMA_CONTAINER="infinite-ai-ollama"
OLLAMA_PORT="11434"
APP_PORT="8000"

# Function to display help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Complete setup script for Ollama integration with Infinite AI Security"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  --start        Start all services"
    echo "  --setup        Full setup (pull models, start services)"
    echo "  --models       Only set up models"
    echo "  --stop         Stop all services"
    echo "  --status       Check service status"
    echo ""
    echo "Examples:"
    echo "  $0 --setup          # Complete setup"
    echo "  $0 --start          # Start services only"
    echo "  $0 --models         # Pull models only"
}

# Function to check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}[1/6]${NC} Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}✗ Docker is not installed${NC}"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        echo -e "${RED}✗ Docker daemon is not running${NC}"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}✗ Docker Compose is not installed${NC}"
        exit 1
    fi
    
    # Check required files
    if [ ! -f "docker-compose.ollama.yml" ]; then
        echo -e "${RED}✗ docker-compose.ollama.yml not found${NC}"
        exit 1
    fi
    
    if [ ! -f "pull_ollama_models.sh" ]; then
        echo -e "${RED}✗ pull_ollama_models.sh not found${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Prerequisites met${NC}"
}

# Function to start Ollama service
start_ollama() {
    echo -e "${YELLOW}[2/6]${NC} Starting Ollama service..."

    if [ -f "docker-compose.ollama.yml" ]; then
        # Start Ollama service (default config has GPU disabled)
        docker-compose -f docker-compose.ollama.yml up -d ollama

        echo -e "${GREEN}✓ Ollama service started${NC}"

        # Wait for service to be ready
        echo -e "${CYAN}Waiting for Ollama to be ready...${NC}"
        COUNT=0
        MAX_WAIT=30
        while [ $COUNT -lt $MAX_WAIT ]; do
            if curl -s "http://localhost:$OLLAMA_PORT/api/version" > /dev/null; then
                break
            fi
            sleep 2
            COUNT=$((COUNT + 1))
        done
        if [ $COUNT -lt $MAX_WAIT ]; then
            echo -e "${GREEN}✓ Ollama API is ready${NC}"
        else
            echo -e "${RED}✗ Ollama API is not responding${NC}"
            exit 1
        fi
    else
        echo -e "${RED}✗ docker-compose.ollama.yml not found${NC}"
        exit 1
    fi
}

# Function to pull models
setup_models() {
    echo -e "${YELLOW}[3/6]${NC} Setting up AI models..."
    
    if [ -f "./pull_ollama_models.sh" ]; then
        chmod +x ./pull_ollama_models.sh
        ./pull_ollama_models.sh
        echo -e "${GREEN}✓ Models setup completed${NC}"
    else
        echo -e "${RED}✗ pull_ollama_models.sh not found${NC}"
        exit 1
    fi
}

# Function to start the main application
start_application() {
    echo -e "${YELLOW}[4/6]${NC} Starting AI security application..."
    
    if [ -f "docker-compose.yml" ]; then
        # Use the ollama compose file too for integration
        if [ -f "docker-compose.ollama.yml" ]; then
            docker-compose -f docker-compose.yml -f docker-compose.ollama.yml up -d
        else
            docker-compose up -d
        fi
        echo -e "${GREEN}✓ AI security application started${NC}"
    else
        echo -e "${YELLOW}⚠ docker-compose.yml not found, starting basic services${NC}"
        # Start with environment variables
        if [ -f ".env.ollama" ]; then
            export $(grep -v '^#' .env.ollama | xargs)
        fi
        python main.py &
        echo -e "${GREEN}✓ Application started in background${NC}"
    fi
}

# Function to check service status
check_status() {
    echo -e "${YELLOW}[5/6]${NC} Checking service status..."
    
    echo "Docker containers:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    echo ""
    echo "Ollama service:"
    if curl -s "http://localhost:$OLLAMA_PORT/api/version" > /dev/null; then
        VERSION=$(curl -s "http://localhost:$OLLAMA_PORT/api/version" | jq -r '.version' 2>/dev/null || echo "unknown")
        echo -e "${GREEN}✓ Ollama API is running (v$VERSION)${NC}"
    else
        echo -e "${RED}✗ Ollama API is not running${NC}"
    fi
    
    echo ""
    echo "Available models:"
    if docker ps | grep -q "$OLLAMA_CONTAINER"; then
        docker exec -it "$OLLAMA_CONTAINER" ollama list 2>/dev/null || echo "No models available or container not running"
    else
        echo "Ollama container is not running"
    fi
}

# Function to stop services
stop_services() {
    echo -e "${YELLOW}[6/6]${NC} Stopping services..."
    
    # Stop Docker Compose services
    if [ -f "docker-compose.ollama.yml" ]; then
        docker-compose -f docker-compose.ollama.yml down
    fi
    
    if [ -f "docker-compose.yml" ]; then
        docker-compose -f docker-compose.yml -f docker-compose.ollama.yml down
    fi
    
    # Kill any background Python processes
    pkill -f "python main.py" 2>/dev/null || true
    
    echo -e "${GREEN}✓ Services stopped${NC}"
}

# Main execution logic
case "${1:-}" in
    --help|-h)
        show_help
        exit 0
        ;;
    --start)
        check_prerequisites
        start_ollama
        check_status
        echo ""
        echo -e "${GREEN}✓ Ollama service is running!${NC}"
        echo "Access Ollama API at: http://localhost:$OLLAMA_PORT"
        ;;
    --models)
        check_prerequisites
        start_ollama
        setup_models
        echo ""
        echo -e "${GREEN}✓ Model setup complete!${NC}"
        ;;
    --setup)
        check_prerequisites
        start_ollama
        setup_models
        start_application
        check_status
        echo ""
        echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  ✓ COMPLETE OLLAMA SETUP SUCCESSFUL                      ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${CYAN}Services are now running:${NC}"
        echo "  Ollama API: http://localhost:$OLLAMA_PORT"
        echo "  Security API: http://localhost:$APP_PORT"
        echo "  Ollama Web UI: http://localhost:3001 (if enabled)"
        echo ""
        echo "Next steps:"
        echo "  1. Test the API: curl http://localhost:$APP_PORT/health"
        echo "  2. Start using the security AI system"
        echo "  3. Check logs with: docker logs $OLLAMA_CONTAINER"
        ;;
    --stop)
        stop_services
        ;;
    --status)
        check_status
        ;;
    *)
        echo "Invalid option: $1"
        show_help
        exit 1
        ;;
esac
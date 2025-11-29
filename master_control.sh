#!/bin/bash
# Master Control Script for Infinite AI Security Autonomous System
# Orchestrates all autonomous capabilities

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
MAIN_DIR="/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security"
LOG_FILE="$MAIN_DIR/logs/master_control.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Function to show banner
show_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                          INFINITE AI SECURITY                                ║"
    echo "║                    Autonomous Operation Control Panel                        ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to show system status
show_status() {
    echo -e "${BLUE}SYSTEM STATUS${NC}"
    echo "════════════════════════════════════════════════════════════════════════════════"
    
    echo -e "${CYAN}Ollama Service:${NC}"
    if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
        VERSION=$(curl -s http://localhost:11434/api/version | jq -r '.version' 2>/dev/null || echo "unknown")
        echo -e "  ✅ Running (v$VERSION)"
    else
        echo -e "  ❌ Not accessible"
    fi
    
    echo -e "${CYAN}Autonomous System:${NC}"
    "$MAIN_DIR/autonomous_operation.sh" status
    
    echo -e "${CYAN}Available Models:${NC}"
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        curl -s http://localhost:11434/api/tags | jq '.models[].name' 2>/dev/null | sed 's/"//g' | sed 's/^/  ✅ /' || echo "  (none)"
    else
        echo "  ❌ Cannot connect to Ollama"
    fi
    
    echo ""
}

# Function to start complete autonomous system
start_autonomous_system() {
    echo -e "${GREEN}Starting Complete Autonomous System...${NC}"
    
    # Start Ollama if not running
    if ! docker -H unix:///var/run/docker.sock ps | grep -q "infinite-ai-ollama"; then
        echo "Starting Ollama service..."
        docker-compose -f "$MAIN_DIR/docker-compose.ollama.yml" up -d ollama
        sleep 10
    fi
    
    # Start autonomous operation
    "$MAIN_DIR/autonomous_operation.sh" start
    
    echo -e "${GREEN}✓ Complete autonomous system is now running${NC}"
}

# Function to stop the system
stop_autonomous_system() {
    echo -e "${RED}Stopping Autonomous System...${NC}"
    
    "$MAIN_DIR/autonomous_operation.sh" stop
    
    echo -e "${RED}✓ Autonomous system stopped${NC}"
}

# Main command handler
main() {
    show_banner
    
    case "${1:-}" in
        status)
            show_status
            ;;
        start)
            start_autonomous_system
            ;;
        stop)
            stop_autonomous_system
            ;;
        restart)
            stop_autonomous_system
            sleep 5
            start_autonomous_system
            ;;
        setup-service)
            echo -e "${CYAN}Setting up systemd service for auto-start...${NC}"
            
            # Copy service file and enable it
            "$MAIN_DIR/setup_systemd_service.sh"
            ;;
        interactive)
            while true; do
                echo ""
                echo -e "${YELLOW}Choose an action:${NC}"
                echo "1) Show Status"
                echo "2) Start System"
                echo "3) Stop System" 
                echo "4) Restart System"
                echo "5) Setup Systemd Service"
                echo "6) Run Self-Learning Cycle"
                echo "7) Run Health Check"
                echo "0) Exit"
                echo -n "Enter choice (0-7): "
                
                read choice
                
                case $choice in
                    1)
                        show_status
                        ;;
                    2)
                        start_autonomous_system
                        ;;
                    3)
                        stop_autonomous_system
                        ;;
                    4)
                        stop_autonomous_system
                        sleep 5
                        start_autonomous_system
                        ;;
                    5)
                        "$MAIN_DIR/setup_systemd_service.sh"
                        ;;
                    6)
                        echo -e "${CYAN}Running self-learning cycle...${NC}"
                        "$MAIN_DIR/auto_update_self_learn.sh" --autonomous-cycle
                        echo -e "${GREEN}Self-learning cycle completed${NC}"
                        ;;
                    7)
                        echo -e "${CYAN}Running health check...${NC}"
                        "$MAIN_DIR/autonomous_operation.sh" health
                        ;;
                    0)
                        echo "Exiting..."
                        break
                        ;;
                    *)
                        echo "Invalid choice. Please enter 0-7."
                        ;;
                esac
            done
            ;;
        *)
            echo -e "${CYAN}Usage:$NC $0 {status|start|stop|restart|setup-service|interactive}"
            echo ""
            echo "Commands:"
            echo "  status        - Show system status"
            echo "  start         - Start autonomous system"
            echo "  stop          - Stop autonomous system"
            echo "  restart       - Restart autonomous system"
            echo "  setup-service - Setup systemd service for auto-start on boot"
            echo "  interactive   - Interactive control panel"
            echo ""
            show_status
            ;;
    esac
}

main "$@"
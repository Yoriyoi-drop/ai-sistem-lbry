#!/bin/bash

####################################################################
# NexaForge AI System - Health & Performance Monitor
# Real-time monitoring dashboard untuk sistem AI 24/7
####################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Clear screen
clear

# Get paths
PROJECT_PATH="/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security"

# Function to print header
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  🏥 NexaForge AI System - Health Monitor${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Function to check service status
check_service_status() {
    if systemctl is-active --quiet nexaforge-24-7; then
        echo -e "${GREEN}✓ ACTIVE${NC}"
    else
        echo -e "${RED}✗ INACTIVE${NC}"
    fi
}

# Function to check container health
check_container() {
    local container=$1
    local port=$2
    
    if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        local health=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null || echo "no healthcheck")
        local status=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null || echo "unknown")
        
        if [ "$status" = "running" ] && [ "$health" = "healthy" ]; then
            echo -e "${GREEN}✓ HEALTHY${NC}"
        elif [ "$status" = "running" ]; then
            echo -e "${YELLOW}⚠ ${status}${NC} (health: $health)"
        else
            echo -e "${RED}✗ ${status}${NC}"
        fi
    else
        echo -e "${RED}✗ NOT FOUND${NC}"
    fi
}

# Function to check http endpoint
check_endpoint() {
    local port=$1
    local endpoint=${2:-/health}
    
    if timeout 2 curl -s "http://localhost:$port$endpoint" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 200 OK${NC}"
    else
        echo -e "${RED}✗ TIMEOUT${NC}"
    fi
}

# Function to get container resource usage
get_container_stats() {
    local container=$1
    
    if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        docker stats --no-stream "$container" --format "{{.CPUPerc}} / {{.MemUsage}}" 2>/dev/null || echo "N/A"
    else
        echo "Container not running"
    fi
}

# Main monitoring loop
monitor_loop() {
    while true; do
        clear
        print_header
        
        echo ""
        echo -e "${CYAN}📊 SYSTEM STATUS${NC}"
        echo "  Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "  Uptime: $(uptime -p)"
        echo "  Service Status: $(check_service_status)"
        
        echo ""
        echo -e "${CYAN}🐳 CONTAINER STATUS${NC}"
        echo ""
        
        # AI Services
        echo -e "${MAGENTA}  AI Services:${NC}"
        printf "    • astramind (8001):     "
        check_container "astramind" "8001"
        printf "    • spectralogic (8002):  "
        check_container "spectralogic" "8002"
        printf "    • forgerun (8003):      "
        check_container "forgerun" "8003"
        printf "    • guardianos (8004):    "
        check_container "guardianos" "8004"
        
        echo ""
        echo -e "${MAGENTA}  Infrastructure:${NC}"
        printf "    • infinite-ai-api:     "
        check_container "infinite-ai-api" "8000"
        printf "    • infinite-ai-nginx:   "
        check_container "infinite-ai-nginx" "80"
        printf "    • infinite-ai-db:      "
        check_container "infinite-ai-db" "5432"
        printf "    • infinite-ai-redis:   "
        check_container "infinite-ai-redis" "6379"
        
        echo ""
        echo -e "${MAGENTA}  Monitoring:${NC}"
        printf "    • infinite-ai-prometheus: "
        check_container "infinite-ai-prometheus" "9090"
        printf "    • infinite-ai-grafana:    "
        check_container "infinite-ai-grafana" "3000"
        
        echo ""
        echo -e "${CYAN}🌐 HTTP ENDPOINTS${NC}"
        echo ""
        printf "    API Health (8000):       "
        check_endpoint 8000
        printf "    AstraMind (8001):        "
        check_endpoint 8001
        printf "    SpectraLogic (8002):     "
        check_endpoint 8002
        printf "    ForgeRun (8003):         "
        check_endpoint 8003
        printf "    GuardianOS (8004):       "
        check_endpoint 8004
        printf "    Nginx (80):              "
        check_endpoint 80
        printf "    Prometheus (9090):       "
        check_endpoint 9090
        printf "    Grafana (3000):          "
        check_endpoint 3000
        
        echo ""
        echo -e "${CYAN}💾 RESOURCE USAGE${NC}"
        echo ""
        
        total_cpu=0
        total_mem=0
        count=0
        
        for container in astramind spectralogic forgerun guardianos infinite-ai-api infinite-ai-db infinite-ai-redis; do
            if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
                stats=$(docker stats --no-stream "$container" --format "{{.CPUPerc}}|{{.MemUsage}}" 2>/dev/null)
                cpu=$(echo "$stats" | cut -d'|' -f1 | sed 's/%//g')
                mem=$(echo "$stats" | cut -d'|' -f2)
                printf "    %-20s CPU: %6s | MEM: %s\n" "$container" "$cpu" "$mem"
            fi
        done
        
        echo ""
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${YELLOW}Press Ctrl+C to exit | Refresh: every 5 seconds${NC}"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        
        sleep 5
    done
}

# Handle Ctrl+C
trap 'echo -e "\n${YELLOW}Monitor stopped${NC}"; exit 0' INT

# Start monitoring
monitor_loop

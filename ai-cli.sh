#!/bin/bash

####################################################################
# NexaForge AI System - Quick Commands
# Copy-paste commands untuk operasi sehari-hari
####################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

case "$1" in

    ########################################################
    # QUICK START COMMANDS
    ########################################################
    
    "status")
        echo -e "${BLUE}Checking system status...${NC}"
        echo ""
        echo -e "${YELLOW}Systemd Service:${NC}"
        sudo systemctl status nexaforge-24-7 --no-pager
        echo ""
        echo -e "${YELLOW}Running Containers:${NC}"
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        ;;
        
    "start")
        echo -e "${GREEN}Starting NexaForge...${NC}"
        sudo systemctl start nexaforge-24-7
        sleep 2
        sudo systemctl status nexaforge-24-7 --no-pager
        ;;
        
    "stop")
        echo -e "${RED}Stopping NexaForge...${NC}"
        sudo systemctl stop nexaforge-24-7
        sleep 2
        echo -e "${GREEN}Stopped successfully${NC}"
        ;;
        
    "restart")
        echo -e "${YELLOW}Restarting NexaForge...${NC}"
        sudo systemctl restart nexaforge-24-7
        sleep 3
        sudo systemctl status nexaforge-24-7 --no-pager
        ;;
        
    "logs")
        echo -e "${BLUE}Showing last 50 logs...${NC}"
        sudo journalctl -u nexaforge-24-7 -n 50
        ;;
        
    "logs-follow")
        echo -e "${BLUE}Following logs in real-time (Ctrl+C to exit)...${NC}"
        sudo journalctl -u nexaforge-24-7 -f
        ;;
        
    "monitor")
        echo -e "${BLUE}Starting health monitor...${NC}"
        bash /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/monitor-24-7.sh
        ;;
        
    "ps")
        echo -e "${BLUE}All running containers:${NC}"
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        echo ""
        echo -e "${BLUE}Container health status:${NC}"
        for container in astramind spectralogic forgerun guardianos infinite-ai-api infinite-ai-db infinite-ai-redis; do
            if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
                health=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null || echo "N/A")
                printf "  %-25s : %s\n" "$container" "$health"
            fi
        done
        ;;
        
    "health")
        echo -e "${BLUE}Checking health endpoints...${NC}"
        echo ""
        endpoints=(
            "API Health|8000|/health"
            "AstraMind|8001|/health"
            "SpectraLogic|8002|/health"
            "ForgeRun|8003|/health"
            "GuardianOS|8004|/health"
            "Prometheus|9090|/-/healthy"
            "Grafana|3000|/api/health"
        )
        
        for endpoint in "${endpoints[@]}"; do
            IFS='|' read -r name port path <<< "$endpoint"
            if timeout 2 curl -s "http://localhost:$port$path" > /dev/null 2>&1; then
                echo -e "${GREEN}✓${NC} $name (http://localhost:$port)"
            else
                echo -e "${RED}✗${NC} $name (http://localhost:$port)"
            fi
        done
        ;;
        
    "container-log")
        if [ -z "$2" ]; then
            echo -e "${RED}Usage: $0 container-log [container-name]${NC}"
            echo "Available containers: astramind, spectralogic, forgerun, guardianos, infinite-ai-api, infinite-ai-db, infinite-ai-redis"
            exit 1
        fi
        echo -e "${BLUE}Logs for $2 (Ctrl+C to exit):${NC}"
        docker logs -f "$2"
        ;;
        
    "shell")
        if [ -z "$2" ]; then
            echo -e "${RED}Usage: $0 shell [container-name]${NC}"
            exit 1
        fi
        echo -e "${BLUE}Entering shell in $2${NC}"
        docker exec -it "$2" /bin/bash || docker exec -it "$2" /bin/sh
        ;;
        
    "stats")
        echo -e "${BLUE}Container resource usage (Ctrl+C to exit):${NC}"
        docker stats
        ;;
        
    "prune")
        echo -e "${YELLOW}Cleaning up unused Docker resources...${NC}"
        docker system prune -a --volumes -f
        echo -e "${GREEN}Cleanup complete${NC}"
        ;;
        
    "enable")
        echo -e "${YELLOW}Enabling auto-start on boot...${NC}"
        sudo systemctl enable nexaforge-24-7
        echo -e "${GREEN}Enabled${NC}"
        ;;
        
    "disable")
        echo -e "${YELLOW}Disabling auto-start on boot...${NC}"
        sudo systemctl disable nexaforge-24-7
        echo -e "${GREEN}Disabled${NC}"
        ;;
        
    "backup")
        echo -e "${BLUE}Backing up database...${NC}"
        docker exec infinite-ai-db pg_dump -U postgres infinite_security > /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/backups/db_backup_$(date +%Y%m%d_%H%M%S).sql
        echo -e "${GREEN}Backup complete${NC}"
        ;;
        
    "restart-container")
        if [ -z "$2" ]; then
            echo -e "${RED}Usage: $0 restart-container [container-name]${NC}"
            exit 1
        fi
        echo -e "${YELLOW}Restarting $2...${NC}"
        docker restart "$2"
        sleep 2
        docker ps --filter "name=$2" --format "table {{.Names}}\t{{.Status}}"
        ;;
        
    "pull")
        echo -e "${YELLOW}Pulling latest images...${NC}"
        cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security
        docker compose -f docker-compose-24-7.yml pull
        echo -e "${GREEN}Pull complete${NC}"
        ;;
        
    "rebuild")
        echo -e "${YELLOW}Rebuilding images...${NC}"
        cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security
        docker compose -f docker-compose-24-7.yml build --no-cache
        echo -e "${GREEN}Rebuild complete${NC}"
        ;;
        
    "clean-logs")
        echo -e "${YELLOW}Clearing Docker logs...${NC}"
        for container in $(docker ps -a --format '{{.Names}}'); do
            docker logs "$container" --tail 0 -f > /dev/null 2>&1 &
            sleep 0.1
        done
        echo -e "${GREEN}Logs cleared${NC}"
        ;;
        
    "port-check")
        echo -e "${BLUE}Checking port availability...${NC}"
        ports=(80 443 3000 5432 6379 8000 8001 8002 8003 8004 9090)
        for port in "${ports[@]}"; do
            if sudo lsof -i ":$port" > /dev/null 2>&1; then
                echo -e "${GREEN}✓${NC} Port $port: IN USE"
            else
                echo -e "${YELLOW}○${NC} Port $port: Available"
            fi
        done
        ;;
        
    "firewall-setup")
        echo -e "${BLUE}Setting up firewall rules...${NC}"
        sudo ufw allow 22/tcp   # SSH
        sudo ufw allow 80/tcp   # HTTP
        sudo ufw allow 443/tcp  # HTTPS
        sudo ufw allow 3000/tcp # Grafana
        sudo ufw allow 9090/tcp # Prometheus
        echo -e "${GREEN}Firewall rules added${NC}"
        ;;
        
    "dashboard")
        echo -e "${BLUE}Opening Grafana Dashboard...${NC}"
        if command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:3000 &
        elif command -v open &> /dev/null; then
            open http://localhost:3000 &
        else
            echo "Grafana: http://localhost:3000"
            echo "Prometheus: http://localhost:9090"
            echo "API: http://localhost:8000"
        fi
        ;;
        
    "help"|"")
        cat << EOF
${BLUE}╔════════════════════════════════════════════════════════════════════════════╗${NC}
${BLUE}║  NexaForge AI System - Command Reference                                  ║${NC}
${BLUE}╚════════════════════════════════════════════════════════════════════════════╝${NC}

${YELLOW}BASIC COMMANDS:${NC}
  status              - Show system status
  start               - Start the service
  stop                - Stop the service
  restart             - Restart the service
  logs                - Show last 50 logs
  logs-follow         - Follow logs in real-time
  
${YELLOW}MONITORING:${NC}
  monitor             - Start health monitor dashboard
  health              - Check health endpoints
  stats               - Show container resource usage
  ps                  - List running containers
  
${YELLOW}CONTAINER MANAGEMENT:${NC}
  container-log [name] - View logs for specific container
  shell [name]         - Enter shell in container
  restart-container [name] - Restart specific container
  
${YELLOW}SYSTEM MANAGEMENT:${NC}
  enable              - Enable auto-start on boot
  disable             - Disable auto-start on boot
  port-check          - Check port availability
  firewall-setup      - Setup firewall rules
  
${YELLOW}MAINTENANCE:${NC}
  backup              - Backup database
  pull                - Pull latest images
  rebuild             - Rebuild images
  prune               - Clean unused resources
  clean-logs          - Clear Docker logs
  
${YELLOW}TOOLS:${NC}
  dashboard           - Open Grafana dashboard
  help                - Show this help message

${BLUE}EXAMPLES:${NC}
  $(basename $0) status
  $(basename $0) logs-follow
  $(basename $0) monitor
  $(basename $0) container-log astramind
  $(basename $0) shell infinite-ai-api
  $(basename $0) health

${YELLOW}For full documentation, see: SETUP_24_7_GUIDE.md${NC}

EOF
        ;;
        
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo "Type: $0 help"
        exit 1
        ;;
        
esac

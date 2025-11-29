#!/bin/bash

# Script untuk menjalankan Infinite AI Security dengan Docker Compose
# Usage: ./run_nexaproge_docker.sh [start|stop|build|logs|up]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ACTION=${1:-up}

case $ACTION in
    "start"|"up")
        echo -e "${GREEN}=== Starting Infinite AI Security (Nexaproge) ===${NC}"
        docker-compose -f docker-compose.nexaproge.yml up -d
        echo -e "${GREEN}✓ Services started successfully${NC}"
        echo -e "${YELLOW}Access the API at: http://localhost:8000${NC}"
        ;;
    "stop")
        echo -e "${GREEN}=== Stopping Infinite AI Security (Nexaproge) ===${NC}"
        docker-compose -f docker-compose.nexaproge.yml down
        echo -e "${GREEN}✓ Services stopped successfully${NC}"
        ;;
    "build")
        echo -e "${GREEN}=== Building Docker images ===${NC}"
        docker-compose -f docker-compose.nexaproge.yml build
        echo -e "${GREEN}✓ Images built successfully${NC}"
        ;;
    "logs")
        echo -e "${GREEN}=== Viewing logs ===${NC}"
        docker-compose -f docker-compose.nexaproge.yml logs -f
        ;;
    "rebuild")
        echo -e "${GREEN}=== Rebuilding and starting services ===${NC}"
        docker-compose -f docker-compose.nexaproge.yml up -d --build
        echo -e "${GREEN}✓ Services rebuilt and started successfully${NC}"
        ;;
    *)
        echo -e "${YELLOW}Usage: $0 [start|stop|build|logs|rebuild|up]${NC}"
        echo -e "${YELLOW}  start/up   - Start services in detached mode${NC}"
        echo -e "${YELLOW}  stop       - Stop services${NC}"
        echo -e "${YELLOW}  build      - Build images${NC}"
        echo -e "${YELLOW}  logs       - View logs${NC}"
        echo -e "${YELLOW}  rebuild    - Rebuild and start services${NC}"
        exit 1
        ;;
esac
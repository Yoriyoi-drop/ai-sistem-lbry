#!/bin/bash

# Script untuk Cek Status Docker Desktop
# Usage: ./check_docker_status.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Docker Desktop Status Check                 ║${NC}"
echo -e "${GREEN}║   Infinite AI Security Platform                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Docker is running
echo -e "${BLUE}[1/6] Checking Docker Service...${NC}"
if docker info > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Docker is running${NC}"
else
    echo -e "${RED}✗ Docker is not running${NC}"
    echo -e "${YELLOW}Please start Docker Desktop${NC}"
    exit 1
fi
echo ""

# Check Docker version
echo -e "${BLUE}[2/6] Docker Version:${NC}"
docker version --format '{{.Server.Version}}'
echo ""

# List all images
echo -e "${BLUE}[3/6] Docker Images:${NC}"
echo -e "${YELLOW}┌─────────────────────────┬─────────┬──────────────┬─────────┐${NC}"
echo -e "${YELLOW}│ Repository              │ Tag     │ Image ID     │ Size    │${NC}"
echo -e "${YELLOW}├─────────────────────────┼─────────┼──────────────┼─────────┤${NC}"
docker images --format "│ {{.Repository}} │ {{.Tag}} │ {{.ID}} │ {{.Size}} │" | head -20
echo -e "${YELLOW}└─────────────────────────┴─────────┴──────────────┴─────────┘${NC}"
echo ""

# Count images
IMAGE_COUNT=$(docker images -q | wc -l)
echo -e "${GREEN}Total Images: ${IMAGE_COUNT}${NC}"
echo ""

# List all containers
echo -e "${BLUE}[4/6] Docker Containers:${NC}"
echo -e "${YELLOW}┌──────────────────────┬──────────────────────┬─────────────────────┐${NC}"
echo -e "${YELLOW}│ Name                 │ Image                │ Status              │${NC}"
echo -e "${YELLOW}├──────────────────────┼──────────────────────┼─────────────────────┤${NC}"
docker ps -a --format "│ {{.Names}} │ {{.Image}} │ {{.Status}} │" | head -20
echo -e "${YELLOW}└──────────────────────┴──────────────────────┴─────────────────────┘${NC}"
echo ""

# Count containers
RUNNING_COUNT=$(docker ps -q | wc -l)
TOTAL_COUNT=$(docker ps -aq | wc -l)
echo -e "${GREEN}Running Containers: ${RUNNING_COUNT}/${TOTAL_COUNT}${NC}"
echo ""

# Check running containers
echo -e "${BLUE}[5/6] Running Containers Details:${NC}"
if [ $RUNNING_COUNT -eq 0 ]; then
    echo -e "${YELLOW}No containers are currently running${NC}"
else
    docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
fi
echo ""

# Check disk usage
echo -e "${BLUE}[6/6] Docker Disk Usage:${NC}"
docker system df
echo ""

# Check for port conflicts
echo -e "${BLUE}Checking for Port Conflicts:${NC}"
PORTS=(8000 8080 8090 3000 5432 6379 9090 11434 11437)
for PORT in "${PORTS[@]}"; do
    if ss -tlnp 2>/dev/null | grep -q ":${PORT} "; then
        PROCESS=$(ss -tlnp 2>/dev/null | grep ":${PORT} " | head -1)
        echo -e "${YELLOW}⚠ Port ${PORT} is in use${NC}"
        echo -e "  ${PROCESS}"
    else
        echo -e "${GREEN}✓ Port ${PORT} is available${NC}"
    fi
done
echo ""

# Check Docker networks
echo -e "${BLUE}Docker Networks:${NC}"
docker network ls
echo ""

# Check Docker volumes
echo -e "${BLUE}Docker Volumes:${NC}"
docker volume ls | head -10
echo ""

# Summary
echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Summary                                      ║${NC}"
echo -e "${GREEN}╠════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║ Docker Status:     Running                     ║${NC}"
echo -e "${GREEN}║ Total Images:      ${IMAGE_COUNT}                              ║${NC}"
echo -e "${GREEN}║ Total Containers:  ${TOTAL_COUNT}                              ║${NC}"
echo -e "${GREEN}║ Running:           ${RUNNING_COUNT}                              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Recommendations
echo -e "${BLUE}Recommendations:${NC}"
if [ $RUNNING_COUNT -eq 0 ]; then
    echo -e "${YELLOW}• No containers running. Start services with:${NC}"
    echo -e "  ${GREEN}docker-compose up -d${NC}"
fi

if [ $TOTAL_COUNT -gt 10 ]; then
    echo -e "${YELLOW}• Many stopped containers detected. Clean up with:${NC}"
    echo -e "  ${GREEN}docker container prune${NC}"
fi

# Check if cleanup is needed
DANGLING_IMAGES=$(docker images -f "dangling=true" -q | wc -l)
if [ $DANGLING_IMAGES -gt 0 ]; then
    echo -e "${YELLOW}• ${DANGLING_IMAGES} dangling images found. Clean up with:${NC}"
    echo -e "  ${GREEN}docker image prune${NC}"
fi

echo ""
echo -e "${GREEN}✓ Status check complete!${NC}"

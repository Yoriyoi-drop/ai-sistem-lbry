#!/bin/bash

# Script untuk Push Docker Image ke Docker Hub dengan nama tag Nexaproge
# Usage: ./push_nexaproge_to_docker.sh [dockerhub_username]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Push Docker Image - Nexaproge AI Security ===${NC}"
echo ""

# Get Docker Hub username
if [ -z "$1" ]; then
    echo -e "${YELLOW}Enter your Docker Hub username:${NC}"
    read DOCKER_USERNAME
else
    DOCKER_USERNAME=$1
fi

echo -e "${GREEN}Docker Hub Username: ${DOCKER_USERNAME}${NC}"
echo ""

# Check if logged in to Docker Hub
echo -e "${YELLOW}Checking Docker Hub login...${NC}"
if ! docker info | grep -q "Username: ${DOCKER_USERNAME}"; then
    echo -e "${YELLOW}Please login to Docker Hub:${NC}"
    docker login
else
    echo -e "${GREEN}✓ Already logged in${NC}"
fi
echo ""

# Build the image with Nexaproge tag
echo -e "${YELLOW}Building Docker image with Nexaproge tag...${NC}"

# Build with multiple tags: latest, version, and nexaproge
docker build -f Dockerfile.nexaproge -t ${DOCKER_USERNAME}/infinite-ai-security:nexaproge .
docker build -f Dockerfile.nexaproge -t ${DOCKER_USERNAME}/infinite-ai-security:latest .

echo -e "${GREEN}✓ Image built successfully${NC}"
echo ""

# Tag and push the image
IMAGES=(
    "infinite-ai-security:nexaproge"
    "infinite-ai-security:latest"
)

for IMAGE in "${IMAGES[@]}"; do
    echo -e "${GREEN}Processing: ${IMAGE}${NC}"

    IMAGE_NAME=$(echo $IMAGE | cut -d: -f1)
    IMAGE_TAG=$(echo $IMAGE | cut -d: -f2)

    # Check if image exists locally
    if docker images | grep -q "${IMAGE_NAME}"; then
        echo -e "${GREEN}✓ Image found locally${NC}"

        # Tag for Docker Hub
        DOCKER_HUB_TAG="${DOCKER_USERNAME}/${IMAGE}"
        echo -e "${YELLOW}Tagging as: ${DOCKER_HUB_TAG}${NC}"

        # Push to Docker Hub
        echo -e "${YELLOW}Pushing to Docker Hub...${NC}"
        docker push ${DOCKER_HUB_TAG}

        echo -e "${GREEN}✓ Successfully pushed ${DOCKER_HUB_TAG}${NC}"
        echo ""
    else
        echo -e "${RED}✗ Image not found: ${IMAGE}${NC}"
        echo ""
    fi
done

# Build and push minimal version too
echo -e "${YELLOW}Building and pushing minimal version...${NC}"
docker build -f Dockerfile.minimal -t ${DOCKER_USERNAME}/infinite-ai-security:minimal .
docker push ${DOCKER_USERNAME}/infinite-ai-security:minimal

# Build and push production version too
echo -e "${YELLOW}Building and pushing production version...${NC}"
docker build -f Dockerfile.production -t ${DOCKER_USERNAME}/infinite-ai-security:production .
docker push ${DOCKER_USERNAME}/infinite-ai-security:production

# Summary
echo -e "${GREEN}=== Push Summary ===${NC}"
echo -e "${GREEN}Successfully pushed images:${NC}"
echo "  - ${DOCKER_USERNAME}/infinite-ai-security:nexaproge"
echo "  - ${DOCKER_USERNAME}/infinite-ai-security:latest"
echo "  - ${DOCKER_USERNAME}/infinite-ai-security:minimal"
echo "  - ${DOCKER_USERNAME}/infinite-ai-security:production"
echo ""

echo -e "${GREEN}=== Pull Commands ===${NC}"
echo -e "${YELLOW}To pull these images on another machine:${NC}"
echo "  docker pull ${DOCKER_USERNAME}/infinite-ai-security:nexaproge"
echo "  docker pull ${DOCKER_USERNAME}/infinite-ai-security:latest"
echo "  docker pull ${DOCKER_USERNAME}/infinite-ai-security:minimal"
echo "  docker pull ${DOCKER_USERNAME}/infinite-ai-security:production"
echo ""

echo -e "${GREEN}=== Docker Hub URLs ===${NC}"
echo "  https://hub.docker.com/r/${DOCKER_USERNAME}/infinite-ai-security"
echo ""

echo -e "${GREEN}✓ All done!${NC}"
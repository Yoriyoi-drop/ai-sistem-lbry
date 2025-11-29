#!/bin/bash

# Script untuk Push Docker Images ke Docker Hub
# Usage: ./push_to_dockerhub.sh [username]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Docker Hub Push Script ===${NC}"
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

# List of images to push
declare -a IMAGES=(
    "citadel-agent-api:latest"
    "citadel-agent:latest"
)

# Tag and push each image
for IMAGE in "${IMAGES[@]}"; do
    echo -e "${GREEN}Processing: ${IMAGE}${NC}"
    
    # Extract image name and tag
    IMAGE_NAME=$(echo $IMAGE | cut -d: -f1)
    IMAGE_TAG=$(echo $IMAGE | cut -d: -f2)
    
    # Check if image exists locally
    if docker images | grep -q "${IMAGE_NAME}"; then
        echo -e "${GREEN}✓ Image found locally${NC}"
        
        # Tag for Docker Hub
        DOCKER_HUB_TAG="${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
        echo -e "${YELLOW}Tagging as: ${DOCKER_HUB_TAG}${NC}"
        docker tag ${IMAGE} ${DOCKER_HUB_TAG}
        
        # Push to Docker Hub
        echo -e "${YELLOW}Pushing to Docker Hub...${NC}"
        docker push ${DOCKER_HUB_TAG}
        
        echo -e "${GREEN}✓ Successfully pushed ${DOCKER_HUB_TAG}${NC}"
        echo ""
    else
        echo -e "${RED}✗ Image not found: ${IMAGE}${NC}"
        echo -e "${YELLOW}Building image...${NC}"
        
        # Try to build the image
        if [ -f "Dockerfile" ]; then
            docker build -t ${IMAGE} .
            
            # Tag and push
            DOCKER_HUB_TAG="${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
            docker tag ${IMAGE} ${DOCKER_HUB_TAG}
            docker push ${DOCKER_HUB_TAG}
            
            echo -e "${GREEN}✓ Built and pushed ${DOCKER_HUB_TAG}${NC}"
        else
            echo -e "${RED}✗ Dockerfile not found, skipping...${NC}"
        fi
        echo ""
    fi
done

# Summary
echo -e "${GREEN}=== Push Summary ===${NC}"
echo -e "${GREEN}Pushed images:${NC}"
for IMAGE in "${IMAGES[@]}"; do
    IMAGE_NAME=$(echo $IMAGE | cut -d: -f1)
    IMAGE_TAG=$(echo $IMAGE | cut -d: -f2)
    echo -e "  - ${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
done
echo ""

echo -e "${GREEN}=== Pull Commands ===${NC}"
echo -e "${YELLOW}To pull these images on another machine:${NC}"
for IMAGE in "${IMAGES[@]}"; do
    IMAGE_NAME=$(echo $IMAGE | cut -d: -f1)
    IMAGE_TAG=$(echo $IMAGE | cut -d: -f2)
    echo -e "  docker pull ${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
done
echo ""

echo -e "${GREEN}=== Docker Hub URLs ===${NC}"
for IMAGE in "${IMAGES[@]}"; do
    IMAGE_NAME=$(echo $IMAGE | cut -d: -f1)
    echo -e "  https://hub.docker.com/r/${DOCKER_USERNAME}/${IMAGE_NAME}"
done
echo ""

echo -e "${GREEN}✓ All done!${NC}"

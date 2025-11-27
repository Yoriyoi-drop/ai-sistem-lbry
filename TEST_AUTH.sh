#!/bin/bash

echo "========================================="
echo "🧪 AUTH FLOW TESTING - Quick Start"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "apps/dashboard" ]; then
    echo "❌ Error: Must run from project root directory"
    exit 1
fi

echo -e "${BLUE}Step 1: Setting up environment...${NC}"

# Copy .env.example to .env if not exists
if [ ! -f "apps/dashboard/.env" ]; then
    echo "Creating .env file..."
    cp apps/dashboard/.env.example apps/dashboard/.env
    echo -e "${GREEN}✅ .env file created${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

echo ""
echo -e "${BLUE}Step 2: Installing dependencies...${NC}"

# Check if node_modules exists
if [ ! -d "apps/dashboard/node_modules" ]; then
    echo "Installing npm packages..."
    cd apps/dashboard
    npm install
    cd ../..
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${GREEN}✅ Dependencies already installed${NC}"
fi

echo ""
echo -e "${BLUE}Step 3: Starting development server...${NC}"
echo ""

cd apps/dashboard
npm run dev


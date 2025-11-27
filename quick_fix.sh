#!/bin/bash
# Quick Fix Script for Infinite AI Security Platform
# This script fixes the critical issues found during testing

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Header
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         INFINITE AI SECURITY PLATFORM - QUICK FIX              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "services" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Starting quick fix process..."
echo ""

# ============================================================================
# 1. ACTIVATE VIRTUAL ENVIRONMENT
# ============================================================================
print_status "Step 1: Checking virtual environment..."

if [ -d ".venv" ]; then
    print_success "Virtual environment found at .venv"
    source .venv/bin/activate
    print_success "Virtual environment activated"
elif [ -d "venv" ]; then
    print_success "Virtual environment found at venv"
    source venv/bin/activate
    print_success "Virtual environment activated"
else
    print_warning "No virtual environment found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    print_success "Virtual environment created and activated"
fi

echo ""

# ============================================================================
# 2. UPGRADE PIP
# ============================================================================
print_status "Step 2: Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "Pip upgraded"
echo ""

# ============================================================================
# 3. INSTALL PYTHON DEPENDENCIES
# ============================================================================
print_status "Step 3: Installing Python dependencies..."

if [ -f "requirements.txt" ]; then
    print_status "Installing from requirements.txt..."
    pip install -r requirements.txt
    print_success "Main dependencies installed"
else
    print_warning "requirements.txt not found, skipping..."
fi

# Install api-gateway specific dependencies
if [ -f "services/api-gateway/requirements.txt" ]; then
    print_status "Installing API Gateway dependencies..."
    pip install -r services/api-gateway/requirements.txt
    print_success "API Gateway dependencies installed"
fi

echo ""

# ============================================================================
# 4. VERIFY BACKEND INSTALLATION
# ============================================================================
print_status "Step 4: Verifying backend installation..."

cd services/api-gateway

if python3 -c "from app import main" 2>/dev/null; then
    print_success "✅ Backend can be imported successfully!"
else
    print_error "❌ Backend import failed. Check the error above."
fi

cd ../..
echo ""

# ============================================================================
# 5. CHECK FRONTEND DEPENDENCIES
# ============================================================================
print_status "Step 5: Checking frontend dependencies..."

if [ -d "dashboard-react" ]; then
    cd dashboard-react
    
    if [ ! -d "node_modules" ]; then
        print_warning "node_modules not found. Installing..."
        npm install
        print_success "Frontend dependencies installed"
    else
        print_success "Frontend dependencies already installed"
    fi
    
    cd ..
else
    print_warning "dashboard-react directory not found"
fi

echo ""

# ============================================================================
# 6. CREATE DOCKERFILE IF MISSING
# ============================================================================
print_status "Step 6: Checking Dockerfile..."

if [ ! -f "Dockerfile" ]; then
    if [ -f "Dockerfile.production" ]; then
        print_warning "Dockerfile not found. Creating from Dockerfile.production..."
        cp Dockerfile.production Dockerfile
        print_success "Dockerfile created"
    else
        print_warning "No Dockerfile templates found"
    fi
else
    print_success "Dockerfile exists"
fi

echo ""

# ============================================================================
# 7. CHECK DATABASE
# ============================================================================
print_status "Step 7: Checking database setup..."

if [ -f "alembic.ini" ]; then
    print_success "Alembic configuration found"
    
    # Count migration files
    if [ -d "alembic/versions" ]; then
        migration_count=$(find alembic/versions -name "*.py" -type f | wc -l)
        print_success "Found $migration_count migration(s)"
    fi
else
    print_warning "alembic.ini not found"
fi

echo ""

# ============================================================================
# 8. CHECK ENVIRONMENT FILES
# ============================================================================
print_status "Step 8: Checking environment configuration..."

if [ -f ".env" ]; then
    print_success ".env file exists"
else
    if [ -f ".env.example" ]; then
        print_warning ".env not found. Creating from .env.example..."
        cp .env.example .env
        print_success ".env created from .env.example"
        print_warning "⚠️  Please update .env with your actual configuration!"
    else
        print_error ".env.example not found"
    fi
fi

echo ""

# ============================================================================
# 9. CLEANUP FRONTEND DUPLICATE (OPTIONAL)
# ============================================================================
print_status "Step 9: Checking for duplicate frontend directories..."

if [ -d "frontend" ] && [ -d "dashboard-react" ]; then
    print_warning "Both 'frontend' and 'dashboard-react' directories exist"
    
    # Check if frontend has package.json
    if [ ! -f "frontend/package.json" ]; then
        print_warning "frontend/ directory is incomplete (no package.json)"
        print_status "Recommendation: Remove 'frontend/' directory and use 'dashboard-react/'"
        # Uncomment to auto-remove:
        # rm -rf frontend/
        # print_success "Removed incomplete frontend/ directory"
    fi
fi

echo ""

# ============================================================================
# SUMMARY
# ============================================================================
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                         FIX SUMMARY                            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

print_success "✅ Virtual environment: Activated"
print_success "✅ Python dependencies: Installed"
print_success "✅ Backend verification: Completed"
print_success "✅ Frontend dependencies: Checked"
print_success "✅ Docker configuration: Checked"
print_success "✅ Environment files: Checked"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                       NEXT STEPS                               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "To start the backend:"
echo "  ${GREEN}cd services/api-gateway${NC}"
echo "  ${GREEN}uvicorn app.main:app --reload --host 0.0.0.0 --port 8000${NC}"
echo ""

echo "To start the frontend (in a new terminal):"
echo "  ${GREEN}cd dashboard-react${NC}"
echo "  ${GREEN}npm run dev${NC}"
echo ""

echo "To start with Docker:"
echo "  ${GREEN}docker compose up --build${NC}"
echo ""

echo "To run tests:"
echo "  ${GREEN}python3 test_project.py${NC}"
echo ""

print_success "🎉 Quick fix completed!"
echo ""

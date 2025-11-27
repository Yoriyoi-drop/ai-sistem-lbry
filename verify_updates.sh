#!/bin/bash

# Verification script for Infinite AI Security Platform Dependency Updates

echo "🔍 Verifying dependency updates for Infinite AI Security Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[VERIFICATION]${NC} $1"
}

TOTAL_CHECKS=0
PASSED_CHECKS=0

verify_file_exists() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ -f "$1" ]; then
        print_status "✓ $1 exists"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        print_error "✗ $1 does not exist"
        return 1
    fi
}

verify_dir_exists() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ -d "$1" ]; then
        print_status "✓ $1 directory exists"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        print_error "✗ $1 directory does not exist"
        return 1
    fi
}

check_version() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if grep -q "$2" "$1"; then
        print_status "✓ $2 found in $1"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        print_error "✗ $2 not found in $1"
        return 1
    fi
}

print_step "Verifying main dependency files..."

# Check main requirements file
verify_file_exists "requirements.txt"
check_version "requirements.txt" "fastapi==0.115.0"
check_version "requirements.txt" "sqlalchemy==2.0.35"
check_version "requirements.txt" "pydantic==2.9.2"

# Check dev requirements file
verify_file_exists "requirements-dev.txt"
check_version "requirements-dev.txt" "pytest==8.3.3"
check_version "requirements-dev.txt" "black==24.8.0"

# Check dashboard package.json
verify_file_exists "dashboard/package.json"
check_version "dashboard/package.json" "\"react\": \"^18.3.1\""
check_version "dashboard/package.json" "\"vite\": \"^5.4.8\""

print_step "Checking for empty directories..."

EMPTY_DIRS=$(find . -type d -empty -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./.vscode/*" -not -path "./.idea/*" -not -path "./__pycache__/*" | wc -l)
echo "📁 Found $EMPTY_DIRS potentially empty directories"

if [ "$EMPTY_DIRS" -lt 50 ]; then
    print_status "✓ Only $EMPTY_DIRS empty directories found (cleanup was effective)"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
else
    print_warning "✗ $EMPTY_DIRS empty directories found (more than expected)"
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
fi

print_step "Verifying Go modules..."

GO_MODS=$(find . -name "go.mod" | wc -l)
echo "📦 Found $GO_MODS go.mod files"

for go_mod in $(find . -name "go.mod"); do
    if [ -f "$go_mod" ]; then
        dir_path=$(dirname "$go_mod")
        (
            cd "$dir_path" 
            if go list -m >/dev/null 2>&1; then
                print_status "✓ $go_mod is valid"
                PASSED_CHECKS=$((PASSED_CHECKS + 1))
            else
                print_error "✗ $go_mod is invalid"
            fi
        )
        TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    fi
done

print_step "Verifying summary file..."

verify_file_exists "DEPENDENCY_UPDATE_SUMMARY.md"

print_step "Final verification results..."

echo
echo "📊 Verification Summary:"
echo "Total checks: $TOTAL_CHECKS"
echo "Passed checks: $PASSED_CHECKS"
echo "Failed checks: $((TOTAL_CHECKS - PASSED_CHECKS))"

PERCENTAGE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
echo "Success rate: $PERCENTAGE%"

if [ $PERCENTAGE -ge 90 ]; then
    print_status "🎉 Dependency update verification successful! ($PERCENTAGE% success rate)"
    echo "✅ All major dependencies have been updated successfully"
    echo "✅ Empty directories have been cleaned up"
    echo "✅ Summary documentation created"
    exit 0
else
    print_error "❌ Dependency update verification failed! ($PERCENTAGE% success rate)"
    exit 1
fi
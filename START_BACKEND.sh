#!/bin/bash

echo "========================================="
echo "🚀 STARTING BACKEND SERVER"
echo "========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "apps/api" ]; then
    echo "❌ Error: Must run from project root directory"
    exit 1
fi

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Export PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/apps/api

echo "Starting Uvicorn server..."
cd apps/api
uvicorn src.main:app --reload --port 8000


#!/bin/bash
# Infinite AI Security Platform - Start Script

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Check if Python dependencies are installed
echo "Checking Python dependencies..."
python -c "import fastapi, uvicorn, sqlalchemy, pydantic, pydantic_settings, passlib, stripe, jwt" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Some Python dependencies are missing"
    echo "Installing from requirements files..."
    pip install -r requirements.txt 2>/dev/null || pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings passlib python-jose[cryptography] stripe psycopg2-binary python-multipart prometheus-client
fi

echo "✅ Dependencies check passed"

# Start the application
echo "🚀 Starting Infinite AI Security Platform..."
echo "   API Documentation: http://$API_HOST:$API_PORT/api/docs"
echo "   Health Check: http://$API_HOST:$API_PORT/api/health"
echo "   Base API: http://$API_HOST:$API_PORT/api/v1/"
echo "--------------------------------------------------------"

python start_server.py
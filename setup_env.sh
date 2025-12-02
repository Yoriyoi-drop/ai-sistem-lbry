#!/bin/bash
# Infinite AI Security Platform - Setup Environment

# Check if .env file exists, create if not
if [ ! -f .env ]; then
    echo "Creating .env file with default values..."
    cat > .env << EOF
# Infinite AI Security Platform - Environment Variables
API_SECRET_KEY=your-super-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
API_DEBUG=true
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=info

# Database Configuration
DATABASE_URL=sqlite:///./infinite_ai_security.db

# Security Configuration
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_MINUTES=43200

# Rate Limiting
RATE_LIMIT_DEFAULT=100
RATE_LIMIT_WINDOW=3600

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://localhost:3001
EOF
    echo "✅ .env file created with default values"
    echo "⚠️  IMPORTANT: Change the secret keys in .env before production!"
fi

echo "Environment setup complete!"
echo ""
echo "To start the application, run:"
echo "  python start_server.py"
echo ""
echo "Or directly with uvicorn:"
echo "  uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
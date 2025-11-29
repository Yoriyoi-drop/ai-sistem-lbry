#!/bin/bash
# Test script to verify the systemd service setup

echo "🔍 Verifying systemd service setup..."

# Check if the service file exists in the systemd directory
if [ -f /etc/systemd/system/infinite-ai-security.service ]; then
    echo "✅ Service file exists in systemd directory"
else
    echo "❌ Service file missing from systemd directory"
fi

# Check the content of the service file
echo ""
echo "📋 Service file content:"
echo "------------------------"
cat /etc/systemd/system/infinite-ai-security.service 2>/dev/null || echo "Cannot read service file - may require sudo"
echo ""

# Test docker-compose availability
echo "🐳 Checking Docker Compose availability..."
if command -v docker-compose &> /dev/null; then
    echo "✅ docker-compose is available"
    DOCKER_COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    echo "✅ docker compose (v2) is available"
    DOCKER_COMPOSE_CMD="docker compose"
else
    echo "❌ Neither docker-compose nor docker compose is available"
    DOCKER_COMPOSE_CMD=""
fi

# Test that docker is available
if command -v docker &> /dev/null; then
    echo "✅ Docker is available"
else
    echo "❌ Docker is not available"
fi

echo ""
echo "🔧 Manual test commands (you may need to run these with sudo):"
echo ""
echo "1. To reload systemd daemon:"
echo "   sudo systemctl daemon-reload"
echo ""
echo "2. To check service status:"
echo "   sudo systemctl status infinite-ai-security.service"
echo ""
echo "3. To start the service:"
echo "   sudo systemctl start infinite-ai-security"
echo ""
echo "4. To check if service is enabled for auto-start:"
echo "   sudo systemctl is-enabled infinite-ai-security"
echo ""

# Show the status of our currently running autonomous system
echo "🤖 Currently running autonomous system:"
ps aux | grep "autonomous_operation.sh" | grep -v grep

echo ""
echo "✅ Verification complete"
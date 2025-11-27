#!/bin/bash

####################################################################
# Health Check Endpoint Setup
# Pastikan setiap service memiliki /health endpoint
####################################################################

set -e

PROJECT_PATH="/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security"
HEALTHCHECK_DIR="$PROJECT_PATH/healthcheck"

echo "🏥 Setting up Health Check Endpoints..."

# Create healthcheck directory
mkdir -p "$HEALTHCHECK_DIR"

# Create FastAPI health endpoint
cat > "$HEALTHCHECK_DIR/api_health.py" << 'EOF'
"""
Health Check Endpoint untuk FastAPI
Tambahkan di main app.py:

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/health")
async def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }
    )

@app.get("/health/ready")
async def readiness_check():
    # Check database connection
    # Check Redis connection
    # Check dependencies
    return JSONResponse(
        status_code=200,
        content={"status": "ready"}
    )

@app.get("/health/live")
async def liveness_check():
    return JSONResponse(
        status_code=200,
        content={"status": "alive"}
    )
"""
EOF

echo "✓ API health endpoint template dibuat"

# Create a simple health check script for containers
cat > "$HEALTHCHECK_DIR/health_check.sh" << 'EOF'
#!/bin/bash

# Generic health check script
# Gunakan dalam Dockerfile healthcheck

PORT=${1:-8000}
ENDPOINT=${2:-/health}

# Try to connect to service
if curl -f http://localhost:$PORT$ENDPOINT > /dev/null 2>&1; then
    exit 0
else
    exit 1
fi
EOF

chmod +x "$HEALTHCHECK_DIR/health_check.sh"

echo "✓ Health check script dibuat"

# Create monitoring script
cat > "$HEALTHCHECK_DIR/monitor_health.py" << 'EOF'
#!/usr/bin/env python3
"""
Monitor Health Status of All Services
Real-time monitoring dashboard
"""

import subprocess
import time
import json
from datetime import datetime

def check_container_health(container_name):
    """Check if container is healthy"""
    try:
        result = subprocess.run(
            ['docker', 'inspect', '--format={{.State.Health.Status}}', container_name],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def check_service_endpoint(port):
    """Check if service is responding"""
    try:
        result = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', f'http://localhost:{port}/health'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return "Timeout"

def main():
    containers = [
        ('astramind', 8001),
        ('spectralogic', 8002),
        ('forgerun', 8003),
        ('guardianos', 8004),
        ('infinite-ai-api', 8000),
        ('infinite-ai-nginx', 80),
        ('infinite-ai-db', 5432),
        ('infinite-ai-redis', 6379),
    ]
    
    print("\n" + "="*80)
    print(f"🏥 NexaForge Health Status Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")
    
    for container, port in containers:
        health = check_container_health(container)
        status_code = check_service_endpoint(port)
        
        # Determine emoji
        if health == "healthy" or status_code.startswith('2'):
            emoji = "✅"
        elif health == "starting":
            emoji = "⏳"
        else:
            emoji = "❌"
        
        print(f"{emoji} {container:30} | Health: {health:15} | HTTP: {status_code}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(10)
EOF

chmod +x "$HEALTHCHECK_DIR/monitor_health.py"

echo "✓ Health monitoring script dibuat"

echo ""
echo "✅ Health Check Setup Completed!"
echo ""
echo "📝 Untuk menjalankan monitoring:"
echo "   python3 $HEALTHCHECK_DIR/monitor_health.py"
echo ""

exit 0

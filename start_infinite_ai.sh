#!/bin/bash
# Startup script for Infinite AI Security - Runs at system boot
# This script is designed to be called from crontab @reboot

# Wait for system to be fully ready
sleep 45

# Log file
LOG_FILE="/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/logs/boot_startup.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

log_message "Starting Infinite AI Security auto-start process..."

# Ensure we're in the right directory
cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security || {
    log_message "ERROR: Cannot change to application directory"
    exit 1
}

# Check if Docker is running
if ! systemctl is-active --quiet docker; then
    log_message "INFO: Docker service is not active, waiting..."
    # For systems where user can't start system services, wait longer
    sleep 30
fi

# Wait for Docker to be ready
MAX_WAIT=60
COUNT=0
while [ $COUNT -lt $MAX_WAIT ]; do
    if docker info > /dev/null 2>&1; then
        log_message "INFO: Docker is ready"
        break
    fi
    sleep 5
    COUNT=$((COUNT + 1))
done

if [ $COUNT -eq $MAX_WAIT ]; then
    log_message "ERROR: Docker not ready after waiting"
    exit 1
fi

# Start Ollama service first
log_message "INFO: Starting Ollama service..."
docker-compose -f docker-compose.ollama.yml up -d ollama

# Wait for Ollama to be ready
sleep 30

# Check if Ollama API is accessible
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    log_message "INFO: Ollama API is accessible"
else
    log_message "WARN: Ollama API not accessible, waiting longer..."
    sleep 30
fi

# Start the autonomous operation system
log_message "INFO: Starting autonomous operation system..."
./autonomous_operation.sh start

log_message "INFO: Auto-start process completed"

# Final status check
if ./autonomous_operation.sh status | grep -q "running"; then
    log_message "INFO: Autonomous system is successfully running"
else
    log_message "WARN: Autonomous system may not be running correctly"
fi
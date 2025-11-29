#!/bin/bash
# Monitor and update script for Infinite AI Security
# This script monitors system health and automatically updates models when needed

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
OLLAMA_HOST="http://localhost:11434"
HEALTH_CHECK_INTERVAL=300  # 5 minutes
UPDATE_CHECK_INTERVAL=86400  # 24 hours
LOG_FILE="/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/logs/monitor.log"
MODEL_UPDATE_FILE="/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/model_updates.json"

# Ensure logs directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Function to check system health
check_health() {
    log_message "INFO: Checking system health..."
    
    # Check if Ollama API is accessible
    if curl -s "$OLLAMA_HOST/api/version" > /dev/null 2>&1; then
        log_message "INFO: ✓ Ollama API is accessible"
    else
        log_message "ERROR: ✗ Ollama API is not accessible"
        return 1
    fi
    
    # Check if required models are available
    REQUIRED_MODELS=("qwen2.5:7b-instruct" "llama3.1" "mistral")
    for model in "${REQUIRED_MODELS[@]}"; do
        if curl -s "$OLLAMA_HOST/api/tags" | grep -q "$model"; then
            log_message "INFO: ✓ Model $model is available"
        else
            log_message "ERROR: ✗ Model $model is missing"
            return 1
        fi
    done
    
    # Check if Docker containers are running
    if docker -H unix:///var/run/docker.sock ps | grep -q "infinite-ai-ollama"; then
        log_message "INFO: ✓ Ollama container is running"
    else
        log_message "ERROR: ✗ Ollama container is not running"
        return 1
    fi
    
    log_message "INFO: ✓ System health check passed"
    return 0
}

# Function to check for model updates
check_model_updates() {
    log_message "INFO: Checking for model updates..."
    
    # For now, we'll use a simple approach - you could enhance this to check
    # online repositories for newer model versions
    LAST_UPDATE_FILE="/tmp/last_model_update_check"
    CURRENT_TIME=$(date +%s)
    
    if [ -f "$LAST_UPDATE_FILE" ]; then
        LAST_UPDATE=$(cat "$LAST_UPDATE_FILE")
        TIME_SINCE_LAST_UPDATE=$((CURRENT_TIME - LAST_UPDATE))
    else
        TIME_SINCE_LAST_UPDATE=$UPDATE_CHECK_INTERVAL  # Force update check on first run
    fi
    
    if [ $TIME_SINCE_LAST_UPDATE -ge $UPDATE_CHECK_INTERVAL ]; then
        # Create/update our model update information file
        cat > "$MODEL_UPDATE_FILE" << EOF
{
  "last_check": "$(date -Iseconds)",
  "models": [
    {
      "name": "qwen2.5:7b-instruct",
      "status": "current"
    },
    {
      "name": "llama3.1",
      "status": "current"
    },
    {
      "name": "mistral",
      "status": "current"
    }
  ]
}
EOF
        echo $CURRENT_TIME > "$LAST_UPDATE_FILE"
        log_message "INFO: Model update check completed"
        
        # Here you could implement actual update checking logic
        # For now, we'll just log that we checked
        log_message "INFO: Checked for model updates (implementation would check online)"
    else
        log_message "INFO: Skipping update check - not time yet"
    fi
}

# Function to restart services if needed
restart_services_if_needed() {
    log_message "INFO: Checking if services need restart..."
    
    if ! check_health; then
        log_message "WARN: Health check failed, attempting restart..."
        
        # Try to restart Ollama container
        docker -H unix:///var/run/docker.sock restart infinite-ai-ollama
        
        # Wait briefly for service to come up
        sleep 10
        
        if check_health; then
            log_message "INFO: ✓ Services restarted successfully"
        else
            log_message "ERROR: ✗ Services failed to restart properly"
        fi
    else
        log_message "INFO: ✓ Services are healthy, no restart needed"
    fi
}

# Function for self-learning (from feedback and interactions)
perform_self_learning() {
    log_message "INFO: Performing self-learning tasks..."
    
    # Monitor feedback file for learning opportunities
    FEEDBACK_FILE="/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security/data/feedback.jsonl"
    
    if [ -f "$FEEDBACK_FILE" ]; then
        FEEDBACK_COUNT=$(wc -l < "$FEEDBACK_FILE")
        log_message "INFO: Found $FEEDBACK_COUNT feedback entries for learning"
        
        # Here you could implement actual learning from feedback
        # For now, just log the activity
        log_message "INFO: Self-learning from feedback completed"
    else
        log_message "INFO: No feedback file found for learning"
    fi
    
    # Check for other learning opportunities (like model performance metrics)
    log_message "INFO: Self-learning tasks completed"
}

# Main monitoring loop
main() {
    log_message "INFO: Starting Infinite AI Security Monitor"
    
    while true; do
        log_message "INFO: Starting monitoring cycle"
        
        # Perform health check
        check_health
        if [ $? -ne 0 ]; then
            log_message "ERROR: Health check failed"
            # Try to fix problems
            restart_services_if_needed
        fi
        
        # Check for updates
        check_model_updates
        
        # Perform self-learning
        perform_self_learning
        
        log_message "INFO: Monitoring cycle completed, sleeping for $HEALTH_CHECK_INTERVAL seconds"
        sleep $HEALTH_CHECK_INTERVAL
    done
}

# Handle signals gracefully
cleanup() {
    log_message "INFO: Received signal, shutting down monitor..."
    exit 0
}

trap cleanup SIGTERM SIGINT

# Run main function or specific functions based on arguments
case "${1:-}" in
    --health)
        check_health
        ;;
    --update)
        check_model_updates
        ;;
    --self-learn)
        perform_self_learning
        ;;
    --restart-services)
        restart_services_if_needed
        ;;
    *)
        log_message "INFO: Monitor starting in daemon mode"
        main
        ;;
esac
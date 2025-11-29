#!/bin/bash
# Autonomous Operation Script for Infinite AI Security
# This script runs the system continuously with self-healing, self-monitoring, and self-improvement

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
MAIN_APP_DIR="/home/whale-d/Unduhan/backup/ai-p/infinite_ai_security"
LOG_FILE="$MAIN_APP_DIR/logs/autonomous_operation.log"
PID_FILE="/tmp/infinite_ai_autonomous.pid"
HEALTH_CHECK_INTERVAL=60  # 1 minute
UPDATE_CHECK_INTERVAL=3600  # 1 hour
MONITOR_SCRIPT="$MAIN_APP_DIR/monitor_updates.sh"
AUTO_UPDATE_SCRIPT="$MAIN_APP_DIR/auto_update_self_learn.sh"
MAIN_PYTHON_APP="$MAIN_APP_DIR/main.py"

# Ensure logs directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Function to check if main app is running
is_main_app_running() {
    if pgrep -f "python.*main.py" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to start main application
start_main_app() {
    log_message "INFO: Starting main application..."
    
    if [ -f "$MAIN_PYTHON_APP" ]; then
        # Set environment variables for the main app
        export OLLAMA_HOST="http://localhost:11434"
        export MODEL_NAME="qwen2.5:7b-instruct"
        
        # Start the main application in the background
        cd "$MAIN_APP_DIR"
        python "$MAIN_PYTHON_APP" > /tmp/main_app.log 2>&1 &
        MAIN_APP_PID=$!
        
        # Wait briefly to see if it starts successfully
        sleep 5
        
        if is_main_app_running; then
            log_message "INFO: Main application started successfully with PID $MAIN_APP_PID"
            echo $MAIN_APP_PID > /tmp/main_app.pid
            return 0
        else
            log_message "ERROR: Main application failed to start"
            cat /tmp/main_app.log >&2
            return 1
        fi
    else
        log_message "ERROR: Main application file not found: $MAIN_PYTHON_APP"
        return 1
    fi
}

# Function to stop main application
stop_main_app() {
    log_message "INFO: Stopping main application..."
    
    if is_main_app_running; then
        pkill -f "python.*main.py" || true
        sleep 2
        
        # Double-check it's stopped
        if is_main_app_running; then
            pkill -9 -f "python.*main.py" || true
            log_message "INFO: Force killed main application"
        else
            log_message "INFO: Main application stopped gracefully"
        fi
    else
        log_message "INFO: Main application was not running"
    fi
    
    rm -f /tmp/main_app.pid
}

# Function to restart main application
restart_main_app() {
    log_message "INFO: Restarting main application..."
    stop_main_app
    sleep 3
    start_main_app
}

# Function to perform comprehensive health check
perform_health_check() {
    log_message "INFO: Performing comprehensive health check..."
    
    # Check if Ollama is responding
    if ! curl -s "$OLLAMA_HOST/api/version" > /dev/null 2>&1; then
        log_message "ERROR: Ollama API is not responding"
        return 1
    fi
    
    # Check if required models are available
    if ! curl -s "$OLLAMA_HOST/api/tags" | grep -q "qwen2.5:7b-instruct"; then
        log_message "ERROR: Required model qwen2.5:7b-instruct is not available"
        return 1
    fi
    
    # Check if main application is running
    if ! is_main_app_running; then
        log_message "ERROR: Main application is not running"
        return 1
    fi
    
    # Check if main application API is responding
    if ! curl -s "http://localhost:8000/health" > /dev/null 2>&1; then
        log_message "ERROR: Main application API is not responding"
        return 1
    fi
    
    log_message "INFO: ✓ All health checks passed"
    return 0
}

# Function to run self-improvement cycle
run_self_improvement() {
    log_message "INFO: Running self-improvement cycle..."
    
    if [ -f "$AUTO_UPDATE_SCRIPT" ]; then
        log_message "INFO: Executing auto-update and self-learning script"
        "$AUTO_UPDATE_SCRIPT" --autonomous-cycle
    else
        log_message "WARN: Auto-update script not found, skipping self-improvement"
    fi
}

# Function to run self-monitoring
run_self_monitoring() {
    log_message "INFO: Running self-monitoring cycle..."
    
    if [ -f "$MONITOR_SCRIPT" ]; then
        log_message "INFO: Executing monitoring script"
        "$MONITOR_SCRIPT" --health
    else
        log_message "WARN: Monitor script not found, skipping monitoring"
    fi
}

# Function to cleanup on exit
cleanup() {
    log_message "INFO: Received signal, shutting down autonomous system..."
    
    # Stop main application
    stop_main_app
    
    # Remove PID file
    rm -f "$PID_FILE"
    
    log_message "INFO: Autonomous system shutdown complete"
    exit 0
}

# Main autonomous loop
main_loop() {
    log_message "INFO: Starting autonomous operation loop"
    
    # Start the main application if not already running
    if ! is_main_app_running; then
        if ! start_main_app; then
            log_message "ERROR: Failed to start main application, exiting"
            exit 1
        fi
    fi
    
    # Run initial checks
    perform_health_check
    run_self_monitoring
    run_self_improvement
    
    # Store current PID
    echo $$ > "$PID_FILE"
    
    # Main loop
    while true; do
        log_message "INFO: Starting autonomous cycle"
        
        # Perform health check
        if ! perform_health_check; then
            log_message "WARN: Health check failed, attempting recovery"
            
            # Try to restart the system
            restart_main_app
            
            # Perform another check after restart
            if ! perform_health_check; then
                log_message "ERROR: System still not healthy after restart"
                # In a production system, you might want to escalate this
            else
                log_message "INFO: System recovered after restart"
            fi
        fi
        
        # Run monitoring and self-improvement periodically
        CURRENT_TIME=$(date +%s)
        if [ -z "$LAST_UPDATE_CHECK" ] || [ $((CURRENT_TIME - LAST_UPDATE_CHECK)) -ge $UPDATE_CHECK_INTERVAL ]; then
            run_self_monitoring
            run_self_improvement
            LAST_UPDATE_CHECK=$CURRENT_TIME
        fi
        
        log_message "INFO: Autonomous cycle completed, sleeping for $HEALTH_CHECK_INTERVAL seconds"
        sleep $HEALTH_CHECK_INTERVAL
    done
}

# Function to handle various commands
handle_command() {
    case "${1:-}" in
        start)
            log_message "INFO: Starting autonomous system..."
            if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
                log_message "INFO: Autonomous system is already running"
            else
                # Run main loop in background
                "$0" run &
                log_message "INFO: Autonomous system started in background"
            fi
            ;;
        stop)
            log_message "INFO: Stopping autonomous system..."
            if [ -f "$PID_FILE" ]; then
                PID=$(cat "$PID_FILE")
                kill -TERM $PID 2>/dev/null || true
                sleep 2
                # Force kill if still running
                kill -9 $PID 2>/dev/null || true
                rm -f "$PID_FILE"
                stop_main_app
                log_message "INFO: Autonomous system stopped"
            else
                log_message "INFO: Autonomous system is not running"
            fi
            ;;
        restart)
            "$0" stop
            sleep 3
            "$0" start
            ;;
        status)
            if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
                log_message "INFO: Autonomous system is running (PID: $(cat $PID_FILE))"
                # Perform a quick health check
                if perform_health_check; then
                    echo "Status: HEALTHY"
                else
                    echo "Status: UNHEALTHY"
                fi
            else
                log_message "INFO: Autonomous system is not running"
                echo "Status: STOPPED"
            fi
            ;;
        run)
            # Set up signal handlers
            trap cleanup SIGTERM SIGINT SIGQUIT
            
            # Execute the main loop
            main_loop
            ;;
        health)
            log_message "INFO: Performing health check..."
            if perform_health_check; then
                echo "System is HEALTHY"
                exit 0
            else
                echo "System is UNHEALTHY"
                exit 1
            fi
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|status|health|run}"
            echo "  start  - Start the autonomous system"
            echo "  stop   - Stop the autonomous system"
            echo "  restart - Restart the autonomous system"
            echo "  status - Check the status of the autonomous system"
            echo "  health - Perform a health check"
            echo "  run    - Run the autonomous loop (internal use)"
            exit 1
            ;;
    esac
}

# Run the command handler with all arguments
handle_command "$@"
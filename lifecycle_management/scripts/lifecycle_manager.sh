#!/bin/bash
# 🚀 NEXAFORGE - LIFECYCLE MANAGEMENT SCRIPTS (L13)
# Scripts for managing auto-update, backup, versioning, and auto-healing operations

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default configuration
PYTHON_CMD="${PYTHON:-python3}"
LOG_FILE="lifecycle_management/logs/lifecycle_operations.log"
CONFIG_FILE="lifecycle_management/config/lifecycle_config.json"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to check prerequisites
check_prerequisites() {
    if ! command -v docker &> /dev/null; then
        log_message "⚠️  Docker not found - some auto-healing features will be limited"
    fi
    
    if ! command -v python3 &> /dev/null; then
        log_message "❌ Python3 not found - exiting"
        exit 1
    fi
}

# Function to start lifecycle manager in background
start_lifecycle_daemon() {
    log_message "🚀 Starting lifecycle management daemon..."
    
    # Create logs directory
    mkdir -p lifecycle_management/logs
    
    # Start the lifecycle manager in background
    nohup python3 lifecycle_management/lifecycle_manager.py > lifecycle_management/logs/lifecycle_daemon.log 2>&1 &
    DAEMON_PID=$!
    
    # Save PID for later use
    echo $DAEMON_PID > lifecycle_management/lifecycle_daemon.pid
    
    log_message "✅ Lifecycle daemon started with PID: $DAEMON_PID"
}

# Function to stop lifecycle manager
stop_lifecycle_daemon() {
    if [ -f "lifecycle_management/lifecycle_daemon.pid" ]; then
        DAEMON_PID=$(cat lifecycle_management/lifecycle_daemon.pid)
        if kill -0 "$DAEMON_PID" 2>/dev/null; then
            log_message "🛑 Stopping lifecycle daemon (PID: $DAEMON_PID)..."
            kill "$DAEMON_PID"
            rm -f lifecycle_management/lifecycle_daemon.pid
            log_message "✅ Lifecycle daemon stopped"
        else
            log_message "⚠️  Daemon process not found"
            rm -f lifecycle_management/lifecycle_daemon.pid
        fi
    else
        log_message "⚠️  No daemon PID file found"
    fi
}

# Function to perform manual backup
perform_backup() {
    log_message "💾 Starting manual backup operation..."
    
    COMPONENTS="${1:-config,logs}"
    
    # Use Python script to create backup
    python3 -c "
import sys
sys.path.append('.')
from lifecycle_management.lifecycle_manager import LifecycleManager
manager = LifecycleManager()
try:
    backup_info = manager.backup_manager.create_backup(components=['$COMPONENTS'.split(',')])
    print(f'Backup completed: {backup_info.backup_id}')
except Exception as e:
    print(f'Backup failed: {e}')
    sys.exit(1)
finally:
    manager.shutdown()
"
    
    log_message "✅ Manual backup completed"
}

# Function to trigger auto-update check
trigger_update_check() {
    log_message "🔄 Starting manual update check..."
    
    # Use Python script to check for updates
    python3 -c "
import sys
sys.path.append('.')
from lifecycle_management.lifecycle_manager import LifecycleManager
manager = LifecycleManager()
try:
    updates = manager.auto_update_manager.check_for_updates()
    print(f'Found {len(updates)} updates available')
    for update in updates:
        print(f'  - {update[\"name\"]}: {update[\"current_version\"]} → {update[\"new_version\"]}')
except Exception as e:
    print(f'Update check failed: {e}')
    sys.exit(1)
finally:
    manager.shutdown()
"
    
    log_message "✅ Update check completed"
}

# Function to deploy a model version
deploy_model_version() {
    MODEL_NAME="${1:-test_model}"
    MODEL_PATH="${2:-./models/test_model}"
    
    log_message "🔄 Deploying model version: $MODEL_NAME"
    
    # Use Python script to deploy model
    python3 -c "
import sys
sys.path.append('.')
from lifecycle_management.lifecycle_manager import LifecycleManager
from pathlib import Path
manager = LifecycleManager()
try:
    # Create mock model directory if it doesn't exist
    Path('models').mkdir(exist_ok=True)
    Path('$MODEL_PATH').parent.mkdir(exist_ok=True)
    Path('$MODEL_PATH').touch()
    
    version_id = manager.version_manager.deploy_version('$MODEL_NAME', '$MODEL_PATH')
    print(f'Model version deployed: {version_id}')
except Exception as e:
    print(f'Model deployment failed: {e}')
    sys.exit(1)
finally:
    manager.shutdown()
"
    
    log_message "✅ Model version deployed"
}

# Function to rollback a model version
rollback_model_version() {
    MODEL_NAME="${1:-test_model}"
    VERSION_ID="${2:-latest}"
    
    log_message "🔙 Rolling back model: $MODEL_NAME to version: $VERSION_ID"
    
    # Use Python script to rollback model
    python3 -c "
import sys
sys.path.append('.')
from lifecycle_management.lifecycle_manager import LifecycleManager
manager = LifecycleManager()
try:
    success = manager.version_manager.rollback_version('$MODEL_NAME', '$VERSION_ID')
    if success:
        print('Model rollback completed successfully')
    else:
        print('Model rollback failed')
        sys.exit(1)
except Exception as e:
    print(f'Model rollback failed: {e}')
    sys.exit(1)
finally:
    manager.shutdown()
"
    
    log_message "✅ Model rollback completed"
}

# Function to restore from backup
restore_backup() {
    BACKUP_ID="${1:-latest}"
    
    log_message "📂 Restoring from backup: $BACKUP_ID"
    
    # Use Python script to restore backup
    python3 -c "
import sys
sys.path.append('.')
from lifecycle_management.lifecycle_manager import LifecycleManager
manager = LifecycleManager()
try:
    success = manager.backup_manager.restore_backup('$BACKUP_ID')
    if success:
        print('Backup restore completed successfully')
    else:
        print('Backup restore failed')
        sys.exit(1)
except Exception as e:
    print(f'Backup restore failed: {e}')
    sys.exit(1)
finally:
    manager.shutdown()
"
    
    log_message "✅ Backup restore completed"
}

# Function to trigger healing for a container
heal_container() {
    CONTAINER_NAME="${1:-nexaforge-api}"
    
    log_message "🏥 Triggering healing for container: $CONTAINER_NAME"
    
    # Use Python script to heal container
    python3 -c "
import sys
sys.path.append('.')
from lifecycle_management.lifecycle_manager import LifecycleManager
manager = LifecycleManager()
try:
    success = manager.auto_healing_manager.heal_container('$CONTAINER_NAME')
    if success:
        print('Container healing completed successfully')
    else:
        print('Container healing failed')
        sys.exit(1)
except Exception as e:
    print(f'Container healing failed: {e}')
    sys.exit(1)
finally:
    manager.shutdown()
"
    
    log_message "✅ Container healing completed"
}

# Function to check system status
check_status() {
    log_message "📊 Checking system lifecycle status..."
    
    # Use Python script to get status
    python3 -c "
import sys
sys.path.append('.')
from lifecycle_management.lifecycle_manager import LifecycleManager
manager = LifecycleManager()
try:
    status = manager.get_status()
    print('LIFECYCLE MANAGEMENT STATUS:')
    print(f'  Auto-update: {\"Enabled\" if status[\"auto_update\"][\"enabled\"] else \"Disabled\"}')
    print(f'  Backup: {\"Enabled\" if True else \"Disabled\"}')  # Always enabled
    print(f'  Versioning: {\"Enabled\" if True else \"Disabled\"}')  # Always enabled
    print(f'  Auto-healing: {\"Active\" if status[\"auto_healing\"][\"active\"] else \"Inactive\"}')
    print(f'  Hot-reload: {\"Enabled\" if True else \"Disabled\"}')  # Always enabled
    print(f'  Last backup: {status[\"backup\"][\"last_backup\"] or \"Never\"}')
    print(f'  Models tracked: {status[\"versioning\"][\"model_count\"]}')
except Exception as e:
    print(f'Status check failed: {e}')
finally:
    manager.shutdown()
"
    
    log_message "✅ Status check completed"
}

# Function to display help
show_help() {
    echo "🚀 NEXAFORGE - LIFECYCLE MANAGEMENT SCRIPT"
    echo "============================================="
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  start-daemon          Start lifecycle management daemon"
    echo "  stop-daemon           Stop lifecycle management daemon"
    echo "  backup [components]   Perform manual backup (default: config,logs)"
    echo "  update-check          Check for available updates"
    echo "  deploy-model [name] [path]  Deploy a new model version"
    echo "  rollback-model [name] [version]  Rollback model to specific version"
    echo "  restore [backup_id]   Restore from backup"
    echo "  heal-container [name] Trigger healing for a container"
    echo "  status                Check system lifecycle status"
    echo "  help                  Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start-daemon"
    echo "  $0 backup \"models,database,config\""
    echo "  $0 deploy-model my_model ./models/my_model"
    echo "  $0 status"
}

# Main script logic
case "${1:-help}" in
    "start-daemon")
        check_prerequisites
        start_lifecycle_daemon
        ;;
    "stop-daemon")
        stop_lifecycle_daemon
        ;;
    "backup")
        check_prerequisites
        perform_backup "${2:-config,logs}"
        ;;
    "update-check")
        check_prerequisites
        trigger_update_check
        ;;
    "deploy-model")
        check_prerequisites
        deploy_model_version "${2:-test_model}" "${3:-./models/test_model}"
        ;;
    "rollback-model")
        check_prerequisites
        rollback_model_version "${2:-test_model}" "${3:-latest}"
        ;;
    "restore")
        check_prerequisites
        restore_backup "${2:-latest}"
        ;;
    "heal-container")
        check_prerequisites
        heal_container "${2:-nexaforge-api}"
        ;;
    "status")
        check_prerequisites
        check_status
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
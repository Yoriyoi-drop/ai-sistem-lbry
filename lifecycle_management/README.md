# 🚀 NEXAFORGE - LIFECYCLE MANAGEMENT LAYER (L13)

The Lifecycle Management Layer (L13) provides comprehensive lifecycle management capabilities for the entire NexaForge system, including auto-update, backup/restore, model versioning, and auto-healing features.

## 📋 Components

### 1. Auto-Update Manager
- Automatic model and service update checking
- Scheduled update windows
- Backup before update
- Rollback on failure

### 2. Backup & Restore Manager
- Full system backup capabilities
- Component-based backups (models, database, config, logs)
- Backup scheduling
- Restore functionality

### 3. Model Version Manager
- Model version tracking
- Version deployment
- Rollback capabilities
- Version history

### 4. Auto-Healing Manager
- Container health monitoring
- Resource usage monitoring
- Automatic healing and restart
- Docker integration

### 5. Hot-Reload Manager
- File change detection
- Hot reload triggers
- Configuration reloading
- Workflow reloading

## 📁 Directory Structure

```
lifecycle_management/
├── lifecycle_manager.py          # Main lifecycle management orchestrator
├── config/
│   └── lifecycle_config.json    # Lifecycle management configuration
├── scripts/
│   └── lifecycle_manager.sh     # Management script
├── auto_update/                 # Auto-update components
├── backup_restore/              # Backup and restore components
├── model_versioning/            # Versioning components
├── auto_healing/                # Auto-healing components
├── hot_reload/                  # Hot-reload components
├── logs/                        # Lifecycle logs
├── backups/                     # Backup storage
└── docker-compose.yml           # Docker configuration
```

## 🔧 Configuration

The lifecycle management system is configured via `config/lifecycle_config.json`:

```json
{
  "auto_update": {
    "check_interval": 3600,
    "update_window": {
      "start": "02:00",
      "end": "04:00"
    },
    "auto_approve_updates": false,
    "backup_before_update": true,
    "rollback_on_failure": true
  },
  "backup": {
    "retention_days": 30,
    "backup_components": ["models", "database", "config", "logs"],
    "backup_schedule": {
      "enabled": true,
      "frequency": "daily",
      "time": "01:00"
    }
  },
  "auto_healing": {
    "enable_container_monitoring": true,
    "enable_resource_monitoring": true,
    "health_check_interval": 30,
    "resource_thresholds": {
      "cpu_percent": 85,
      "memory_percent": 85,
      "disk_percent": 90
    }
  }
}
```

## 🚀 Usage

### Starting the Lifecycle Manager

```bash
# Start the lifecycle manager daemon
./lifecycle_management/scripts/lifecycle_manager.sh start-daemon
```

### Manual Operations

```bash
# Perform a manual backup
./lifecycle_management/scripts/lifecycle_manager.sh backup "models,database,config"

# Check for updates
./lifecycle_management/scripts/lifecycle_manager.sh update-check

# Deploy a new model version
./lifecycle_management/scripts/lifecycle_manager.sh deploy-model my_model ./models/my_model

# Rollback a model version
./lifecycle_management/scripts/lifecycle_manager.sh rollback-model my_model v1.0.0

# Restore from backup
./lifecycle_management/scripts/lifecycle_manager.sh restore my_backup_id

# Heal a container
./lifecycle_management/scripts/lifecycle_manager.sh heal-container my_container

# Check system status
./lifecycle_management/scripts/lifecycle_manager.sh status

# Stop the daemon
./lifecycle_management/scripts/lifecycle_manager.sh stop-daemon
```

### Using Docker Compose

```bash
# Start lifecycle services
docker-compose -f lifecycle_management/docker-compose.yml up -d

# View logs
docker-compose -f lifecycle_management/docker-compose.yml logs -f

# Stop services
docker-compose -f lifecycle_management/docker-compose.yml down
```

## 📊 Event Logging

All lifecycle events are logged to:
- `lifecycle_management/logs/lifecycle_events.json` - JSON event log
- `lifecycle_management/logs/lifecycle.log` - Standard log file

The event log includes:
- Auto-update events
- Backup/restore events
- Version deployment/rollback events
- Container healing events
- Health check failures

## 🔁 Integration with Other Layers

The Lifecycle Management Layer integrates with all other layers in the NexaForge architecture:
- **L2 (Model AI Layer)**: Model versioning and updates
- **L6 (Message Queue)**: Health status notifications
- **L7 (API Gateway)**: Service status updates
- **L9 (Database Layer)**: Database backup/restore
- **L10 (Monitoring)**: Health metrics and alerting
- **L11 (Security)**: Secure backup and restore operations

## 🚨 Alerts and Monitoring

The lifecycle manager automatically generates alerts for:
- Failed updates
- Backup failures
- High resource usage
- Unresponsive containers
- Version deployment issues

## 🛡️ Security Considerations

- All backup files are stored with appropriate permissions
- Secure update sources verification
- Encrypted backup options (when configured)
- Access controls for lifecycle operations

## 📈 Performance

The lifecycle manager is designed to:
- Minimize system impact during operations
- Perform updates during low-usage windows
- Maintain system availability during lifecycle operations
- Efficiently manage system resources

## 🔄 Ready for Next Phases

The Lifecycle Management Layer (L13) completes the full 14-layer NexaForge architecture, providing comprehensive lifecycle management for:
- Automatic updates and maintenance
- Backup and disaster recovery
- Model versioning and rollback
- System health and auto-healing
- Hot reload capabilities
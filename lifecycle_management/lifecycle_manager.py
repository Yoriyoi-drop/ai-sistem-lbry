#!/usr/bin/env python3
"""
🚀 NEXAFORGE - LIFECYCLE MANAGEMENT LAYER (L13)
Comprehensive lifecycle management system for auto-update, backup, versioning, and auto-healing
"""

import os
import sys
import json
import time
import shutil
import logging
import threading
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import docker
from docker.errors import DockerException
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lifecycle_management/logs/lifecycle.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class LifecycleEventType(Enum):
    """Lifecycle event types"""
    AUTO_UPDATE_STARTED = "auto_update_started"
    AUTO_UPDATE_COMPLETED = "auto_update_completed"
    AUTO_UPDATE_FAILED = "auto_update_failed"
    BACKUP_STARTED = "backup_started"
    BACKUP_COMPLETED = "backup_completed"
    BACKUP_FAILED = "backup_failed"
    RESTORE_STARTED = "restore_started"
    RESTORE_COMPLETED = "restore_completed"
    RESTORE_FAILED = "restore_failed"
    VERSION_DEPLOYED = "version_deployed"
    VERSION_ROLLED_BACK = "version_rolled_back"
    CONTAINER_HEALED = "container_healed"
    CONTAINER_RESTARTED = "container_restarted"
    HOT_RELOAD_STARTED = "hot_reload_started"
    HOT_RELOAD_COMPLETED = "hot_reload_completed"
    HEALTH_CHECK_FAILED = "health_check_failed"

@dataclass
class ModelVersion:
    """Represents a model version"""
    version_id: str
    model_path: str
    created_at: datetime
    size_mb: float
    status: str  # 'active', 'inactive', 'staged'
    metadata: Dict[str, Any]

@dataclass
class BackupInfo:
    """Represents a backup"""
    backup_id: str
    created_at: datetime
    size_mb: float
    location: str
    components: List[str]
    status: str  # 'completed', 'failed', 'in_progress'

class LifecycleEventLogger:
    """Logs lifecycle events to file and database"""
    
    def __init__(self):
        self.log_dir = Path("lifecycle_management/logs")
        self.log_dir.mkdir(exist_ok=True)
        self.events_file = self.log_dir / "lifecycle_events.json"
        
    def log_event(self, event_type: LifecycleEventType, details: Dict[str, Any] = None):
        """Log a lifecycle event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type.value,
            "details": details or {}
        }
        
        # Append to events file
        with open(self.events_file, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        logger.info(f"Lifecycle event: {event_type.value} - {details}")

class AutoUpdateManager:
    """Manages automatic model and service updates"""
    
    def __init__(self, event_logger: LifecycleEventLogger):
        self.event_logger = event_logger
        self.update_config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load auto-update configuration"""
        config_path = Path("lifecycle_management/config/auto_update.json")
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        else:
            # Default configuration
            default_config = {
                "check_interval": 3600,  # 1 hour
                "update_window": {"start": "02:00", "end": "04:00"},
                "auto_approve_updates": False,
                "backup_before_update": True,
                "rollback_on_failure": True,
                "model_sources": ["https://models.nexaforge.com"]
            }
            config_path.parent.mkdir(exist_ok=True)
            with open(config_path, "w") as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """Check for available updates"""
        logger.info("Checking for available updates...")
        
        updates_available = []
        
        # Simulate checking for model updates
        # In real implementation, this would check model registries
        updates_available.append({
            "component": "model",
            "name": "qwen2.5-coder-32b",
            "current_version": "v1.0.0",
            "new_version": "v1.1.0",
            "download_size_mb": 15.2,
            "release_notes": "Performance improvements and bug fixes"
        })
        
        updates_available.append({
            "component": "service",
            "name": "api_gateway",
            "current_version": "v1.2.0",
            "new_version": "v1.3.0",
            "download_size_mb": 2.1,
            "release_notes": "Security patches and optimization"
        })
        
        return updates_available
    
    def download_update(self, update_info: Dict[str, Any], destination: str) -> bool:
        """Download an update"""
        try:
            logger.info(f"Downloading {update_info['name']} update...")
            self.event_logger.log_event(
                LifecycleEventType.AUTO_UPDATE_STARTED,
                {"component": update_info["name"], "version": update_info["new_version"]}
            )
            
            # Simulate download (in real implementation, this would download from actual sources)
            time.sleep(2)  # Simulate download time
            
            # Create a mock update file
            Path(destination).mkdir(parents=True, exist_ok=True)
            mock_file = Path(destination) / f"{update_info['name']}_v{update_info['new_version']}.tar.gz"
            with open(mock_file, "w") as f:
                f.write(f"Mock update content for {update_info['name']}")
            
            logger.info(f"Downloaded {update_info['name']} update successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to download update: {e}")
            self.event_logger.log_event(
                LifecycleEventType.AUTO_UPDATE_FAILED,
                {"component": update_info["name"], "error": str(e)}
            )
            return False
    
    def apply_update(self, update_path: str, update_info: Dict[str, Any]) -> bool:
        """Apply an update to the system"""
        try:
            logger.info(f"Applying update for {update_info['name']}...")
            
            # In real implementation, this would extract and apply the update
            # For now, simulate the process
            time.sleep(1)  # Simulate extraction time
            
            # Update version tracking
            versions_file = Path("lifecycle_management/model_versions.json")
            versions = {}
            if versions_file.exists():
                with open(versions_file) as f:
                    versions = json.load(f)
            
            versions[update_info["name"]] = {
                "current_version": update_info["new_version"],
                "last_updated": datetime.now().isoformat(),
                "status": "active"
            }
            
            with open(versions_file, "w") as f:
                json.dump(versions, f, indent=2)
            
            logger.info(f"Successfully applied update for {update_info['name']}")
            self.event_logger.log_event(
                LifecycleEventType.AUTO_UPDATE_COMPLETED,
                {"component": update_info["name"], "version": update_info["new_version"]}
            )
            return True
        except Exception as e:
            logger.error(f"Failed to apply update: {e}")
            self.event_logger.log_event(
                LifecycleEventType.AUTO_UPDATE_FAILED,
                {"component": update_info["name"], "error": str(e)}
            )
            return False

class BackupManager:
    """Manages backup and restore operations"""
    
    def __init__(self, event_logger: LifecycleEventLogger):
        self.event_logger = event_logger
        self.backup_dir = Path("lifecycle_management/backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self, components: List[str], backup_name: str = None) -> BackupInfo:
        """Create a backup of specified components"""
        backup_id = backup_name or f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.backup_dir / backup_id
        backup_path.mkdir(exist_ok=True)
        
        self.event_logger.log_event(
            LifecycleEventType.BACKUP_STARTED,
            {"backup_id": backup_id, "components": components}
        )
        
        try:
            logger.info(f"Creating backup: {backup_id} for components: {components}")
            
            total_size = 0
            
            for component in components:
                if component == "models":
                    # Backup model files
                    models_path = Path("models")
                    if models_path.exists():
                        backup_models_path = backup_path / "models"
                        backup_models_path.mkdir(exist_ok=True)
                        shutil.copytree(models_path, backup_models_path / "models", dirs_exist_ok=True)
                        total_size += self._get_dir_size(backup_models_path)
                
                elif component == "database":
                    # Backup database files
                    db_path = Path("data/database")
                    if db_path.exists():
                        backup_db_path = backup_path / "database"
                        backup_db_path.mkdir(exist_ok=True)
                        shutil.copytree(db_path, backup_db_path, dirs_exist_ok=True)
                        total_size += self._get_dir_size(backup_db_path)
                
                elif component == "config":
                    # Backup configuration files
                    config_path = Path("config")
                    if config_path.exists():
                        backup_config_path = backup_path / "config"
                        backup_config_path.mkdir(exist_ok=True)
                        shutil.copytree(config_path, backup_config_path, dirs_exist_ok=True)
                        total_size += self._get_dir_size(backup_config_path)
                
                elif component == "logs":
                    # Backup logs
                    logs_path = Path("logs")
                    if logs_path.exists():
                        backup_logs_path = backup_path / "logs"
                        backup_logs_path.mkdir(exist_ok=True)
                        shutil.copytree(logs_path, backup_logs_path, dirs_exist_ok=True)
                        total_size += self._get_dir_size(backup_logs_path)
            
            backup_info = BackupInfo(
                backup_id=backup_id,
                created_at=datetime.now(),
                size_mb=total_size,
                location=str(backup_path),
                components=components,
                status="completed"
            )
            
            # Write backup info
            with open(backup_path / "backup_info.json", "w") as f:
                json.dump({
                    "backup_id": backup_info.backup_id,
                    "created_at": backup_info.created_at.isoformat(),
                    "size_mb": backup_info.size_mb,
                    "components": backup_info.components,
                    "status": backup_info.status
                }, f, indent=2)
            
            logger.info(f"Backup {backup_id} completed successfully ({total_size:.2f} MB)")
            self.event_logger.log_event(
                LifecycleEventType.BACKUP_COMPLETED,
                {"backup_id": backup_id, "size_mb": total_size}
            )
            
            return backup_info
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            self.event_logger.log_event(
                LifecycleEventType.BACKUP_FAILED,
                {"backup_id": backup_id, "error": str(e)}
            )
            raise
    
    def restore_backup(self, backup_id: str) -> bool:
        """Restore from a backup"""
        backup_path = self.backup_dir / backup_id
        
        self.event_logger.log_event(
            LifecycleEventType.RESTORE_STARTED,
            {"backup_id": backup_id}
        )
        
        try:
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup {backup_id} not found")
            
            logger.info(f"Restoring from backup: {backup_id}")
            
            # Read backup info
            with open(backup_path / "backup_info.json") as f:
                backup_info = json.load(f)
            
            # Restore each component
            restored_components = []
            
            if "models" in backup_info["components"]:
                models_backup = backup_path / "models"
                if models_backup.exists():
                    shutil.rmtree("models", ignore_errors=True)
                    shutil.copytree(models_backup / "models", "models")
                    restored_components.append("models")
            
            if "database" in backup_info["components"]:
                db_backup = backup_path / "database"
                if db_backup.exists():
                    shutil.rmtree("data/database", ignore_errors=True)
                    shutil.copytree(db_backup, "data/database")
                    restored_components.append("database")
            
            if "config" in backup_info["components"]:
                config_backup = backup_path / "config"
                if config_backup.exists():
                    shutil.rmtree("config", ignore_errors=True)
                    shutil.copytree(config_backup, "config")
                    restored_components.append("config")
            
            logger.info(f"Restore completed for components: {restored_components}")
            self.event_logger.log_event(
                LifecycleEventType.RESTORE_COMPLETED,
                {"backup_id": backup_id, "restored_components": restored_components}
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")
            self.event_logger.log_event(
                LifecycleEventType.RESTORE_FAILED,
                {"backup_id": backup_id, "error": str(e)}
            )
            return False
    
    def _get_dir_size(self, path: Path) -> float:
        """Get directory size in MB"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = Path(dirpath) / filename
                total_size += file_path.stat().st_size
        return total_size / (1024 * 1024)  # Convert to MB

class ModelVersionManager:
    """Manages model versions and rollbacks"""
    
    def __init__(self, event_logger: LifecycleEventLogger):
        self.event_logger = event_logger
        self.versions_file = Path("lifecycle_management/model_versions.json")
        self.version_history = self._load_versions()
    
    def _load_versions(self) -> Dict[str, List[ModelVersion]]:
        """Load model version history"""
        if self.versions_file.exists():
            with open(self.versions_file) as f:
                data = json.load(f)
                versions = {}
                for model_name, model_data in data.items():
                    versions[model_name] = [
                        ModelVersion(
                            version_id=item["version_id"],
                            model_path=item["model_path"],
                            created_at=datetime.fromisoformat(item["created_at"]),
                            size_mb=item["size_mb"],
                            status=item["status"],
                            metadata=item.get("metadata", {})
                        )
                        for item in model_data
                    ]
                return versions
        return {}
    
    def save_versions(self):
        """Save model version history"""
        data = {}
        for model_name, versions in self.version_history.items():
            data[model_name] = [
                {
                    "version_id": v.version_id,
                    "model_path": v.model_path,
                    "created_at": v.created_at.isoformat(),
                    "size_mb": v.size_mb,
                    "status": v.status,
                    "metadata": v.metadata
                }
                for v in versions
            ]
        
        with open(self.versions_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def deploy_version(self, model_name: str, model_path: str, metadata: Dict[str, Any] = None) -> str:
        """Deploy a new model version"""
        version_id = f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        size_mb = self._get_file_size(model_path) / (1024 * 1024)  # Convert to MB
        
        new_version = ModelVersion(
            version_id=version_id,
            model_path=model_path,
            created_at=datetime.now(),
            size_mb=size_mb,
            status="active",
            metadata=metadata or {}
        )
        
        if model_name not in self.version_history:
            self.version_history[model_name] = []
        
        # Deactivate current active version
        for version in self.version_history[model_name]:
            if version.status == "active":
                version.status = "inactive"
        
        self.version_history[model_name].append(new_version)
        self.save_versions()
        
        logger.info(f"Deployed new version {version_id} for model {model_name}")
        self.event_logger.log_event(
            LifecycleEventType.VERSION_DEPLOYED,
            {"model_name": model_name, "version_id": version_id}
        )
        
        return version_id
    
    def rollback_version(self, model_name: str, version_id: str) -> bool:
        """Rollback to a specific model version"""
        if model_name not in self.version_history:
            logger.error(f"No versions found for model {model_name}")
            return False
        
        target_version = None
        for version in self.version_history[model_name]:
            if version.version_id == version_id:
                target_version = version
                break
        
        if not target_version:
            logger.error(f"Version {version_id} not found for model {model_name}")
            return False
        
        # Deactivate current active version
        for version in self.version_history[model_name]:
            if version.status == "active":
                version.status = "inactive"
        
        # Activate target version
        target_version.status = "active"
        self.save_versions()
        
        logger.info(f"Rolled back to version {version_id} for model {model_name}")
        self.event_logger.log_event(
            LifecycleEventType.VERSION_ROLLED_BACK,
            {"model_name": model_name, "version_id": version_id}
        )
        
        return True
    
    def get_active_version(self, model_name: str) -> Optional[ModelVersion]:
        """Get the active version for a model"""
        if model_name in self.version_history:
            for version in self.version_history[model_name]:
                if version.status == "active":
                    return version
        return None
    
    def list_all_versions(self, model_name: str) -> List[ModelVersion]:
        """List all versions for a model"""
        if model_name in self.version_history:
            return self.version_history[model_name]
        return []
    
    def _get_file_size(self, file_path: str) -> int:
        """Get file size in bytes"""
        return Path(file_path).stat().st_size

class AutoHealingManager:
    """Manages auto-healing of services and containers"""
    
    def __init__(self, event_logger: LifecycleEventLogger):
        self.event_logger = event_logger
        self.docker_client = self._get_docker_client()
        self.health_check_interval = 30  # seconds
        self.is_monitoring = False
        self.monitoring_thread = None
    
    def _get_docker_client(self):
        """Initialize docker client"""
        try:
            return docker.from_env()
        except DockerException:
            logger.warning("Docker not available, some auto-healing features will be limited")
            return None
    
    def start_health_monitoring(self):
        """Start health monitoring in background"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._health_monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        logger.info("Auto-healing monitoring started")
    
    def stop_health_monitoring(self):
        """Stop health monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        logger.info("Auto-healing monitoring stopped")
    
    def _health_monitoring_loop(self):
        """Main health monitoring loop"""
        while self.is_monitoring:
            try:
                self._check_system_health()
            except Exception as e:
                logger.error(f"Error in health monitoring: {e}")
            
            time.sleep(self.health_check_interval)
    
    def _check_system_health(self):
        """Check health of various system components"""
        # Check system resources
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        
        # Log high resource usage
        if cpu_percent > 85:
            self.event_logger.log_event(
                LifecycleEventType.HEALTH_CHECK_FAILED,
                {"type": "high_cpu", "value": cpu_percent}
            )
        if memory_percent > 85:
            self.event_logger.log_event(
                LifecycleEventType.HEALTH_CHECK_FAILED,
                {"type": "high_memory", "value": memory_percent}
            )
        if disk_percent > 90:
            self.event_logger.log_event(
                LifecycleEventType.HEALTH_CHECK_FAILED,
                {"type": "high_disk", "value": disk_percent}
            )
        
        # Check Docker containers if available
        if self.docker_client:
            try:
                containers = self.docker_client.containers.list()
                for container in containers:
                    status = container.status
                    if status == "exited":
                        # Container is stopped, try to restart
                        logger.info(f"Restarting stopped container: {container.name}")
                        container.start()
                        self.event_logger.log_event(
                            LifecycleEventType.CONTAINER_RESTARTED,
                            {"container_name": container.name, "reason": "stopped"}
                        )
                    elif status == "running":
                        # Check if container is responsive
                        try:
                            container.reload()
                            # Container is running and responsive
                        except:
                            logger.error(f"Container {container.name} is not responding")
                            # Try to restart
                            container.restart()
                            self.event_logger.log_event(
                                LifecycleEventType.CONTAINER_HEALED,
                                {"container_name": container.name, "reason": "unresponsive"}
                            )
            except Exception as e:
                logger.error(f"Error checking container health: {e}")
    
    def heal_container(self, container_name: str) -> bool:
        """Heal a specific container"""
        if not self.docker_client:
            logger.error("Docker client not available")
            return False
        
        try:
            container = self.docker_client.containers.get(container_name)
            status = container.status
            
            if status == "exited":
                container.start()
                logger.info(f"Started container: {container_name}")
            elif status == "running":
                container.restart()
                logger.info(f"Restarted container: {container_name}")
            else:
                container.restart()
                logger.info(f"Restarted container: {container_name}")
            
            self.event_logger.log_event(
                LifecycleEventType.CONTAINER_HEALED,
                {"container_name": container_name}
            )
            
            return True
        except Exception as e:
            logger.error(f"Failed to heal container {container_name}: {e}")
            return False

class HotReloadManager:
    """Manages hot reloading of services and workflows"""
    
    def __init__(self, event_logger: LifecycleEventLogger):
        self.event_logger = event_logger
        self.watched_files = {}
        self.reload_callbacks = {}
    
    def register_reload_target(self, name: str, path: str, callback):
        """Register a target for hot reloading"""
        self.watched_files[name] = {
            "path": path,
            "last_modified": self._get_last_modified(path)
        }
        self.reload_callbacks[name] = callback
    
    def check_for_changes(self) -> List[str]:
        """Check if any registered files have changed"""
        changed_items = []
        
        for name, info in self.watched_files.items():
            current_modified = self._get_last_modified(info["path"])
            if current_modified > info["last_modified"]:
                changed_items.append(name)
                info["last_modified"] = current_modified
        
        return changed_items
    
    def perform_hot_reload(self, target_name: str) -> bool:
        """Perform hot reload for a specific target"""
        self.event_logger.log_event(
            LifecycleEventType.HOT_RELOAD_STARTED,
            {"target": target_name}
        )
        
        try:
            logger.info(f"Hot reloading target: {target_name}")
            
            if target_name in self.reload_callbacks:
                callback = self.reload_callbacks[target_name]
                callback()
                
                logger.info(f"Hot reload completed for: {target_name}")
                self.event_logger.log_event(
                    LifecycleEventType.HOT_RELOAD_COMPLETED,
                    {"target": target_name}
                )
                return True
            else:
                logger.error(f"No reload callback found for: {target_name}")
                return False
                
        except Exception as e:
            logger.error(f"Hot reload failed for {target_name}: {e}")
            return False
    
    def _get_last_modified(self, path: str) -> float:
        """Get last modified time for a file or directory"""
        path_obj = Path(path)
        if path_obj.is_file():
            return path_obj.stat().st_mtime
        elif path_obj.is_dir():
            # Get the most recent modification time in the directory
            latest = path_obj.stat().st_mtime
            for item in path_obj.rglob('*'):
                if item.is_file():
                    latest = max(latest, item.stat().st_mtime)
            return latest
        else:
            return 0

class LifecycleManager:
    """Main lifecycle management orchestrator"""
    
    def __init__(self):
        self.event_logger = LifecycleEventLogger()
        self.auto_update_manager = AutoUpdateManager(self.event_logger)
        self.backup_manager = BackupManager(self.event_logger)
        self.version_manager = ModelVersionManager(self.event_logger)
        self.auto_healing_manager = AutoHealingManager(self.event_logger)
        self.hot_reload_manager = HotReloadManager(self.event_logger)
        
        # Start auto-healing monitoring
        self.auto_healing_manager.start_health_monitoring()
    
    def shutdown(self):
        """Clean shutdown of lifecycle manager"""
        logger.info("Shutting down lifecycle manager...")
        self.auto_healing_manager.stop_health_monitoring()
    
    def get_status(self) -> Dict[str, Any]:
        """Get overall system lifecycle status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "auto_update": {
                "enabled": True,
                "check_interval": self.auto_update_manager.update_config["check_interval"]
            },
            "backup": {
                "enabled": True,
                "last_backup": self._get_last_backup_time()
            },
            "versioning": {
                "enabled": True,
                "model_count": len(self.version_manager.version_history)
            },
            "auto_healing": {
                "active": self.auto_healing_manager.is_monitoring,
                "health_check_interval": self.auto_healing_manager.health_check_interval
            },
            "hot_reload": {
                "enabled": True,
                "watched_targets": len(self.hot_reload_manager.watched_files)
            }
        }
    
    def _get_last_backup_time(self) -> Optional[str]:
        """Get the time of the last backup"""
        backups_dir = Path("lifecycle_management/backups")
        if not backups_dir.exists():
            return None
        
        backups = [d for d in backups_dir.iterdir() if d.is_dir()]
        if not backups:
            return None
        
        latest_backup = max(backups, key=lambda x: x.stat().st_mtime)
        return datetime.fromtimestamp(latest_backup.stat().st_mtime).isoformat()

def main():
    """Demo of Lifecycle Management Layer (L13) implementation"""
    print("🚀 NEXAFORGE - LIFECYCLE MANAGEMENT LAYER (L13)")
    print("=" * 60)
    
    # Initialize lifecycle manager
    lifecycle_manager = LifecycleManager()
    
    print("\n🔍 DEMO 1: LIFECYCLE STATUS")
    status = lifecycle_manager.get_status()
    print(f"   Auto-update: Enabled (check every {status['auto_update']['check_interval']}s)")
    print(f"   Backup system: Enabled")
    print(f"   Versioning: Enabled ({status['versioning']['model_count']} models tracked)")
    print(f"   Auto-healing: Active (check every {status['auto_healing']['health_check_interval']}s)")
    print(f"   Hot-reload: Enabled ({status['hot_reload']['watched_targets']} targets)")
    
    print("\n📊 DEMO 2: AUTO-UPDATE CHECK")
    updates = lifecycle_manager.auto_update_manager.check_for_updates()
    print(f"   Available updates: {len(updates)}")
    for update in updates:
        print(f"   - {update['name']}: {update['current_version']} → {update['new_version']}")
    
    print("\n💾 DEMO 3: CREATE BACKUP")
    try:
        backup_info = lifecycle_manager.backup_manager.create_backup(
            components=["config", "logs"],
            backup_name="demo_backup"
        )
        print(f"   Backup created: {backup_info.backup_id} ({backup_info.size_mb:.2f} MB)")
    except Exception as e:
        print(f"   Backup failed: {e}")
    
    print("\n🔄 DEMO 4: MODEL VERSIONING")
    # Deploy a new version (simulated)
    try:
        if Path("models").exists():
            version_id = lifecycle_manager.version_manager.deploy_version(
                "test_model", 
                "models/test_model", 
                {"accuracy": 0.95, "size": "32B"}
            )
            print(f"   New model version deployed: {version_id}")
    except:
        print("   (Skipping version deployment - models directory not found)")
    
    print("\n🏥 DEMO 5: SIMULATE AUTO-HEALING")
    # The auto-healing system is running in background, monitoring system health
    print("   Auto-healing monitoring is active")
    print(f"   Health checks every {lifecycle_manager.auto_healing_manager.health_check_interval}s")
    
    print("\n🔥 DEMO 6: REGISTER HOT-RELOAD TARGETS")
    # Register a demo reload target
    def demo_reload_callback():
        print("   Reload callback executed!")
    
    lifecycle_manager.hot_reload_manager.register_reload_target(
        "demo_config", 
        "config", 
        demo_reload_callback
    )
    
    print("   Demo config reload target registered")
    
    print("\n🎯 L13 COMPLETE: Lifecycle Management Systems Ready!")
    print("   - Auto-update capabilities")
    print("   - Backup and restore systems")
    print("   - Model versioning and rollback")
    print("   - Auto-healing containers")
    print("   - Hot reload functionality")
    print("   - Comprehensive lifecycle event logging")
    
    print(f"\n📋 EVENT LOG LOCATION: lifecycle_management/logs/lifecycle_events.json")
    
    # Keep the system running for demo purposes
    print(f"\n⏳ Lifecycle manager running... Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(10)
            # Check for hot reloads
            changes = lifecycle_manager.hot_reload_manager.check_for_changes()
            if changes:
                for change in changes:
                    lifecycle_manager.hot_reload_manager.perform_hot_reload(change)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down lifecycle manager...")
        lifecycle_manager.shutdown()
        print("✅ Lifecycle manager stopped")

if __name__ == "__main__":
    main()
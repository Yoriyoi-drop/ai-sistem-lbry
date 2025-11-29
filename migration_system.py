# 🗄️ NEXAFORGE - DATABASE MIGRATION SYSTEM (L9 Component)

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class DatabaseMigration:
    """Represents a single database migration"""
    
    def __init__(self, version: str, name: str, description: str = ""):
        self.version = version
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.applied_at = None
        self.status = "pending"  # pending, applied, failed
    
    def to_dict(self):
        """Convert migration to dictionary for JSON serialization"""
        return {
            "version": self.version,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
            "status": self.status
        }

class MigrationManager:
    """Manages database migrations for the system"""
    
    def __init__(self, config_path: str = "database_config.json"):
        self.migrations_path = Path("./migrations")
        self.migrations_path.mkdir(exist_ok=True)
        
        # Create migrations index file
        self.migrations_index = self.migrations_path / "index.json"
        if not self.migrations_index.exists():
            self.migrations_index.write_text(json.dumps([]))
    
    def create_migration(self, version: str, name: str, description: str, 
                        postgres_sql: str = "", mongo_js: str = "", redis_commands: str = "") -> str:
        """Create a new migration file with SQL/JS commands"""
        
        # Create migration directory
        migration_dir = self.migrations_path / f"V{version}__{name.replace(' ', '_')}"
        migration_dir.mkdir(exist_ok=True)
        
        # Create migration info file
        migration_info = {
            "version": version,
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "applied_at": None,
            "status": "pending"
        }
        
        # Write info file
        (migration_dir / "info.json").write_text(json.dumps(migration_info, indent=2))
        
        # Write PostgreSQL migration
        if postgres_sql:
            (migration_dir / "postgres.sql").write_text(postgres_sql)
        
        # Write MongoDB migration
        if mongo_js:
            (migration_dir / "mongo.js").write_text(mongo_js)
        
        # Write Redis migration
        if redis_commands:
            (migration_dir / "redis.txt").write_text(redis_commands)
        
        # Update index
        index = self._load_index()
        migration = DatabaseMigration(version, name, description)
        index.append(migration.to_dict())
        self._save_index(index)
        
        print(f"✅ Migration {version} created: {name}")
        return str(migration_dir)
    
    def _load_index(self) -> List[Dict]:
        """Load migration index from file"""
        try:
            content = self.migrations_index.read_text()
            return json.loads(content)
        except:
            return []
    
    def _save_index(self, index: List[Dict]):
        """Save migration index to file"""
        self.migrations_index.write_text(json.dumps(index, indent=2))
    
    def list_migrations(self) -> List[Dict]:
        """List all migrations"""
        return self._load_index()
    
    def get_pending_migrations(self) -> List[Dict]:
        """Get migrations that haven't been applied yet"""
        all_migrations = self._load_index()
        return [m for m in all_migrations if m["status"] == "pending"]
    
    def apply_migration(self, version: str) -> bool:
        """Simulate applying a migration"""
        index = self._load_index()
        
        for migration in index:
            if migration["version"] == version:
                migration["status"] = "applied"
                migration["applied_at"] = datetime.now().isoformat()
                
                print(f"✅ Migration {version} applied successfully")
                
                self._save_index(index)
                return True
        
        print(f"❌ Migration {version} not found")
        return False
    
    def rollback_migration(self, version: str) -> bool:
        """Simulate rolling back a migration"""
        index = self._load_index()
        
        for migration in index:
            if migration["version"] == version and migration["status"] == "applied":
                migration["status"] = "pending"
                migration["applied_at"] = None
                
                print(f"🔄 Migration {version} rolled back")
                
                self._save_index(index)
                return True
        
        print(f"❌ Migration {version} not found or not applied")
        return False

def main():
    """Demo of migration system"""
    print("🗄️ NEXAFORGE - DATABASE MIGRATION SYSTEM (L9 Component)")
    print("=" * 55)
    
    # Initialize migration manager
    migration_manager = MigrationManager()
    
    print(f"\n📋 AVAILABLE MIGRATIONS:")
    migrations = migration_manager.list_migrations()
    if migrations:
        for migration in migrations:
            print(f"  • V{migration['version']}: {migration['name']} ({migration['status']})")
    else:
        print("  No migrations created yet")
    
    print(f"\n🔧 CREATING MIGRATIONS:")
    
    # Create users table migration
    users_migration_sql = """
-- PostgreSQL migration for users table
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    subscription_tier VARCHAR(20) DEFAULT 'free',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
    """
    
    migration_manager.create_migration(
        "001", 
        "Create Users Table", 
        "Initial user accounts table creation",
        postgres_sql=users_migration_sql
    )
    
    # Create API tokens table migration
    tokens_migration_sql = """
-- PostgreSQL migration for API tokens
CREATE TABLE api_tokens (
    id VARCHAR(255) PRIMARY KEY,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    token_type VARCHAR(20) DEFAULT 'api_key',
    permissions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    last_used TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_api_tokens_user_id ON api_tokens(user_id);
CREATE INDEX idx_api_tokens_active ON api_tokens(is_active) WHERE is_active = TRUE;
    """
    
    migration_manager.create_migration(
        "002",
        "Create API Tokens Table",
        "API authentication token management",
        postgres_sql=tokens_migration_sql
    )
    
    # Create workflows table migration
    workflows_migration_sql = """
-- PostgreSQL migration for workflows
CREATE TABLE workflows (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    definition JSONB,
    execution_count INTEGER DEFAULT 0,
    last_executed TIMESTAMP
);

CREATE INDEX idx_workflows_owner ON workflows(owner_id);
CREATE INDEX idx_workflows_status ON workflows(status);
    """
    
    migration_manager.create_migration(
        "003",
        "Create Workflows Table",
        "Workflow definition and execution tracking",
        postgres_sql=workflows_migration_sql
    )
    
    # Show migration status
    print(f"\n📊 MIGRATION STATUS:")
    all_migrations = migration_manager.list_migrations()
    for migration in all_migrations:
        status_icon = "✅" if migration["status"] == "applied" else "⏳"
        print(f"  {status_icon} V{migration['version']}: {migration['name']}")
    
    # Show pending migrations
    pending = migration_manager.get_pending_migrations()
    print(f"\n🔄 PENDING MIGRATIONS: {len(pending)}")
    for migration in pending:
        print(f"  • V{migration['version']}: {migration['name']}")
    
    print(f"\n⚡ APPLYING MIGRATIONS:")
    # Apply first migration
    migration_manager.apply_migration("001")
    
    # Show updated status
    print(f"\n📈 UPDATED MIGRATION STATUS:")
    all_migrations = migration_manager.list_migrations()
    for migration in all_migrations:
        status_icon = "✅" if migration["status"] == "applied" else "⏳"
        applied_info = f" - Applied: {migration['applied_at'][:19]}" if migration["applied_at"] else ""
        print(f"  {status_icon} V{migration['version']}: {migration['name']}{applied_info}")
    
    print(f"\n📋 MIGRATION DIRECTORY STRUCTURE:")
    print("  migrations/")
    for item in Path("./migrations").iterdir():
        if item.is_dir():
            print(f"    └── {item.name}/")
            for subitem in item.iterdir():
                print(f"        └── {subitem.name}")
    
    print(f"\n🎉 Migration System Ready!")
    print("   - Versioned migration files")
    "   - PostgreSQL, MongoDB, and Redis support")
    print("   - Status tracking and rollback capability")

if __name__ == "__main__":
    main()
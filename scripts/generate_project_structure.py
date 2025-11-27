#!/usr/bin/env python3
"""
Automatic Project Structure Generator
Generates all placeholder files for empty folders in the project.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Base directory
BASE_DIR = Path(__file__).parent.parent.absolute()

# File templates
TEMPLATES = {
    "python_init": '''"""
{docstring}
"""

__version__ = "0.1.0"
''',
    
    "python_module": '''"""
{docstring}

Created: {date}
"""

# TODO: Implement {module_name}


def main():
    """Main function for {module_name}"""
    pass


if __name__ == "__main__":
    main()
''',
    
    "typescript_index": '''/**
 * {docstring}
 * 
 * @created {date}
 */

// TODO: Implement {module_name}

export {{}};
''',
    
    "typescript_module": '''/**
 * {docstring}
 * 
 * @created {date}
 */

// TODO: Implement {module_name}

export const placeholder = true;
''',
    
    "react_component": '''import React from 'react';

/**
 * {docstring}
 * 
 * @created {date}
 */
export const {component_name} = () => {{
  return (
    <div className="{class_name}">
      <h2>{component_name}</h2>
      <p>TODO: Implement {component_name} component</p>
    </div>
  );
}};

export default {component_name};
''',
    
    "shell_script": '''#!/bin/bash
# {docstring}
# Created: {date}

set -e

echo "TODO: Implement {script_name}"
''',
    
    "sql_file": '''-- {docstring}
-- Created: {date}

-- TODO: Implement SQL schema/queries
''',
    
    "markdown": '''# {title}

> {docstring}

**Created:** {date}

## Overview

TODO: Add documentation

## Usage

TODO: Add usage instructions

## Examples

TODO: Add examples
''',
    
    "gitkeep": '''# This file keeps the directory in version control
''',
    
    "go_file": '''package {package_name}

// {docstring}
// Created: {date}

// TODO: Implement {module_name}
''',
    
    "rust_file": '''//! {docstring}
//! Created: {date}

// TODO: Implement {module_name}
''',
    
    "solidity": '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * {docstring}
 * Created: {date}
 */
contract {contract_name} {{
    // TODO: Implement contract
}}
''',

    "test_python": '''"""
{docstring}

Created: {date}
"""

import pytest


class Test{class_name}:
    """Test suite for {module_name}"""
    
    def test_placeholder(self):
        """Placeholder test"""
        # TODO: Implement tests
        assert True
''',

    "test_typescript": '''/**
 * {docstring}
 * 
 * @created {date}
 */

import {{ describe, it, expect }} from 'vitest';

describe('{module_name}', () => {{
  it('should pass placeholder test', () => {{
    // TODO: Implement tests
    expect(true).toBe(true);
  }});
}});
''',
}

# File structure definition
# Format: "path": [("filename", "template_type", "description")]
FILE_STRUCTURE: Dict[str, List[Tuple[str, str, str]]] = {
    # 1. DATABASE & MIGRATIONS
    "src/database": [
        ("__init__.py", "python_init", "Database package initialization"),
        ("connection.py", "python_module", "Database connection manager"),
        ("session.py", "python_module", "Database session factory"),
        ("base.py", "python_module", "Base model for SQLAlchemy"),
        ("models.py", "python_module", "Database models"),
    ],
    
    "apps/api/src/database/migrations/versions": [
        ("001_initial_schema.py", "python_module", "Initial database schema migration"),
        ("002_add_users_table.py", "python_module", "User table migration"),
        ("003_add_agents_table.py", "python_module", "Agent table migration"),
        ("004_add_scans_table.py", "python_module", "Security scan table migration"),
        ("005_add_subscriptions_table.py", "python_module", "Subscription table migration"),
    ],
    
    "app/db": [
        ("schema.sql", "sql_file", "Database schema SQL"),
        ("seed.sql", "sql_file", "Seed data SQL"),
        ("backup.sql", "sql_file", "Backup template"),
    ],
    
    # 2. TESTING - API
    "apps/api/tests/unit": [
        ("__init__.py", "python_init", "Unit tests package"),
        ("test_auth.py", "test_python", "Authentication tests"),
        ("test_models.py", "test_python", "Database model tests"),
        ("test_services.py", "test_python", "Service layer tests"),
        ("test_utils.py", "test_python", "Utility function tests"),
        ("test_middleware.py", "test_python", "Middleware tests"),
    ],
    
    "apps/api/tests/integration": [
        ("__init__.py", "python_init", "Integration tests package"),
        ("test_api_endpoints.py", "test_python", "API endpoint tests"),
        ("test_database.py", "test_python", "Database integration tests"),
        ("test_external_services.py", "test_python", "External service integration"),
        ("test_workflow.py", "test_python", "Workflow integration tests"),
    ],
    
    "apps/api/tests/e2e": [
        ("__init__.py", "python_init", "End-to-end tests package"),
        ("test_user_flow.py", "test_python", "Complete user journey test"),
        ("test_scan_workflow.py", "test_python", "Scan workflow end-to-end"),
        ("test_agent_execution.py", "test_python", "Agent execution flow"),
    ],
    
    # 3. TESTING - DASHBOARD
    "apps/dashboard/tests/unit": [
        ("setup.ts", "typescript_module", "Test setup configuration"),
        ("components.test.tsx", "test_typescript", "Component unit tests"),
        ("stores.test.ts", "test_typescript", "State management tests"),
        ("utils.test.ts", "test_typescript", "Utility function tests"),
        ("hooks.test.ts", "test_typescript", "Custom hooks tests"),
    ],
    
    "apps/dashboard/tests/integration": [
        ("api.test.ts", "test_typescript", "API integration tests"),
        ("auth.test.ts", "test_typescript", "Authentication flow tests"),
        ("navigation.test.ts", "test_typescript", "Navigation tests"),
    ],
    
    "apps/dashboard/tests/e2e": [
        ("login.spec.ts", "test_typescript", "Login flow test"),
        ("dashboard.spec.ts", "test_typescript", "Dashboard functionality test"),
        ("agents.spec.ts", "test_typescript", "Agent management test"),
        ("security.spec.ts", "test_typescript", "Security features test"),
    ],
    
    # 4. API COMPONENTS
    "apps/api/src/tasks": [
        ("__init__.py", "python_init", "Background tasks package"),
        ("celery_app.py", "python_module", "Celery application configuration"),
        ("security_tasks.py", "python_module", "Security scanning background tasks"),
        ("cleanup_tasks.py", "python_module", "Database cleanup tasks"),
        ("notification_tasks.py", "python_module", "Notification sending tasks"),
        ("report_tasks.py", "python_module", "Report generation tasks"),
    ],
    
    "apps/api/src/cache": [
        ("__init__.py", "python_init", "Cache package"),
        ("redis_client.py", "python_module", "Redis client configuration"),
        ("cache_keys.py", "python_module", "Cache key definitions"),
        ("decorators.py", "python_module", "Caching decorators"),
    ],
    
    # 5. DASHBOARD PAGES
    "apps/dashboard/src/pages/auth": [
        ("Login.tsx", "react_component", "Login page component"),
        ("Register.tsx", "react_component", "Registration page component"),
        ("ForgotPassword.tsx", "react_component", "Password reset page"),
        ("index.ts", "typescript_index", "Export all auth pages"),
    ],
    
    "apps/dashboard/src/pages/dashboard": [
        ("Dashboard.tsx", "react_component", "Main dashboard page"),
        ("Overview.tsx", "react_component", "Overview section"),
        ("index.ts", "typescript_index", "Export dashboard pages"),
    ],
    
    "apps/dashboard/src/pages/agents": [
        ("AgentsPage.tsx", "react_component", "Agents listing page"),
        ("AgentDetail.tsx", "react_component", "Single agent detail page"),
        ("CreateAgent.tsx", "react_component", "Create agent form"),
        ("index.ts", "typescript_index", "Export agent pages"),
    ],
    
    "apps/dashboard/src/pages/security": [
        ("SecurityPage.tsx", "react_component", "Security overview page"),
        ("ScanResults.tsx", "react_component", "Scan results page"),
        ("ThreatMap.tsx", "react_component", "Threat visualization page"),
        ("index.ts", "typescript_index", "Export security pages"),
    ],
    
    "apps/dashboard/src/pages/settings": [
        ("SettingsPage.tsx", "react_component", "Main settings page"),
        ("Profile.tsx", "react_component", "User profile settings"),
        ("Subscription.tsx", "react_component", "Subscription management"),
        ("Preferences.tsx", "react_component", "User preferences"),
        ("index.ts", "typescript_index", "Export settings pages"),
    ],
    
    # 6. DASHBOARD COMPONENTS
    "apps/dashboard/src/components/ui": [
        ("button.tsx", "react_component", "Button component"),
        ("card.tsx", "react_component", "Card component"),
        ("dialog.tsx", "react_component", "Dialog/Modal component"),
        ("input.tsx", "react_component", "Input component"),
        ("select.tsx", "react_component", "Select dropdown component"),
        ("table.tsx", "react_component", "Table component"),
        ("toast.tsx", "react_component", "Toast notification component"),
        ("index.ts", "typescript_index", "Export all UI components"),
    ],
    
    "apps/dashboard/src/components/layout": [
        ("Header.tsx", "react_component", "Header component"),
        ("Sidebar.tsx", "react_component", "Sidebar navigation"),
        ("Footer.tsx", "react_component", "Footer component"),
        ("Layout.tsx", "react_component", "Main layout wrapper"),
        ("index.ts", "typescript_index", "Export layout components"),
    ],
    
    "apps/dashboard/src/components/common": [
        ("Loading.tsx", "react_component", "Loading spinner component"),
        ("ErrorBoundary.tsx", "react_component", "Error boundary component"),
        ("NotFound.tsx", "react_component", "404 page component"),
        ("ProtectedRoute.tsx", "react_component", "Protected route wrapper"),
        ("index.ts", "typescript_index", "Export common components"),
    ],
    
    "apps/dashboard/src/components/agents": [
        ("AgentCard.tsx", "react_component", "Agent card display"),
        ("AgentList.tsx", "react_component", "Agent list component"),
        ("AgentStatus.tsx", "react_component", "Agent status indicator"),
        ("AgentForm.tsx", "react_component", "Agent creation/edit form"),
        ("index.ts", "typescript_index", "Export agent components"),
    ],
    
    "apps/dashboard/src/components/security": [
        ("ThreatMap.tsx", "react_component", "Threat visualization"),
        ("ScanResults.tsx", "react_component", "Scan results display"),
        ("SecurityDashboard.tsx", "react_component", "Security overview"),
        ("VulnerabilityList.tsx", "react_component", "Vulnerability list"),
        ("index.ts", "typescript_index", "Export security components"),
    ],
    
    "apps/dashboard/src/components/labyrinth": [
        ("LabyrinthVisualization.tsx", "react_component", "Labyrinth maze display"),
        ("DefenseMetrics.tsx", "react_component", "Defense metrics display"),
        ("RouteMap.tsx", "react_component", "Route mapping visualization"),
        ("index.ts", "typescript_index", "Export labyrinth components"),
    ],
    
    # 7. DASHBOARD SERVICES
    "apps/dashboard/src/services": [
        ("api.ts", "typescript_module", "Axios API client configuration"),
        ("authService.ts", "typescript_module", "Authentication API calls"),
        ("agentService.ts", "typescript_module", "Agent management API calls"),
        ("securityService.ts", "typescript_module", "Security API calls"),
        ("websocketService.ts", "typescript_module", "WebSocket connection handler"),
        ("index.ts", "typescript_index", "Export all services"),
    ],
    
    "apps/dashboard/src/hooks": [
        ("useAuth.ts", "typescript_module", "Authentication hook"),
        ("useAgents.ts", "typescript_module", "Agents management hook"),
        ("useWebSocket.ts", "typescript_module", "WebSocket connection hook"),
        ("useLocalStorage.ts", "typescript_module", "Local storage hook"),
        ("useDebounce.ts", "typescript_module", "Debounce hook"),
        ("index.ts", "typescript_index", "Export all hooks"),
    ],
    
    "apps/dashboard/src/utils": [
        ("format.ts", "typescript_module", "Data formatting utilities"),
        ("validation.ts", "typescript_module", "Form validation utilities"),
        ("constants.ts", "typescript_module", "Application constants"),
        ("helpers.ts", "typescript_module", "Helper functions"),
        ("index.ts", "typescript_index", "Export all utilities"),
    ],
    
    "apps/dashboard/src/types": [
        ("index.ts", "typescript_index", "Main types export"),
        ("agent.types.ts", "typescript_module", "Agent-related types"),
        ("security.types.ts", "typescript_module", "Security-related types"),
        ("user.types.ts", "typescript_module", "User-related types"),
        ("api.types.ts", "typescript_module", "API response types"),
    ],
    
    "apps/dashboard/src/store": [
        ("index.ts", "typescript_index", "Store configuration"),
        ("authStore.ts", "typescript_module", "Authentication state"),
        ("agentStore.ts", "typescript_module", "Agent management state"),
        ("securityStore.ts", "typescript_module", "Security state"),
        ("uiStore.ts", "typescript_module", "UI state (theme, sidebar, etc)"),
    ],
    
    "apps/dashboard/src/styles": [
        ("globals.css", "markdown", "Global styles"),
        ("themes.ts", "typescript_module", "Theme configuration"),
        ("variables.css", "markdown", "CSS variables"),
    ],
    
    "apps/dashboard/src/config": [
        ("routes.ts", "typescript_module", "Route definitions"),
        ("constants.ts", "typescript_module", "Configuration constants"),
        ("env.ts", "typescript_module", "Environment variables"),
    ],
    
    "apps/dashboard/src/assets/images": [
        (".gitkeep", "gitkeep", "Keep folder in git"),
    ],
    
    "apps/dashboard/src/assets/icons": [
        (".gitkeep", "gitkeep", "Keep folder in git"),
    ],
    
    "apps/dashboard/src/assets/fonts": [
        (".gitkeep", "gitkeep", "Keep folder in git"),
    ],
    
    "apps/dashboard/public": [
        ("robots.txt", "markdown", "SEO robots file"),
        (".gitkeep", "gitkeep", "Keep folder in git"),
    ],
    
    # 8. WEB3
    "apps/web3/contracts": [
        ("SecurityRegistry.sol", "solidity", "Security registry contract"),
        ("ThreatToken.sol", "solidity", "Threat token contract"),
        ("AuditTrail.sol", "solidity", "Audit trail contract"),
    ],
    
    "apps/web3/scripts": [
        ("deploy.js", "typescript_module", "Deployment script"),
        ("verify.js", "typescript_module", "Contract verification script"),
        ("interact.js", "typescript_module", "Contract interaction script"),
    ],
    
    "apps/web3/test": [
        ("SecurityRegistry.test.js", "test_typescript", "Contract tests"),
        ("ThreatToken.test.js", "test_typescript", "Token tests"),
        ("AuditTrail.test.js", "test_typescript", "Audit tests"),
    ],
    
    # 9. DOCUMENTATION
    "docs/architecture": [
        ("overview.md", "markdown", "System architecture overview"),
        ("component-diagram.md", "markdown", "Component diagrams"),
        ("data-flow.md", "markdown", "Data flow documentation"),
        ("security-design.md", "markdown", "Security architecture"),
        ("labyrinth-concept.md", "markdown", "Labyrinth explanation"),
    ],
    
    "docs/api": [
        ("openapi.yaml", "markdown", "OpenAPI specification"),
        ("authentication.md", "markdown", "Auth documentation"),
        ("endpoints.md", "markdown", "Endpoint documentation"),
        ("websocket.md", "markdown", "WebSocket API docs"),
    ],
    
    "docs/deployment": [
        ("local-development.md", "markdown", "Local setup guide"),
        ("docker-deployment.md", "markdown", "Docker deployment"),
        ("kubernetes-deployment.md", "markdown", "K8s deployment"),
        ("production-checklist.md", "markdown", "Production checklist"),
    ],
    
    "docs/guides": [
        ("getting-started.md", "markdown", "Getting started guide"),
        ("contributing.md", "markdown", "Contribution guidelines"),
        ("code-style.md", "markdown", "Code style guide"),
        ("troubleshooting.md", "markdown", "Troubleshooting guide"),
    ],
    
    "docs/tutorials": [
        ("creating-agents.md", "markdown", "Agent creation tutorial"),
        ("custom-security-rules.md", "markdown", "Custom rules guide"),
        ("extending-labyrinth.md", "markdown", "Labyrinth extension"),
    ],
    
    "docs/diagrams": [
        (".gitkeep", "gitkeep", "Keep folder"),
    ],
    
    # 10. SHARED
    "shared/proto": [
        ("agent.proto", "markdown", "Agent service proto"),
        ("security.proto", "markdown", "Security service proto"),
        ("labyrinth.proto", "markdown", "Labyrinth service proto"),
        ("workflow.proto", "markdown", "Workflow proto"),
    ],
    
    "shared/types/python": [
        ("__init__.py", "python_init", "Python types package"),
        ("common.py", "python_module", "Common Python types"),
        ("models.py", "python_module", "Shared data models"),
    ],
    
    "shared/types/typescript": [
        ("index.ts", "typescript_index", "TypeScript types index"),
        ("common.ts", "typescript_module", "Common TypeScript types"),
        ("models.ts", "typescript_module", "Shared data models"),
    ],
    
    "shared/docs": [
        ("api-contract.md", "markdown", "Service API contracts"),
        ("data-models.md", "markdown", "Shared data models"),
        ("communication.md", "markdown", "Inter-service communication"),
    ],
    
    # 11. SCRIPTS
    "scripts/setup": [
        ("install_dependencies.sh", "shell_script", "Install all dependencies"),
        ("setup_dev_env.sh", "shell_script", "Setup development environment"),
        ("init_database.sh", "shell_script", "Initialize database"),
    ],
    
    "scripts/build": [
        ("build_all.sh", "shell_script", "Build all services"),
        ("build_api.sh", "shell_script", "Build API service"),
        ("build_dashboard.sh", "shell_script", "Build dashboard"),
        ("build_security.sh", "shell_script", "Build security services"),
    ],
    
    "scripts/deploy": [
        ("deploy_dev.sh", "shell_script", "Deploy to development"),
        ("deploy_staging.sh", "shell_script", "Deploy to staging"),
        ("deploy_prod.sh", "shell_script", "Deploy to production"),
    ],
    
    "scripts/database": [
        ("seed_data.py", "python_module", "Seed database with data"),
        ("backup.sh", "shell_script", "Backup database"),
        ("restore.sh", "shell_script", "Restore database"),
        ("migrate.sh", "shell_script", "Run migrations"),
    ],
    
    "scripts/testing": [
        ("run_all_tests.sh", "shell_script", "Run all tests"),
        ("run_integration_tests.sh", "shell_script", "Run integration tests"),
        ("run_load_tests.sh", "shell_script", "Run load tests"),
    ],
    
    "scripts/maintenance": [
        ("cleanup.sh", "shell_script", "Cleanup old data"),
        ("health_check.sh", "shell_script", "System health check"),
        ("log_rotation.sh", "shell_script", "Log rotation"),
    ],
    
    # 12. SECURITY ENGINE
    "packages/security-engine/scanner_go/internal/config": [
        ("config.go", "go_file", "Configuration management"),
    ],
    
    "packages/security-engine/scanner_go/internal/analyzer": [
        ("static_analyzer.go", "go_file", "Static code analyzer"),
        ("pattern_matcher.go", "go_file", "Pattern matching"),
    ],
    
    "packages/security-engine/scanner_go/internal/reporter": [
        ("reporter.go", "go_file", "Report generation"),
    ],
    
    "packages/security-engine/scanner_go/internal/api": [
        ("handlers.go", "go_file", "HTTP handlers"),
    ],
    
    "packages/security-engine/scanner_go/tests": [
        ("scanner_test.go", "go_file", "Scanner tests"),
        ("analyzer_test.go", "go_file", "Analyzer tests"),
    ],
    
    "packages/security-engine/labyrinth_rust/tests": [
        ("integration_test.rs", "rust_file", "Integration tests"),
    ],
    
    "packages/security-engine/labyrinth_rust/benches": [
        ("labyrinth_bench.rs", "rust_file", "Performance benchmarks"),
    ],
    
    "packages/security-engine/detector_python/detector": [
        ("__init__.py", "python_init", "Detector package"),
        ("ml_detector.py", "python_module", "ML-based detection"),
        ("rule_engine.py", "python_module", "Rule-based detection"),
        ("threat_classifier.py", "python_module", "Threat classification"),
        ("alert_manager.py", "python_module", "Alert management"),
    ],
    
    "packages/security-engine/detector_python/models": [
        (".gitkeep", "gitkeep", "Keep folder for ML models"),
    ],
    
    "packages/security-engine/detector_python/tests": [
        ("__init__.py", "python_init", "Tests package"),
        ("test_detector.py", "test_python", "Detector tests"),
        ("test_rule_engine.py", "test_python", "Rule engine tests"),
    ],
    
    # 13. OTHERS
    "temp": [
        (".gitkeep", "gitkeep", "Keep folder in git"),
        ("README.md", "markdown", "Temporary files folder"),
    ],
    
    "archive/old_docs": [
        (".gitkeep", "gitkeep", "Keep folder"),
        ("README.md", "markdown", "Archived documentation"),
    ],
    
    "automation/n8n/credentials": [
        (".gitkeep", "gitkeep", "Keep folder"),
        ("credentials.example.json", "markdown", "Example credentials"),
        ("README.md", "markdown", "Credentials setup guide"),
    ],
    
    # 14. GENERAL TESTS
    "tests/security": [
        ("test_auth.py", "test_python", "Security authentication tests"),
        ("test_vulnerabilities.py", "test_python", "Vulnerability scanning tests"),
        ("test_encryption.py", "test_python", "Encryption tests"),
    ],
    
    "tests/e2e": [
        ("test_full_scan_workflow.py", "test_python", "Complete scan workflow"),
        ("test_threat_response.py", "test_python", "Threat response workflow"),
        ("test_recovery_system.py", "test_python", "Recovery system test"),
    ],
    
    "tests/load": [
        ("locustfile.py", "python_module", "Locust load test configuration"),
        ("k6-script.js", "typescript_module", "K6 load test script"),
        ("results.md", "markdown", "Load test results documentation"),
    ],
}


def get_component_name(filename: str) -> str:
    """Extract component name from filename"""
    name = filename.replace(".tsx", "").replace(".ts", "").replace(".py", "")
    # Convert snake_case or kebab-case to PascalCase
    return ''.join(word.capitalize() for word in name.replace("-", "_").split("_"))


def get_class_name(filename: str) -> str:
    """Get CSS class name from component name"""
    name = filename.replace(".tsx", "").replace(".ts", "")
    return name.lower().replace("_", "-")


def get_module_name(filename: str) -> str:
    """Get module name from filename"""
    return filename.rsplit(".", 1)[0]


def get_package_name(path: str) -> str:
    """Get Go package name from path"""
    return path.split("/")[-1]


def generate_file_content(filename: str, template_type: str, description: str, path: str) -> str:
    """Generate file content based on template type"""
    template = TEMPLATES.get(template_type, "")
    
    date = datetime.now().strftime("%Y-%m-%d")
    component_name = get_component_name(filename)
    class_name = get_class_name(filename)
    module_name = get_module_name(filename)
    package_name = get_package_name(path)
    script_name = module_name
    contract_name = component_name
    
    title = description
    
    return template.format(
        docstring=description,
        date=date,
        component_name=component_name,
        class_name=class_name,
        module_name=module_name,
        package_name=package_name,
        script_name=script_name,
        title=title,
        contract_name=contract_name,
    )


def create_file(filepath: Path, content: str):
    """Create a file with content"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    if filepath.exists():
        print(f"  ⚠️  SKIP (exists): {filepath.relative_to(BASE_DIR)}")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Make shell scripts executable
    if filepath.suffix == '.sh':
        os.chmod(filepath, 0o755)
    
    print(f"  ✅ CREATE: {filepath.relative_to(BASE_DIR)}")
    return True


def generate_structure(dry_run: bool = False):
    """Generate entire project structure"""
    print("=" * 70)
    print("🚀 PROJECT STRUCTURE GENERATOR")
    print("=" * 70)
    print()
    
    created_count = 0
    skipped_count = 0
    total_count = sum(len(files) for files in FILE_STRUCTURE.values())
    
    print(f"📊 Total files to create: {total_count}")
    print()
    
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be created")
        print()
    
    for folder_path, files in FILE_STRUCTURE.items():
        full_path = BASE_DIR / folder_path
        
        print(f"\n📁 {folder_path}/")
        
        for filename, template_type, description in files:
            filepath = full_path / filename
            content = generate_file_content(filename, template_type, description, folder_path)
            
            if not dry_run:
                if create_file(filepath, content):
                    created_count += 1
                else:
                    skipped_count += 1
            else:
                print(f"  📄 WOULD CREATE: {filename} ({description})")
    
    print()
    print("=" * 70)
    print("✅ GENERATION COMPLETE!")
    print("=" * 70)
    print(f"✨ Created: {created_count} files")
    print(f"⚠️  Skipped: {skipped_count} files (already exist)")
    print(f"📊 Total:   {total_count} files")
    print()


def main():
    """Main function"""
    import sys
    
    dry_run = "--dry-run" in sys.argv or "-d" in sys.argv
    
    print()
    print("┌" + "─" * 68 + "┐")
    print("│" + " " * 15 + "🏗️  AUTOMATIC STRUCTURE GENERATOR" + " " * 18 + "│")
    print("└" + "─" * 68 + "┘")
    print()
    
    if dry_run:
        print("⚠️  Running in DRY RUN mode")
        print("   No files will be created, only showing what would happen")
        print()
    else:
        print("⚡ Running in LIVE mode")
        print("   Files will be created in your project")
        print()
        response = input("Continue? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
        print()
    
    generate_structure(dry_run=dry_run)
    
    if not dry_run:
        print("🎉 Next steps:")
        print("   1. Review the generated files")
        print("   2. Replace TODO comments with actual implementations")
        print("   3. Run tests to ensure everything works")
        print()


if __name__ == "__main__":
    main()

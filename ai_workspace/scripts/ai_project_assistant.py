#!/usr/bin/env python3
"""
AI Project Assistant

This script helps the AI understand the project structure and provides
guidance on working with the Infinite AI Security platform.
"""

import os
import json
from pathlib import Path
import yaml
from typing import Dict, List


class AIProjectAssistant:
    def __init__(self, project_root: str = None):
        """
        Initialize the AI Project Assistant.
        
        Args:
            project_root: Root directory of the project
        """
        if project_root is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.project_root = project_root
        self.config_path = os.path.join(project_root, 'ai_workspace', 'config', 'ai_config.yaml')
        
        # Load configuration
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def get_project_overview(self) -> str:
        """
        Get an overview of the project for the AI.
        
        Returns:
            String with project overview information
        """
        overview = """
# Infinite AI Security Platform - Project Overview

## Project Purpose
This is a comprehensive AI security platform with multi-agent systems, security scanning, and advanced defense mechanisms.

## Key Components
1. **AI Hub** - Python-based AI orchestration using LangGraph
2. **Security Scanner** - Go-based high-performance scanner
3. **Labyrinth Defense** - Rust-based dynamic defense system
4. **API Gateway** - FastAPI-based service coordination
5. **React Dashboard** - Real-time monitoring and control interface

## Architecture
- Multi-service architecture with microservices
- LangGraph for 200-node AI orchestration workflows
- 50-level pipeline system for complex operations
- Multi-region SaaS platform design
- Real-time monitoring and dashboards

## Key Directories
- `api/` - API Gateway service
- `agents/` - AI agent implementations  
- `services/` - Core microservices
- `frontend/` - React dashboard
- `docs/` - Documentation
- `scripts/` - Automation scripts
- `tests/` - Test suites
- `ai_workspace/` - Your dedicated workspace (you are here)

## Working Guidelines for AI
1. Always use the Safe File Editor to modify files
2. Make small, focused changes
3. Test your changes when possible
4. Document your modifications
5. Follow existing code patterns and styles
6. Respect the project's multi-service architecture
        """
        return overview

    def get_allowed_operations(self) -> str:
        """
        Get information about allowed operations for the AI.
        
        Returns:
            String with allowed operations information
        """
        operations = f"""
# Allowed Operations

## Read Operations
- You can read files in these directories: {', '.join(self.config.get('allowed_directories', []))}
- You can read files with these extensions: {', '.join(self.config.get('allowed_file_extensions', []))}

## Write Operations  
- You can write to the same directories and file types
- All changes are backed up automatically
- Changes are logged for review

## Restricted Areas
- Do not modify: {', '.join(self.config.get('restricted_directories', []))}
- Do not execute code directly
- Do not delete files
- Do not run system commands

## Safety Measures
- File backups are created before modification
- All changes are logged
- Maximum file size for editing: {self.config.get('safety', {}).get('max_file_size', 5242880) / (1024*1024)} MB
        """
        return operations

    def get_project_structure_summary(self) -> str:
        """
        Get a summary of the project structure.

        Returns:
            String with project structure information
        """
        try:
            # Import the SafeFileEditor to get actual project structure
            import sys
            from pathlib import Path

            # Add the tools directory to the Python path
            tools_dir = Path(__file__).parent.parent / "tools"
            sys.path.insert(0, str(tools_dir))

            from safe_file_editor import SafeFileEditor
            editor = SafeFileEditor()
            structure = editor.get_project_structure(max_depth=2)  # Only show top 2 levels

            # Create a summary from the actual structure
            structure_info = "# Project Structure Summary\n\n"

            for directory, contents in list(structure.items())[:10]:  # Limit to first 10 directories
                if directory == '':
                    directory = '(root)'
                structure_info += f"## `{directory or '(root)'}`\n"
                if contents['directories']:
                    structure_info += f"- **Subdirectories**: {', '.join(contents['directories'][:5])}"  # Limit display
                    if len(contents['directories']) > 5:
                        structure_info += f", ... ({len(contents['directories'])-5} more)"
                    structure_info += "\n"
                if contents['files']:
                    structure_info += f"- **Files**: {', '.join(contents['files'][:5])}"  # Limit display
                    if len(contents['files']) > 5:
                        structure_info += f", ... ({len(contents['files'])-5} more)"
                    structure_info += "\n"
                structure_info += "\n"

            structure_info += """
## Key Services
- `ai-hub/` - AI orchestration with LangGraph (Python)
- `scanner-go/` - Security scanning engine (Go)
- `labyrinth-rust/` - Defense mechanisms (Rust)
- `api-gateway/` - FastAPI service coordination
- `subscription-service/` - Billing & subscription management

## Frontend
- `frontend/` - React dashboard with real-time visualization
- `dashboard-react/` - Alternate React dashboard implementation

## AI Components
- `agents/` - Individual AI agents
- `ai_workspace/` - Your dedicated AI workspace (current location)
- `core-rust/` - Rust AI implementations
- `langgraph*` - LangGraph orchestration files

## Security Components
- `security_advanced/` - Advanced security features
- `reverse_engineering/` - Reverse engineering tools
- `datacenter_security/` - Data center security components

## Infrastructure & Operations
- `infrastructure/` - Docker, Kubernetes configs
- `scripts/` - Automation and setup scripts
- `deployment/` - Deployment configurations
- `observability/` - Monitoring and logging

## Documentation & Testing
- `docs/` - Project documentation
- `tests/` - Test suites for all services
- Various markdown files with project details
            """
            return structure_info
        except Exception:
            # Fallback to original static content if import fails
            structure_info = """
# Project Structure Summary

## Services
- `ai-hub/` - AI orchestration with LangGraph (Python)
- `scanner-go/` - Security scanning engine (Go)
- `labyrinth-rust/` - Defense mechanisms (Rust)
- `api-gateway/` - FastAPI service coordination
- `subscription-service/` - Billing & subscription management

## Frontend
- `frontend/` - React dashboard with real-time visualization
- `dashboard-react/` - Alternate React dashboard implementation

## AI Components
- `agents/` - Individual AI agents
- `ai_workspace/` - Your dedicated AI workspace (current location)
- `core-rust/` - Rust AI implementations
- `langgraph*` - LangGraph orchestration files

## Security Components
- `security_advanced/` - Advanced security features
- `reverse_engineering/` - Reverse engineering tools
- `datacenter_security/` - Data center security components

## Infrastructure & Operations
- `infrastructure/` - Docker, Kubernetes configs
- `scripts/` - Automation and setup scripts
- `deployment/` - Deployment configurations
- `observability/` - Monitoring and logging

## Documentation & Testing
- `docs/` - Project documentation
- `tests/` - Test suites for all services
- Various markdown files with project details
            """
            return structure_info

    def get_common_tasks(self) -> str:
        """
        Get information about common tasks the AI might perform.
        
        Returns:
            String with common tasks information
        """
        tasks = """
# Common Tasks for AI

## Code Development
- Implement new AI agents in the `agents/` directory
- Enhance existing services in `services/` or `api/`
- Add new workflow nodes to the LangGraph orchestration
- Improve security scanning capabilities in `scanner-go/`
- Enhance the React dashboard in `frontend/`

## Code Review & Improvement
- Refactor existing code for better performance
- Add documentation to existing functions and classes
- Improve error handling and validation
- Optimize database queries and API responses
- Enhance security measures across services

## Bug Fixes
- Identify and fix issues in existing code
- Improve error handling and edge cases
- Address performance bottlenecks
- Fix integration issues between services

## Feature Implementation
- Add new API endpoints in the API Gateway
- Implement new security scanning rules
- Create new visualization components in the dashboard
- Enhance the multi-agent coordination system
        """
        return tasks

    def get_working_tips(self) -> str:
        """
        Get working tips for the AI.
        
        Returns:
            String with working tips
        """
        tips = """
# Working Tips

## Best Practices
1. Always make incremental changes and test them
2. Follow the existing code style and conventions
3. Add appropriate logging and error handling
4. Write clear docstrings for functions and classes
5. Respect the service boundaries in the microservices architecture
6. Consider security implications of your changes

## Safety Guidelines
1. Use the Safe File Editor for all file modifications
2. Don't remove existing error handling or validation
3. Test your changes in a development environment first
4. Make sure new code follows the same security patterns
5. Keep changes focused and avoid large modifications in one go

## Useful Commands
- `python ai_workspace/tools/safe_file_editor.py read <file>` - Read a file
- `python ai_workspace/tools/safe_file_editor.py write <file> --content "<content>"` - Write to a file
- Check existing tests in `tests/` directories to understand expected behavior
- Look at `README.md` and `PROJECT_STRUCTURE.md` for architectural details

## Understanding the Codebase
- Start with `README.md` for overall project understanding
- Check `PROJECT_STRUCTURE.md` for detailed directory structure
- Look at `config.py` to understand configuration options
- Review service-specific README files for implementation details
- Examine existing agents to understand the agent patterns
        """
        return tips

    def get_complete_guide(self) -> str:
        """
        Get the complete guide for working with the project.
        
        Returns:
            String with complete guide
        """
        guide = f"""
{self.get_project_overview()}

{self.get_allowed_operations()}

{self.get_project_structure_summary()}

{self.get_common_tasks()}

{self.get_working_tips()}

# Getting Started

1. Start by exploring the README.md and PROJECT_STRUCTURE.md files
2. familiarize yourself with the service architecture
3. Use the Safe File Editor for any modifications
4. Check existing code patterns before implementing new features
5. Remember that you're in the ai_workspace/ directory - this is your dedicated area

Remember: You have the ability to edit, modify, and improve all parts of the project within the allowed boundaries. Use your capabilities to enhance the platform's functionality, security, and performance.
"""
        return guide


def main():
    """Command line interface for the AI Project Assistant."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Project Assistant for Infinite AI Security Platform')
    parser.add_argument('--section', 
                       choices=['overview', 'operations', 'structure', 'tasks', 'tips', 'complete'],
                       default='complete',
                       help='Section to display')
    
    args = parser.parse_args()
    
    assistant = AIProjectAssistant()
    
    if args.section == 'overview':
        print(assistant.get_project_overview())
    elif args.section == 'operations':
        print(assistant.get_allowed_operations())
    elif args.section == 'structure':
        print(assistant.get_project_structure_summary())
    elif args.section == 'tasks':
        print(assistant.get_common_tasks())
    elif args.section == 'tips':
        print(assistant.get_working_tips())
    elif args.section == 'complete':
        print(assistant.get_complete_guide())


if __name__ == "__main__":
    main()
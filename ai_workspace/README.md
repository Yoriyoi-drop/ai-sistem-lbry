# AI Workspace for Infinite AI Security Platform

Welcome to your dedicated AI workspace! This directory contains all the tools and configurations needed for AI to work on the Infinite AI Security Platform project.

## 📁 Directory Structure

```
ai_workspace/
├── config/           # Configuration files
│   └── ai_config.yaml # AI workspace settings
├── tools/            # Safe tools for AI operations
│   └── safe_file_editor.py # Safe file reading/writing tool
├── scripts/          # Helper scripts
│   └── ai_project_assistant.py # Project guide for AI
├── work/             # Working area for AI operations
│   └── backup/       # Automated backups of modified files
└── logs/             # Operation logs
    └── ai_changes.log # Log of all AI file operations
```

## 🛠️ Available Tools

### Safe File Editor
The `safe_file_editor.py` tool allows safe file operations with:
- Path validation against allowed directories
- Content validation to prevent dangerous operations
- Automatic backup creation before modifications
- Comprehensive logging of all changes
- File size validation

**Usage:**
```bash
# Read a file
python tools/safe_file_editor.py read path/to/file

# Write to a file
python tools/safe_file_editor.py write path/to/file --content "new content"

# Append to a file
python tools/safe_file_editor.py append path/to/file --content "additional content"
```

### AI Project Assistant
The `ai_project_assistant.py` script provides guidance on the project structure and working practices:

```bash
# Get complete guide
python scripts/ai_project_assistant.py

# Get specific section
python scripts/ai_project_assistant.py --section overview
```

Available sections: `overview`, `operations`, `structure`, `tasks`, `tips`, `complete`

## ⚙️ Configuration

The `config/ai_config.yaml` file defines:
- Allowed directories and file extensions for AI operations
- Safety settings (backup, logging, file size limits)
- Access permissions and restrictions
- Service connection settings

## 🚀 Getting Started

1. **Understand the project**: Run the AI Project Assistant to get familiar with the platform:
   ```bash
   python scripts/ai_project_assistant.py
   ```

2. **Explore the project structure**: Start with `README.md` and `PROJECT_STRUCTURE.md` in the root directory

3. **Check allowed operations**: Review `ai_config.yaml` to understand what files you can modify

4. **Start working**: Use the Safe File Editor to make changes to project files

## 🛡️ Safety Features

- **Path validation**: Only allowed directories can be accessed
- **Content validation**: Dangerous patterns are blocked
- **Automatic backups**: All modified files are backed up before changes
- **Change logging**: All operations are logged for review
- **File size limits**: Large files are protected from modification
- **Restricted access**: Critical directories like `.git`, `venv` are protected

## 📝 Logging

All AI operations are logged to `logs/ai_changes.log` with timestamps and details about the operations performed.

## 🧭 Working Guidelines

1. Always use the Safe File Editor for file operations
2. Make focused, incremental changes
3. Follow existing code patterns and styles
4. Test changes when possible
5. Respect the microservices architecture
6. Consider security implications of your changes

## 🔍 Key Areas to Work On

- Enhance AI agent capabilities in the `agents/` directory
- Improve security scanning in `scanner-go/`
- Add new features to the React dashboard in `frontend/`
- Optimize the LangGraph orchestration in `ai-hub/`
- Implement new workflow nodes and improve pipeline efficiency
- Enhance the Labyrinth defense mechanisms in `labyrinth-rust/`

You now have a fully configured workspace to work on the Infinite AI Security Platform project safely and effectively!
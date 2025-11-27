#!/usr/bin/env python3
"""
Safe File Editor for AI Operations

This tool provides a safe way for AI to edit files in the project with built-in
validation, backup, and logging capabilities.
"""

import os
import shutil
import yaml
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import re


class SafeFileEditor:
    def __init__(self, config_path: str = None):
        """
        Initialize the Safe File Editor with configuration.

        Args:
            config_path: Path to the AI configuration file
        """
        # Default config path if not provided
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__),
                '..', 'config', 'ai_config.yaml'
            )

        # Verify config file exists before loading
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Setup logging
        self._setup_logging()

        # Project root
        self.project_root = self.config.get('project_root', os.getcwd())

        # Verify project root exists
        if not os.path.exists(self.project_root):
            self.logger.error(f"Project root does not exist: {self.project_root}")
            raise ValueError(f"Project root does not exist: {self.project_root}")

        # Get allowed directories and extensions
        self.allowed_directories = self.config.get('allowed_directories', [])
        self.restricted_directories = self.config.get('restricted_directories', [])
        self.allowed_extensions = self.config.get('allowed_file_extensions', [])

        # Safety settings
        self.enable_backup = self.config.get('safety', {}).get('enable_file_backup', True)
        self.backup_location = self.config.get('safety', {}).get('backup_location', 'work/backup')
        self.max_file_size = self.config.get('safety', {}).get('max_file_size', 5242880)  # 5MB
        self.dry_run_mode = self.config.get('safety', {}).get('dry_run_mode', False)  # Safety mode

        # Create backup directory if needed
        if self.enable_backup:
            backup_full_path = os.path.join(self.project_root, self.backup_location)
            os.makedirs(backup_full_path, exist_ok=True)
            self.logger.info(f"Backup directory created: {backup_full_path}")

    def _setup_logging(self):
        """Setup logging for AI file operations."""
        log_level_str = self.config.get('notifications', {}).get('log_level', 'INFO')
        log_level = getattr(logging, log_level_str.upper(), logging.INFO)
        
        log_file = os.path.join(
            self.config.get('workspace_dir', '.'), 
            self.config.get('safety', {}).get('log_location', 'logs/ai_changes.log')
        )
        
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()  # Also log to console
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _is_path_allowed(self, file_path: str) -> bool:
        """
        Check if the file path is in an allowed directory and has allowed extension.

        Args:
            file_path: Path to the file to check

        Returns:
            True if the file is allowed to be modified, False otherwise
        """
        try:
            # Normalize path to prevent directory traversal attacks
            path_obj = Path(file_path).resolve()
            project_root = Path(self.project_root).resolve()

            # Sanitize path - check for directory traversal
            if '..' in str(path_obj) or str(path_obj).startswith('../') or str(path_obj).startswith('..\\'):
                self.logger.warning(f"Path traversal detected in: {file_path}")
                return False

            # Check if file is within project root
            try:
                path_obj.relative_to(project_root)
            except ValueError:
                self.logger.warning(f"Path {file_path} is not within project root")
                return False

            # Check if file is in a restricted directory
            for restricted in self.restricted_directories:
                restricted_path = project_root / restricted
                try:
                    path_obj.relative_to(restricted_path)
                    self.logger.warning(f"Path {file_path} is in a restricted directory: {restricted}")
                    return False
                except ValueError:
                    continue

            # Check if file is in an allowed directory
            is_allowed = False
            for allowed_dir in self.allowed_directories:
                allowed_path = project_root / allowed_dir
                try:
                    path_obj.relative_to(allowed_path)
                    is_allowed = True
                    break
                except ValueError:
                    continue

            if not is_allowed:
                self.logger.warning(f"Path {file_path} is not in an allowed directory")
                return False

            # Check file extension
            file_ext = path_obj.suffix.lower()
            if file_ext not in self.allowed_extensions and file_ext != '':
                allowed_ext_str = ', '.join(self.allowed_extensions)
                self.logger.warning(f"File extension {file_ext} not allowed. Allowed: {allowed_ext_str}")
                return False

            # Special case: allow files without extensions if they're specifically .env files
            if file_ext == '' and path_obj.name != '.env':
                self.logger.warning(f"Files without extensions are not allowed: {file_path}")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Error validating path {file_path}: {str(e)}")
            return False

    def _create_backup(self, file_path: str) -> str:
        """
        Create a backup of the file before modification.

        Args:
            file_path: Path to the file to backup

        Returns:
            Path to the backup file
        """
        if not self.enable_backup:
            return None

        try:
            file_path_obj = Path(file_path).resolve()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            backup_filename = f"{file_path_obj.name}.{timestamp}.bak"

            # Create relative path structure in backup to preserve organization
            rel_path = file_path_obj.relative_to(Path(self.project_root).resolve())
            backup_dir = Path(self.project_root) / self.backup_location / rel_path.parent
            backup_dir.mkdir(parents=True, exist_ok=True)

            backup_path = str(backup_dir / backup_filename)

            shutil.copy2(file_path, backup_path)
            self.logger.info(f"Backup created: {backup_path}")

            return backup_path
        except Exception as e:
            self.logger.error(f"Failed to create backup for {file_path}: {str(e)}")
            return None

    def _validate_content(self, content: str) -> bool:
        """
        Validate content to prevent dangerous operations.

        Args:
            content: Content to validate

        Returns:
            True if content is safe, False otherwise
        """
        dangerous_patterns = [
            # System execution
            r'import\s+os',
            r'import\s+sys',
            r'subprocess\.',
            r'eval\s*\(',
            r'exec\s*\(',
            r'__import__\s*\(',
            r'compile\s*\(',
            r'os\.system',
            r'os\.popen',
            r'os\.exec',
            r'os\.spawn',
            r'shutil\.',
            r'execfile',
            # File system access
            r'open\s*\(',
            r'file\s*\(',
            r'io\.open',
            # Network operations
            r'urllib\.',
            r'requests\.',
            r'socket\.',
            r'ftplib.',
            # Code injection
            r'exec\(',
            r'eval\(',
            # Shell access
            r'bash',
            r'shell',
            r'cmd',
            # Dangerous imports
            r'import\s+subprocess',
            r'import\s+pty',
            r'import\s+ctypes',
            r'import\s+pickle',
        ]

        content_lower = content.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, content_lower):
                self.logger.warning(f"Dangerous pattern detected in content: {pattern}")
                return False

        # Additional checks for specific dangerous patterns
        dangerous_strings = [
            'rm -rf',
            '>:',  # potential file overwrite
            '>/dev/',
            '>/proc/',
            '>>/etc/',
            'chmod 777',
        ]

        for dangerous in dangerous_strings:
            if dangerous in content:
                self.logger.warning(f"Dangerous string detected in content: {dangerous}")
                return False

        return True

    def read_file(self, file_path: str) -> Optional[str]:
        """
        Safely read a file with validation.

        Args:
            file_path: Path to the file to read

        Returns:
            File content as string or None if failed
        """
        try:
            # Normalize the file path
            file_path = os.path.join(self.project_root, file_path.lstrip('/'))
            path_to_check = Path(file_path).resolve()

            # Validate path exists and is a file
            if not path_to_check.is_file():
                self.logger.error(f"File does not exist or is not a file: {path_to_check}")
                return None

            # Validate path
            if not self._is_path_allowed(str(path_to_check)):
                self.logger.error(f"Read operation denied for: {file_path}")
                return None

            # Check file size
            if path_to_check.stat().st_size > self.max_file_size:
                self.logger.error(f"File too large to read: {file_path} (size: {path_to_check.stat().st_size}, max: {self.max_file_size})")
                return None

            # Read the file
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            self.logger.info(f"File read successfully: {file_path} (size: {len(content)} chars)")
            return content

        except UnicodeDecodeError:
            self.logger.error(f"File is not a text file or contains invalid encoding: {file_path}")
            return None
        except PermissionError:
            self.logger.error(f"Permission denied reading file: {file_path}")
            return None
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {str(e)}")
            return None

    def write_file(self, file_path: str, content: str, create_dirs: bool = True) -> bool:
        """
        Safely write content to a file with validation, backup, and logging.

        Args:
            file_path: Path to the file to write
            content: Content to write to the file
            create_dirs: Whether to create parent directories if they don't exist

        Returns:
            True if successful, False otherwise
        """
        try:
            # Full path resolution
            full_path = os.path.join(self.project_root, file_path.lstrip('/'))
            path_to_check = Path(full_path).resolve()

            # Validate path
            if not self._is_path_allowed(str(path_to_check)):
                self.logger.error(f"Write operation denied for: {file_path}")
                return False

            # Validate content
            if not self._validate_content(content):
                self.logger.error(f"Content validation failed for: {file_path}")
                return False

            # Check file size to prevent extremely large files
            if len(content) > self.max_file_size:
                self.logger.error(f"Content too large to write: {file_path} (size: {len(content)}, max: {self.max_file_size})")
                return False

            # Check dry run mode
            if self.dry_run_mode:
                self.logger.info(f"[DRY RUN] Would write file: {file_path} (size: {len(content)} chars)")
                return True  # Return True in dry run mode to indicate validation passed

            # Create directory if needed
            if create_dirs:
                path_to_check.parent.mkdir(parents=True, exist_ok=True)

            # Create backup if file exists
            backup_path = None
            if path_to_check.exists():
                backup_path = self._create_backup(str(path_to_check))

            # Write the file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Log the change
            self.logger.info(f"File written successfully: {file_path} (size: {len(content)} chars)")
            if backup_path:
                self.logger.info(f"Backup available: {backup_path}")

            return True

        except PermissionError:
            self.logger.error(f"Permission denied writing file: {file_path}")
            return False
        except OSError as e:
            self.logger.error(f"OS error writing file {file_path}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Error writing file {file_path}: {str(e)}")
            return False

    def append_to_file(self, file_path: str, content: str) -> bool:
        """
        Safely append content to a file.

        Args:
            file_path: Path to the file to append to
            content: Content to append to the file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Full path resolution
            full_path = os.path.join(self.project_root, file_path.lstrip('/'))
            path_to_check = Path(full_path).resolve()

            # Validate path exists as a file or can be created
            if not path_to_check.exists():
                # If file doesn't exist, check that its parent directory exists and is allowed
                if not path_to_check.parent.exists():
                    if not self._is_path_allowed(str(path_to_check.parent)):
                        self.logger.error(f"Append operation denied for: {file_path} (parent directory not allowed)")
                        return False
                else:
                    # Check if the parent directory is allowed
                    if not self._is_path_allowed(str(path_to_check.parent)):
                        self.logger.error(f"Append operation denied for: {file_path} (parent directory not allowed)")
                        return False

            # Validate path
            if not self._is_path_allowed(str(path_to_check)):
                self.logger.error(f"Append operation denied for: {file_path}")
                return False

            # Validate content
            if not self._validate_content(content):
                self.logger.error(f"Content validation failed for: {file_path}")
                return False

            # Check content size to prevent extremely large appends
            if len(content) > self.max_file_size:
                self.logger.error(f"Content too large to append: {file_path} (size: {len(content)}, max: {self.max_file_size})")
                return False

            # Check dry run mode
            if self.dry_run_mode:
                self.logger.info(f"[DRY RUN] Would append to file: {file_path} (size: {len(content)} chars)")
                return True  # Return True in dry run mode to indicate validation passed

            # Create directory if needed
            path_to_check.parent.mkdir(parents=True, exist_ok=True)

            # Create backup if file exists
            backup_path = None
            if path_to_check.exists():
                # Check if file would exceed max size after append
                current_size = path_to_check.stat().st_size
                if current_size + len(content) > self.max_file_size:
                    self.logger.error(f"File would be too large after append: {file_path}")
                    return False
                backup_path = self._create_backup(str(path_to_check))

            # Append to the file
            with open(full_path, 'a', encoding='utf-8') as f:
                f.write(content)

            # Log the change
            self.logger.info(f"Content appended successfully to: {file_path} (size: {len(content)} chars)")
            if backup_path:
                self.logger.info(f"Backup available: {backup_path}")

            return True

        except PermissionError:
            self.logger.error(f"Permission denied appending to file: {file_path}")
            return False
        except OSError as e:
            self.logger.error(f"OS error appending to file {file_path}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Error appending to file {file_path}: {str(e)}")
            return False

    def get_project_structure(self, max_depth: int = 5) -> Dict:
        """
        Get the project directory structure for AI reference.

        Args:
            max_depth: Maximum depth to traverse in the directory tree

        Returns:
            Dictionary representing the project structure
        """
        structure = {}

        try:
            def _walk_with_depth(root, depth=0):
                if depth >= max_depth:
                    return

                # Get directories and files at this level
                try:
                    with os.scandir(root) as entries:
                        dirs = []
                        files = []

                        for entry in entries:
                            entry_path = entry.path
                            if entry.is_dir() and self._is_path_allowed(entry_path):
                                dirs.append(entry.name)
                            elif entry.is_file() and self._is_path_allowed(entry_path):
                                files.append(entry.name)

                        # Add to structure if there are allowed items
                        rel_path = os.path.relpath(root, self.project_root)
                        if rel_path == '.':
                            rel_path = ''

                        if dirs or files:
                            structure[rel_path] = {
                                'directories': dirs,
                                'files': files
                            }

                        # Recursively process subdirectories
                        for dirname in dirs:
                            subdir = os.path.join(root, dirname)
                            _walk_with_depth(subdir, depth + 1)

                except (PermissionError, OSError):
                    # Skip directories we can't access
                    pass

            _walk_with_depth(self.project_root)
        except Exception as e:
            self.logger.error(f"Error getting project structure: {str(e)}")

        return structure

    def search_files(self, pattern: str, file_extension: str = None) -> List[str]:
        """
        Search for files in allowed directories by pattern or extension.

        Args:
            pattern: Pattern to search for in filenames
            file_extension: Optional file extension to filter by

        Returns:
            List of matching file paths
        """
        results = []

        try:
            # Walk through allowed directories only
            for root, dirs, files in os.walk(self.project_root):
                # Filter directories to only allowed ones
                dirs[:] = [d for d in dirs if self._is_path_allowed(os.path.join(root, d))]

                for file in files:
                    file_path = os.path.join(root, file)

                    # Check if the file is allowed
                    if not self._is_path_allowed(file_path):
                        continue

                    # Check extension if specified
                    if file_extension and not file.lower().endswith(file_extension.lower()):
                        continue

                    # Check pattern match (case insensitive)
                    if pattern.lower() in file.lower():
                        results.append(file_path)

        except Exception as e:
            self.logger.error(f"Error searching for files: {str(e)}")

        return results

    def find_file(self, filename: str) -> str:
        """
        Find a specific file in the project.

        Args:
            filename: Name of the file to find

        Returns:
            Full path to the file if found, None otherwise
        """
        try:
            for root, dirs, files in os.walk(self.project_root):
                # Filter directories to only allowed ones
                dirs[:] = [d for d in dirs if self._is_path_allowed(os.path.join(root, d))]

                if filename in files:
                    file_path = os.path.join(root, filename)
                    if self._is_path_allowed(file_path):
                        return file_path
        except Exception as e:
            self.logger.error(f"Error finding file {filename}: {str(e)}")

        return None


def main():
    """Command line interface for the Safe File Editor."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Safe File Editor for AI Operations')
    parser.add_argument('action', choices=['read', 'write', 'append'], 
                       help='Action to perform: read, write, or append')
    parser.add_argument('file_path', help='Path to the file to operate on')
    parser.add_argument('--content', help='Content to write or append')
    parser.add_argument('--config', help='Path to configuration file')
    
    args = parser.parse_args()
    
    # Initialize the editor
    editor = SafeFileEditor(args.config)
    
    if args.action == 'read':
        content = editor.read_file(args.file_path)
        if content is not None:
            print(content)
        else:
            print(f"Error: Could not read file {args.file_path}")
            exit(1)
    elif args.action == 'write':
        if not args.content:
            print("Error: --content is required for write action")
            exit(1)
        success = editor.write_file(args.file_path, args.content)
        if not success:
            print(f"Error: Could not write to file {args.file_path}")
            exit(1)
    elif args.action == 'append':
        if not args.content:
            print("Error: --content is required for append action")
            exit(1)
        success = editor.append_to_file(args.file_path, args.content)
        if not success:
            print(f"Error: Could not append to file {args.file_path}")
            exit(1)


if __name__ == "__main__":
    main()
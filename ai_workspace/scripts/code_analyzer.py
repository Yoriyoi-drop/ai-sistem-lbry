#!/usr/bin/env python3
"""
Code Analysis Tool for AI

This script helps the AI analyze code files and understand patterns in the project.
"""

import os
import re
from pathlib import Path
import sys
from typing import Dict, List, Tuple


class CodeAnalyzer:
    def __init__(self, project_root: str = None):
        """
        Initialize the Code Analyzer.
        
        Args:
            project_root: Root directory of the project
        """
        if project_root is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.project_root = project_root
        
        # Import SafeFileEditor to leverage its path validation
        tools_dir = os.path.join(self.project_root, 'ai_workspace', 'tools')
        sys.path.insert(0, tools_dir)
        
        from safe_file_editor import SafeFileEditor
        self.editor = SafeFileEditor()

    def analyze_file(self, file_path: str) -> Dict:
        """
        Analyze a code file to extract important information.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Dictionary with analysis results
        """
        content = self.editor.read_file(file_path)
        if not content:
            return {"error": f"Could not read file: {file_path}"}
        
        analysis = {
            "file_path": file_path,
            "line_count": len(content.splitlines()),
            "char_count": len(content),
            "imports": [],
            "functions": [],
            "classes": [],
            "comments": 0,
            "docstrings": 0,
        }
        
        # Language-specific analysis
        if file_path.endswith('.py'):
            self._analyze_python(content, analysis)
        elif file_path.endswith(('.js', '.ts', '.tsx', '.jsx')):
            self._analyze_javascript(content, analysis)
        elif file_path.endswith('.go'):
            self._analyze_go(content, analysis)
        elif file_path.endswith('.rs'):
            self._analyze_rust(content, analysis)
        
        return analysis

    def _analyze_python(self, content: str, analysis: Dict):
        """Analyze Python code."""
        lines = content.splitlines()
        
        # Count comments and docstrings
        in_multiline_docstring = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#'):
                analysis["comments"] += 1
            elif stripped.startswith('"""') or stripped.startswith("'''"):
                analysis["docstrings"] += 1
                # Simple detection of multiline docstrings
                if (stripped.count('"""') == 1 or stripped.count("'''") == 1) and not in_multiline_docstring:
                    in_multiline_docstring = True
                elif in_multiline_docstring and ('"""' in stripped or "'''" in stripped):
                    in_multiline_docstring = False
            elif in_multiline_docstring:
                analysis["docstrings"] += 1
        
        # Find imports
        import_pattern = r'^(import|from)\s+(\w+|\w+\.\w+)'
        for line in lines:
            match = re.match(import_pattern, line.strip())
            if match:
                analysis["imports"].append(match.group(0).strip())
        
        # Find functions and classes
        func_pattern = r'def\s+(\w+)\s*\('
        class_pattern = r'class\s+(\w+)'
        
        for line in lines:
            func_match = re.search(func_pattern, line.strip())
            if func_match:
                analysis["functions"].append(func_match.group(1))
            
            class_match = re.search(class_pattern, line.strip())
            if class_match:
                analysis["classes"].append(class_match.group(1))

    def _analyze_javascript(self, content: str, analysis: Dict):
        """Analyze JavaScript/TypeScript code."""
        lines = content.splitlines()
        
        # Count comments
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('//'):
                analysis["comments"] += 1
            elif stripped.startswith('/*') or stripped.startswith('/**'):
                analysis["comments"] += 1  # Simplified counting
        
        # Find imports (simplified)
        import_pattern = r'import\s+.*\s+from\s+[\'"].*[\'"]'
        for line in lines:
            match = re.search(import_pattern, line)
            if match:
                analysis["imports"].append(match.group(0).strip())
        
        # Find functions and classes
        func_pattern = r'function\s+(\w+)'
        arrow_func_pattern = r'const\s+\w+\s*=\s*\w*\s*=>'
        class_pattern = r'class\s+(\w+)'
        
        for line in lines:
            func_match = re.search(func_pattern, line)
            if func_match:
                analysis["functions"].append(func_match.group(1))
            
            arrow_match = re.search(arrow_func_pattern, line)
            if arrow_match:
                analysis["functions"].append("arrow_function")
            
            class_match = re.search(class_pattern, line)
            if class_match:
                analysis["classes"].append(class_match.group(1))

    def _analyze_go(self, content: str, analysis: Dict):
        """Analyze Go code."""
        lines = content.splitlines()
        
        # Count comments
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('//'):
                analysis["comments"] += 1
            elif stripped.startswith('/*'):
                analysis["comments"] += 1  # Simplified counting
        
        # Find imports
        import_pattern = r'import\s+\(?|import\s+"'
        for line in lines:
            if re.search(import_pattern, line):
                analysis["imports"].append(line.strip())
        
        # Find functions
        func_pattern = r'func\s+(?:\([^)]+\)\s+)?(\w+)\s*\('
        for line in lines:
            match = re.search(func_pattern, line)
            if match:
                analysis["functions"].append(match.group(1))
        
        # Find types (structs, interfaces)
        type_pattern = r'type\s+(\w+)\s+(struct|interface)'
        for line in lines:
            match = re.search(type_pattern, line)
            if match:
                analysis["classes"].append(f"{match.group(1)} ({match.group(2)})")

    def _analyze_rust(self, content: str, analysis: Dict):
        """Analyze Rust code."""
        lines = content.splitlines()
        
        # Count comments
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('//'):
                analysis["comments"] += 1
            elif stripped.startswith('/*'):
                analysis["comments"] += 1  # Simplified counting
        
        # Find imports
        import_pattern = r'use\s+[\w:]+'
        for line in lines:
            match = re.search(import_pattern, line)
            if match:
                analysis["imports"].append(match.group(0).strip())
        
        # Find functions
        func_pattern = r'fn\s+(\w+)\s*\('
        for line in lines:
            match = re.search(func_pattern, line)
            if match:
                analysis["functions"].append(match.group(1))
        
        # Find structs and enums
        struct_pattern = r'struct\s+(\w+)'
        enum_pattern = r'enum\s+(\w+)'
        for line in lines:
            struct_match = re.search(struct_pattern, line)
            if struct_match:
                analysis["classes"].append(f"{struct_match.group(1)} (struct)")
            
            enum_match = re.search(enum_pattern, line)
            if enum_match:
                analysis["classes"].append(f"{enum_match.group(1)} (enum)")

    def analyze_directory(self, dir_path: str, file_extensions: List[str] = None) -> Dict:
        """
        Analyze all code files in a directory.
        
        Args:
            dir_path: Path to the directory to analyze
            file_extensions: List of file extensions to include (e.g., ['.py', '.js'])
            
        Returns:
            Dictionary with analysis results
        """
        if file_extensions is None:
            file_extensions = ['.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs']
        
        analysis = {
            "directory": dir_path,
            "files": [],
            "total_lines": 0,
            "total_chars": 0,
            "languages": {}
        }
        
        # Find files in the directory
        for root, dirs, files in os.walk(os.path.join(self.project_root, dir_path)):
            # Filter out directories that are not allowed
            dirs[:] = [d for d in dirs if self.editor._is_path_allowed(os.path.join(root, d))]
            
            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.project_root)
                    
                    if self.editor._is_path_allowed(full_path):
                        file_analysis = self.analyze_file(rel_path)
                        if "error" not in file_analysis:
                            analysis["files"].append(file_analysis)
                            analysis["total_lines"] += file_analysis["line_count"]
                            analysis["total_chars"] += file_analysis["char_count"]
                            
                            # Track language usage
                            ext = os.path.splitext(file)[1]
                            if ext in analysis["languages"]:
                                analysis["languages"][ext] += 1
                            else:
                                analysis["languages"][ext] = 1
        
        return analysis

    def find_patterns(self, pattern: str, file_extensions: List[str] = None) -> List[Tuple[str, List[str]]]:
        """
        Find occurrences of a specific pattern in code files.
        
        Args:
            pattern: Pattern to search for
            file_extensions: List of file extensions to search in
            
        Returns:
            List of tuples (file_path, matches)
        """
        if file_extensions is None:
            file_extensions = ['.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs']
        
        results = []
        
        # Search all allowed files
        for root, dirs, files in os.walk(self.project_root):
            # Filter directories to only allowed ones
            dirs[:] = [d for d in dirs if self.editor._is_path_allowed(os.path.join(root, d))]
            
            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.project_root)
                    
                    if self.editor._is_path_allowed(file_path):
                        content = self.editor.read_file(rel_path)
                        if content:
                            matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
                            if matches:
                                results.append((rel_path, matches))
        
        return results

    def get_complexity_metrics(self) -> Dict:
        """
        Get overall project complexity metrics.
        
        Returns:
            Dictionary with complexity metrics
        """
        metrics = {
            "total_files": 0,
            "total_lines": 0,
            "by_language": {},
            "by_directory": {}
        }
        
        # Scan for code files
        for root, dirs, files in os.walk(self.project_root):
            # Filter directories to only allowed ones
            dirs[:] = [d for d in dirs if self.editor._is_path_allowed(os.path.join(root, d))]
            
            for file in files:
                if self.editor._is_path_allowed(os.path.join(root, file)):
                    # Check if it's a code file
                    ext = os.path.splitext(file)[1]
                    if ext in ['.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.java', '.cpp', '.c', '.h']:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.project_root)
                        content = self.editor.read_file(rel_path)
                        
                        if content:
                            lines = len(content.splitlines())
                            
                            metrics["total_files"] += 1
                            metrics["total_lines"] += lines
                            
                            # Update language counts
                            if ext in metrics["by_language"]:
                                metrics["by_language"][ext]["files"] += 1
                                metrics["by_language"][ext]["lines"] += lines
                            else:
                                metrics["by_language"][ext] = {"files": 1, "lines": lines}
                            
                            # Update directory counts
                            dir_path = os.path.dirname(rel_path)
                            if dir_path in metrics["by_directory"]:
                                metrics["by_directory"][dir_path]["files"] += 1
                                metrics["by_directory"][dir_path]["lines"] += lines
                            else:
                                metrics["by_directory"][dir_path] = {"files": 1, "lines": lines}
        
        return metrics


def main():
    """Command line interface for the Code Analyzer."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Code Analysis Tool for AI')
    parser.add_argument('action', choices=['analyze-file', 'analyze-dir', 'find-pattern', 'complexity'], 
                       help='Action to perform')
    parser.add_argument('target', help='Target for the action (file path, directory, or pattern)')
    parser.add_argument('--extensions', nargs='+', 
                       help='File extensions to include in analysis (e.g., .py .js)')
    
    args = parser.parse_args()
    
    analyzer = CodeAnalyzer()
    
    if args.action == 'analyze-file':
        result = analyzer.analyze_file(args.target)
        print(f"Analysis of {args.target}:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    elif args.action == 'analyze-dir':
        extensions = args.extensions or ['.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs']
        result = analyzer.analyze_directory(args.target, extensions)
        print(f"Analysis of {args.target}:")
        print(f"  Files analyzed: {len(result['files'])}")
        print(f"  Total lines: {result['total_lines']}")
        print(f"  Total chars: {result['total_chars']}")
        print(f"  Languages: {result['languages']}")
    elif args.action == 'find-pattern':
        extensions = args.extensions or ['.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs']
        results = analyzer.find_patterns(args.target, extensions)
        print(f"Pattern '{args.target}' found in:")
        for file_path, matches in results:
            print(f"  {file_path}: {len(matches)} matches")
    elif args.action == 'complexity':
        result = analyzer.get_complexity_metrics()
        print("Project Complexity Metrics:")
        print(f"  Total files: {result['total_files']}")
        print(f"  Total lines: {result['total_lines']}")
        print(f"  By language: {result['by_language']}")
        # Print top 5 directories by line count
        sorted_dirs = sorted(result['by_directory'].items(), key=lambda x: x[1]['lines'], reverse=True)[:5]
        print("  Top directories by lines:")
        for dir_path, metrics in sorted_dirs:
            print(f"    {dir_path}: {metrics['lines']} lines ({metrics['files']} files)")


if __name__ == "__main__":
    main()
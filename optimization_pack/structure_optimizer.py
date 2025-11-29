"""
Module Structure Optimizer
Implements dependency grouping and modularization for better resource usage
"""
import os
from typing import Dict, List, Callable, Any
import importlib
from pathlib import Path


class ModuleOptimizer:
    """
    Optimizes module structure and loading patterns
    """
    
    def __init__(self):
        self.modules = {}
        self.dependencies = {}
        self.load_order = []
    
    def register_module(self, name: str, path: str, dependencies: List[str] = None):
        """
        Register a module with its dependencies for optimized loading
        """
        if dependencies is None:
            dependencies = []
        
        self.modules[name] = path
        self.dependencies[name] = dependencies
    
    def get_load_order(self) -> List[str]:
        """
        Calculate optimal load order based on dependencies
        """
        visited = set()
        order = []
        
        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            
            for dep in self.dependencies.get(node, []):
                dfs(dep)
            
            order.append(node)
        
        for module in self.modules:
            dfs(module)
        
        return order


class ProjectStructureOptimizer:
    """
    Optimizes the overall project structure for better performance
    """
    
    @staticmethod
    def create_optimized_structure():
        """
        Creates an optimized directory structure with logical grouping
        """
        optimized_dirs = [
            'core/',           # Core functionality
            'core/models/',    # Data models
            'core/database/',  # Database operations
            'core/security/',  # Security operations
            'services/',       # Business logic services
            'services/ai/',    # AI-specific services
            'services/security/',  # Security-specific services
            'api/',           # API endpoints
            'api/routes/',    # Route definitions
            'api/middleware/', # API middleware
            'utils/',         # Utility functions
            'utils/cache/',   # Caching utilities
            'utils/lazy_load/', # Lazy loading utilities
            'config/',        # Configuration
            'tests/',         # Tests
            'tests/unit/',    # Unit tests
            'tests/integration/', # Integration tests
        ]
        
        base_path = Path('.')
        for directory in optimized_dirs:
            (base_path / directory).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def organize_existing_modules():
        """
        Provides recommendations for organizing existing modules
        """
        recommendations = {
            'core': [
                'config.py',
                'settings.py',
            ],
            'database': [
                'database.py',
                'models.py',
                'migrations/',
            ],
            'security': [
                'asm/',  # All security detection modules
                'security/',
            ],
            'api': [
                'api/',
            ],
            'services': [
                'agents/',
                'services/',
            ],
            'utils': [
                'utils/',
                'shared/',
            ]
        }
        
        return recommendations


class ImportOptimizer:
    """
    Optimizes import statements and reduces startup time
    """
    
    @staticmethod
    def optimize_imports_in_file(file_path: str) -> str:
        """
        Analyzes and suggests optimization for import statements in a Python file
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic import organization
        lines = content.split('\n')
        imports = []
        non_imports = []
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                # Skip standard library imports that are fast
                if any(stripped.startswith(f'import {lib}') or stripped.startswith(f'from {lib}')
                      for lib in ['os', 'sys', 'json', 're', 'pathlib', 'typing', 'functools']):
                    non_imports.append(line)
                else:
                    imports.append(line)
            else:
                non_imports.append(line)
        
        # Sort imports by frequency and impact
        sorted_imports = sorted(imports, key=lambda x: ImportOptimizer._import_priority(x))
        
        # Combine optimized imports with non-import lines
        optimized_content = '\n'.join(sorted_imports + [''] + non_imports)
        
        return optimized_content
    
    @staticmethod
    def _import_priority(import_line: str) -> int:
        """
        Assigns priority to imports based on typical loading time
        Lower numbers are loaded first
        """
        low_priority_modules = [
            'tensorflow', 'torch', 'sklearn', 'numpy', 'pandas',
            'cv2', 'PIL', 'matplotlib', 'seaborn', 'scipy'
        ]
        
        high_priority_modules = [
            'os', 'sys', 'json', 're', 'pathlib', 'typing', 'functools'
        ]
        
        line_lower = import_line.lower()
        
        if any(mod in line_lower for mod in low_priority_modules):
            return 100  # Load last
        elif any(mod in line_lower for mod in high_priority_modules):
            return 1   # Load first
        else:
            return 50  # Default priority


# Optimized module loader that only loads what's needed
class OptimizedModuleLoader:
    """
    Optimized module loader that loads modules based on usage patterns
    """
    
    def __init__(self):
        self.loaded_modules = {}
        self.usage_stats = {}
    
    def load_if_needed(self, module_name: str, usage_context: str = 'default'):
        """
        Load a module only if needed based on context
        """
        if module_name not in self.loaded_modules:
            # Track usage
            if usage_context not in self.usage_stats:
                self.usage_stats[usage_context] = []
            self.usage_stats[usage_context].append(module_name)
            
            # Load the module
            module = importlib.import_module(module_name)
            self.loaded_modules[module_name] = module
        
        return self.loaded_modules[module_name]
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get statistics about module usage
        """
        return self.usage_stats


# Example optimized service loader
class ServiceLoader:
    """
    Optimized service loader that implements lazy loading
    """
    
    def __init__(self):
        self._services = {}
    
    def get_service(self, service_name: str, service_module: str):
        """
        Get a service, loading it only when first requested
        """
        if service_name not in self._services:
            # Import only when needed
            module = importlib.import_module(service_module)
            service_class = getattr(module, service_name)
            self._services[service_name] = service_class()
        
        return self._services[service_name]


# Singleton instance for shared use
service_loader = ServiceLoader()
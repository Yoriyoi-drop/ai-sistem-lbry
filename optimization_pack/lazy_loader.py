"""
Lazy Loading Implementation for Heavy Modules
Used to reduce startup time and memory usage by loading modules only when needed
"""
import importlib
from functools import wraps
from typing import Callable, Any


class LazyLoader:
    """
    Lazy loader class to load modules only when accessed
    """
    def __init__(self, module_name: str):
        self.module_name = module_name
        self._module = None

    def __getattr__(self, name: str) -> Any:
        if self._module is None:
            self._module = importlib.import_module(self.module_name)
        return getattr(self._module, name)


def lazy_import(module_name: str):
    """
    Decorator to create lazy imports
    """
    return LazyLoader(module_name)


def lazy_load_on_call(func: Callable) -> Callable:
    """
    Decorator to load heavy modules only when the function is called
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # This is where we would load heavy modules upon function call
        return func(*args, **kwargs)
    
    return wrapper


# Example implementations for heavy AI modules
class AILazyLoader:
    """
    Lazy loader for AI-related modules that are typically heavy
    """
    @staticmethod
    @lazy_load_on_call
    def get_ollama_client():
        """Lazy load Ollama client only when needed"""
        try:
            import ollama
            return ollama
        except ImportError:
            # Fallback implementation
            import requests
            import os

            class _OllamaClient:
                def __init__(self, host=None):
                    self.host = (host or os.getenv("OLLAMA_HOST", "http://localhost:11434")).rstrip('/')

                def list(self):
                    resp = requests.get(f"{self.host}/api/models")
                    resp.raise_for_status()
                    return resp.json()

                def chat(self, model, messages, options=None):
                    payload = {"model": model, "messages": messages}
                    if options:
                        payload["options"] = options
                    resp = requests.post(f"{self.host}/api/chat", json=payload, timeout=300)
                    resp.raise_for_status()
                    return resp.json()

            return _OllamaClient()

    @staticmethod
    @lazy_load_on_call
    def get_numpy():
        """Lazy load NumPy only when needed"""
        import numpy as np
        return np

    @staticmethod
    @lazy_load_on_call
    def get_pandas():
        """Lazy load Pandas only when needed"""
        import pandas as pd
        return pd

    @staticmethod
    @lazy_load_on_call
    def get_scikit_learn():
        """Lazy load Scikit-learn only when needed"""
        import sklearn
        return sklearn


# Example usage in the main application
def get_ai_client():
    """
    Function to get AI client with lazy loading
    """
    return AILazyLoader.get_ollama_client()


def get_ml_modules():
    """
    Function to get ML modules with lazy loading
    """
    return {
        'numpy': AILazyLoader.get_numpy(),
        'pandas': AILazyLoader.get_pandas(),
        'sklearn': AILazyLoader.get_scikit_learn()
    }
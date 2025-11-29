"""
Advanced Caching Implementation for Optimized Performance
Uses multiple caching strategies to reduce computation overhead
"""
from functools import lru_cache, wraps
from typing import Any, Callable, Optional
import hashlib
import json
import time
from datetime import datetime, timedelta
import asyncio


class CacheManager:
    """
    Advanced caching manager with multiple caching strategies
    """
    def __init__(self):
        self.memory_cache = {}
        self.expire_times = {}

    def _make_key(self, *args, **kwargs) -> str:
        """Create a unique key for cache based on arguments"""
        key_data = {
            'args': args,
            'kwargs': kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()

    def set(self, key: str, value: Any, expire_seconds: Optional[int] = None):
        """Set a value in cache with optional expiration"""
        self.memory_cache[key] = value
        
        if expire_seconds:
            expire_time = datetime.now() + timedelta(seconds=expire_seconds)
            self.expire_times[key] = expire_time
        else:
            # Remove expiration if it exists
            if key in self.expire_times:
                del self.expire_times[key]

    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache, return None if expired or not found"""
        # Check if key exists
        if key not in self.memory_cache:
            return None
        
        # Check if expired
        if key in self.expire_times:
            if datetime.now() > self.expire_times[key]:
                # Clean up expired entry
                del self.memory_cache[key]
                del self.expire_times[key]
                return None
        
        return self.memory_cache[key]

    def delete(self, key: str):
        """Delete a key from cache"""
        if key in self.memory_cache:
            del self.memory_cache[key]
        if key in self.expire_times:
            del self.expire_times[key]

    def clear(self):
        """Clear all cache"""
        self.memory_cache.clear()
        self.expire_times.clear()

    def cache_with_ttl(self, ttl_seconds: int = 300):
        """Decorator to cache function results with TTL"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                key = self._make_key(func.__name__, *args, **kwargs)
                cached_result = self.get(key)
                
                if cached_result is not None:
                    return cached_result
                
                result = await func(*args, **kwargs)
                self.set(key, result, ttl_seconds)
                return result
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                key = self._make_key(func.__name__, *args, **kwargs)
                cached_result = self.get(key)
                
                if cached_result is not None:
                    return cached_result
                
                result = func(*args, **kwargs)
                self.set(key, result, ttl_seconds)
                return result
            
            # Return appropriate wrapper based on function type
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        return decorator


# Global cache manager instance
cache_manager = CacheManager()


# LRU Cache decorators with optimized sizes
def optimized_lru_cache(maxsize: int = 128):
    """
    Optimized LRU cache decorator with custom size
    """
    def decorator(func: Callable) -> Callable:
        cached_func = lru_cache(maxsize=maxsize)(func)
        cached_func.cache_clear = lambda: cached_func.cache_clear()
        cached_func.cache_info = lambda: cached_func.cache_info()
        return cached_func
    return decorator


# Specific caching implementations for common operations
class SecurityCache:
    """
    Specialized cache for security operations
    """
    
    @staticmethod
    @optimized_lru_cache(maxsize=256)
    def sql_injection_pattern_cache(query: str) -> tuple:
        """
        Cache SQL injection detection results
        """
        # This would be the actual detection logic
        # For now, we return the hash of the query as a placeholder
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        return query_hash, time.time()

    @staticmethod
    @cache_manager.cache_with_ttl(ttl_seconds=180)  # 3 minutes TTL
    def cached_model_response(model_name: str, messages: list, options: dict = None) -> dict:
        """
        Cache AI model responses to avoid repeated expensive calls
        """
        # This would interact with the AI model
        # Return a hash-based placeholder for now
        response_hash = hashlib.sha256(str(messages).encode()).hexdigest()
        return {
            'response_hash': response_hash,
            'timestamp': time.time(),
            'model': model_name
        }


# Memory-optimized cache for frequently accessed data
class MemoryOptimizedCache:
    """
    Memory-optimized cache with size limits and eviction policy
    """
    def __init__(self, max_items: int = 1000):
        self.max_items = max_items
        self.cache = {}
        self.access_times = {}
        
    def __setitem__(self, key: str, value: Any):
        if key not in self.cache and len(self.cache) >= self.max_items:
            # Remove least recently used item
            oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        self.cache[key] = value
        self.access_times[key] = time.time()
        
    def __getitem__(self, key: str) -> Any:
        if key in self.cache:
            self.access_times[key] = time.time()  # Update access time
            return self.cache[key]
        raise KeyError(key)
        
    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: str) -> bool:
        return key in self.cache
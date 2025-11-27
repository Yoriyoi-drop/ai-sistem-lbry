"""
Caching decorators for API endpoints

Created: 2025-11-26
"""

from functools import wraps
import hashlib
import json
from typing import Callable, Optional
import logging

from .redis_client import redis_client
from .cache_keys import CacheKeys

logger = logging.getLogger(__name__)


def cache_response(expire: int = 300, key_prefix: Optional[str] = None):
    """
    Decorator to cache function responses in Redis
    
    Args:
        expire: Cache expiration time in seconds (default: 5 minutes)
        key_prefix: Optional prefix for cache key
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = _generate_cache_key(func, args, kwargs, key_prefix)
            
            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_result
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            redis_client.set(cache_key, result, expire=expire)
            logger.debug(f"Cached result for {cache_key}")
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = _generate_cache_key(func, args, kwargs, key_prefix)
            
            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            redis_client.set(cache_key, result, expire=expire)
            logger.debug(f"Cached result for {cache_key}")
            
            return result
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def invalidate_cache(*keys: str):
    """
    Decorator to invalidate cache keys after function execution
    
    Args:
        keys: Cache key patterns to invalidate
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # Invalidate cache keys
            for key in keys:
                redis_client.delete(key)
                logger.debug(f"Invalidated cache key: {key}")
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Invalidate cache keys
            for key in keys:
                redis_client.delete(key)
                logger.debug(f"Invalidated cache key: {key}")
            
            return result
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def rate_limit(max_requests: int = 100, window: int = 60):
    """
    Rate limiting decorator using Redis
    
    Args:
        max_requests: Maximum number of requests allowed
        window: Time window in seconds
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Get user identifier (from args or kwargs)
            user_id = kwargs.get('user_id') or (args[0] if args else 'anonymous')
            
            # Generate rate limit key
            rate_key = CacheKeys.rate_limit(user_id, func.__name__)
            
            # Check current count
            current_count = redis_client.get(rate_key) or 0
            
            if current_count >= max_requests:
                raise Exception(f"Rate limit exceeded: {max_requests} requests per {window} seconds")
            
            # Increment counter
            redis_client.increment(rate_key)
            
            # Set expiration on first request
            if current_count == 0:
                redis_client.expire(rate_key, window)
            
            # Execute function
            return await func(*args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Get user identifier
            user_id = kwargs.get('user_id') or (args[0] if args else 'anonymous')
            
            # Generate rate limit key
            rate_key = CacheKeys.rate_limit(user_id, func.__name__)
            
            # Check current count
            current_count = redis_client.get(rate_key) or 0
            
            if current_count >= max_requests:
                raise Exception(f"Rate limit exceeded: {max_requests} requests per {window} seconds")
            
            # Increment counter
            redis_client.increment(rate_key)
            
            # Set expiration on first request
            if current_count == 0:
                redis_client.expire(rate_key, window)
            
            # Execute function
            return func(*args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def _generate_cache_key(func: Callable, args: tuple, kwargs: dict, prefix: Optional[str] = None) -> str:
    """Generate a unique cache key for function call"""
    # Create key from function name and arguments
    key_parts = [
        prefix or func.__module__,
        func.__name__,
    ]
    
    # Add args and kwargs to key
    args_str = json.dumps(args, sort_keys=True, default=str)
    kwargs_str = json.dumps(kwargs, sort_keys=True, default=str)
    
    # Hash the arguments to keep key length manageable
    args_hash = hashlib.md5((args_str + kwargs_str).encode()).hexdigest()
    key_parts.append(args_hash)
    
    return ":".join(key_parts)


import asyncio

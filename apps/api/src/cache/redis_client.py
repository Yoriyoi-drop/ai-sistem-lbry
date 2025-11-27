"""
Redis client configuration and utilities

Created: 2025-11-26
"""

import redis
from redis import ConnectionPool
import json
import logging
from typing import Any, Optional
import os

logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_URL = os.getenv("REDIS_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")

# Create connection pool
redis_pool = ConnectionPool.from_url(
    REDIS_URL,
    password=REDIS_PASSWORD,
    max_connections=50,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_keepalive=True,
    health_check_interval=30,
)


class RedisClient:
    """Redis client wrapper with utility methods"""
    
    def __init__(self):
        self.client = redis.Redis(connection_pool=redis_pool)
    
    def ping(self) -> bool:
        """Check if Redis is available"""
        try:
            return self.client.ping()
        except redis.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            return False
    
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """
        Set a key-value pair
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            expire: Expiration time in seconds
        """
        try:
            serialized_value = json.dumps(value)
            if expire:
                return self.client.setex(key, expire, serialized_value)
            else:
                return self.client.set(key, serialized_value)
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value by key
        
        Args:
            key: Cache key
            
        Returns:
            Deserialized value or None if not found
        """
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return None
    
    def delete(self, *keys: str) -> int:
        """Delete one or more keys"""
        try:
            return self.client.delete(*keys)
        except Exception as e:
            logger.error(f"Error deleting cache keys: {e}")
            return 0
    
    def exists(self, key: str) -> bool:
        """Check if a key exists"""
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Error checking key existence: {e}")
            return False
    
    def expire(self, key: str, seconds: int) -> bool:
        """Set expiration time for a key"""
        try:
            return self.client.expire(key, seconds)
        except Exception as e:
            logger.error(f"Error setting expiration: {e}")
            return False
    
    def ttl(self, key: str) -> int:
        """Get time-to-live for a key"""
        try:
            return self.client.ttl(key)
        except Exception as e:
            logger.error(f"Error getting TTL: {e}")
            return -2
    
    def increment(self, key: str, amount: int = 1) -> int:
        """Increment a counter"""
        try:
            return self.client.incrby(key, amount)
        except Exception as e:
            logger.error(f"Error incrementing key {key}: {e}")
            return 0
    
    def decrement(self, key: str, amount: int = 1) -> int:
        """Decrement a counter"""
        try:
            return self.client.decrby(key, amount)
        except Exception as e:
            logger.error(f"Error decrementing key {key}: {e}")
            return 0
    
    def set_hash(self, name: str, mapping: dict) -> bool:
        """Set hash fields"""
        try:
            serialized_mapping = {k: json.dumps(v) for k, v in mapping.items()}
            return self.client.hset(name, mapping=serialized_mapping)
        except Exception as e:
            logger.error(f"Error setting hash {name}: {e}")
            return False
    
    def get_hash(self, name: str, key: str) -> Optional[Any]:
        """Get hash field value"""
        try:
            value = self.client.hget(name, key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting hash field: {e}")
            return None
    
    def get_all_hash(self, name: str) -> dict:
        """Get all hash fields"""
        try:
            data = self.client.hgetall(name)
            return {k: json.loads(v) for k, v in data.items()}
        except Exception as e:
            logger.error(f"Error getting all hash fields: {e}")
            return {}
    
    def publish(self, channel: str, message: Any) -> int:
        """Publish message to a channel"""
        try:
            serialized_message = json.dumps(message)
            return self.client.publish(channel, serialized_message)
        except Exception as e:
            logger.error(f"Error publishing to channel {channel}: {e}")
            return 0
    
    def flushdb(self) -> bool:
        """Flush current database (use with caution!)"""
        try:
            return self.client.flushdb()
        except Exception as e:
            logger.error(f"Error flushing database: {e}")
            return False


# Global Redis client instance
redis_client = RedisClient()


def get_redis_client() -> RedisClient:
    """Get Redis client instance"""
    return redis_client

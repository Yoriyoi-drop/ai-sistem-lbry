"""
Optimization Configuration
Contains all configuration for the optimization pack
"""
import os
from typing import Optional, Dict, Any
from pydantic import BaseSettings, Field


class OptimizationConfig(BaseSettings):
    """
    Configuration for optimization features
    """
    # Caching Configuration
    cache_enabled: bool = Field(default=True, env="CACHE_ENABLED")
    cache_ttl_seconds: int = Field(default=300, env="CACHE_TTL_SECONDS")  # 5 minutes
    cache_max_size: int = Field(default=1000, env="CACHE_MAX_SIZE")
    
    # Lazy Loading Configuration
    lazy_loading_enabled: bool = Field(default=True, env="LAZY_LOADING_ENABLED")
    lazy_modules_whitelist: list = Field(
        default_factory=lambda: os.getenv("LAZY_MODULES_WHITELIST", 
                                         "tensorflow,torch,sklearn,numpy,pandas,cv2,PIL").split(",")
    )
    
    # Memory Optimization
    memory_limit_mb: int = Field(default=1024, env="MEMORY_LIMIT_MB")
    gc_threshold_multiplier: float = Field(default=2.0, env="GC_THRESHOLD_MULTIPLIER")
    
    # Performance Optimization
    async_workers: int = Field(default=4, env="ASYNC_WORKERS")
    max_connections: int = Field(default=100, env="MAX_CONNECTIONS")
    connection_timeout: int = Field(default=30, env="CONNECTION_TIMEOUT")
    
    # Profiling Configuration
    profiling_enabled: bool = Field(default=False, env="PROFILING_ENABLED")
    profiling_output_dir: str = Field(default="profiles/", env="PROFILING_OUTPUT_DIR")
    profiling_threshold_ms: float = Field(default=100.0, env="PROFILING_THRESHOLD_MS")
    
    # Database Optimization
    db_pool_size: int = Field(default=20, env="DB_POOL_SIZE")
    db_pool_max_overflow: int = Field(default=10, env="DB_POOL_MAX_OVERFLOW")
    db_pool_recycle: int = Field(default=3600, env="DB_POOL_RECYCLE")
    
    # API Optimization
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window_seconds: int = Field(default=60, env="RATE_LIMIT_WINDOW_SECONDS")
    
    # File System Optimization
    temp_dir: str = Field(default="/tmp", env="TEMP_DIR")
    upload_chunk_size: int = Field(default=8192, env="UPLOAD_CHUNK_SIZE")  # 8KB
    
    # Security Optimization
    security_cache_ttl: int = Field(default=180, env="SECURITY_CACHE_TTL")  # 3 minutes for security results
    
    class Config:
        env_file = ".env"
        case_sensitive = False


class OptimizedSettings:
    """
    Singleton class for optimized settings with lazy initialization
    """
    _instance: Optional['OptimizedSettings'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.config = OptimizationConfig()
            self._initialized = True
    
    def get(self) -> OptimizationConfig:
        return self.config
    
    def update_from_dict(self, updates: Dict[str, Any]):
        """Update configuration values from dictionary"""
        for key, value in updates.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)


# Global instance
optimized_settings = OptimizedSettings()


# Optimization utilities
def get_optimization_config() -> OptimizationConfig:
    """Get the optimization configuration"""
    return optimized_settings.get()


def apply_memory_optimizations():
    """
    Apply memory optimization settings
    """
    import gc
    
    # Configure garbage collection
    if hasattr(gc, 'set_threshold'):
        threshold = gc.get_threshold()
        gc.set_threshold(
            int(threshold[0] * optimized_settings.config.gc_threshold_multiplier),
            int(threshold[1] * optimized_settings.config.gc_threshold_multiplier),
            int(threshold[2] * optimized_settings.config.gc_threshold_multiplier)
        )
    
    # Enable memory-efficient string operations
    os.environ['PYTHONHASHSEED'] = 'random'
    os.environ['PYTHONMALLOC'] = 'malloc'


def apply_performance_optimizations():
    """
    Apply general performance optimizations
    """
    # Optimize asyncio settings
    os.environ['PYTHONASYNCIODEBUG'] = '0'
    
    # Optimize JSON serialization
    try:
        import orjson
        # orjson is already optimized, we just ensure it's available
    except ImportError:
        pass  # Use standard json if orjson not available


def setup_optimization_environment():
    """
    Setup the entire optimization environment
    """
    # Apply memory optimizations
    apply_memory_optimizations()
    
    # Apply performance optimizations
    apply_performance_optimizations()
    
    # Ensure required directories exist
    os.makedirs(optimized_settings.config.profiling_output_dir, exist_ok=True)
    os.makedirs(optimized_settings.config.temp_dir, exist_ok=True)


# Initialize optimization environment on import
setup_optimization_environment()
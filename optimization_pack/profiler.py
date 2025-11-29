"""
Performance Profiler for Optimization
Used to identify bottlenecks and optimize performance
"""
import cProfile
import pstats
import io
import os
import time
from functools import wraps
from typing import Callable, Any, Dict
from contextlib import contextmanager
import asyncio
from .config import get_optimization_config


class PerformanceProfiler:
    """
    Advanced performance profiler for identifying bottlenecks
    """
    def __init__(self):
        self.config = get_optimization_config()
        self.profiles = {}
        self.profile_times = {}
    
    @contextmanager
    def profile_block(self, name: str):
        """
        Context manager for profiling code blocks
        """
        if not self.config.profiling_enabled:
            yield
            return
        
        start_time = time.time()
        pr = cProfile.Profile()
        pr.enable()
        
        try:
            yield
        finally:
            pr.disable()
            end_time = time.time()
            
            # Store profile data
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s)
            ps.sort_stats('cumulative')
            ps.print_stats()
            
            self.profiles[name] = s.getvalue()
            self.profile_times[name] = end_time - start_time
    
    def profile_function(self, threshold_ms: float = None):
        """
        Decorator to profile function execution
        """
        if threshold_ms is None:
            threshold_ms = self.config.profiling_threshold_ms
        
        def decorator(func: Callable) -> Callable:
            if not self.config.profiling_enabled:
                return func
            
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                pr = cProfile.Profile()
                pr.enable()
                
                try:
                    result = await func(*args, **kwargs)
                finally:
                    pr.disable()
                    end_time = time.time()
                    
                    execution_time_ms = (end_time - start_time) * 1000
                    
                    if execution_time_ms >= threshold_ms:
                        self._save_profile_data(func.__name__, pr, execution_time_ms)
                    
                return result
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = time.time()
                pr = cProfile.Profile()
                pr.enable()
                
                try:
                    result = func(*args, **kwargs)
                finally:
                    pr.disable()
                    end_time = time.time()
                    
                    execution_time_ms = (end_time - start_time) * 1000
                    
                    if execution_time_ms >= threshold_ms:
                        self._save_profile_data(func.__name__, pr, execution_time_ms)
                
                return result
            
            # Return appropriate wrapper based on function type
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator
    
    def _save_profile_data(self, func_name: str, profile: cProfile.Profile, execution_time: float):
        """
        Save profile data to file
        """
        output_dir = self.config.profiling_output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{func_name}_{int(time.time())}_{execution_time:.2f}ms.prof"
        filepath = os.path.join(output_dir, filename)
        
        # Save the profile stats
        profile.dump_stats(filepath)
        
        # Also save human-readable version
        readable_filename = f"{func_name}_{int(time.time())}_{execution_time:.2f}ms.txt"
        readable_filepath = os.path.join(output_dir, readable_filename)
        
        s = io.StringIO()
        ps = pstats.Stats(profile, stream=s)
        ps.sort_stats('cumulative')
        ps.print_stats()
        
        with open(readable_filepath, 'w') as f:
            f.write(f"Execution time: {execution_time:.2f}ms\n")
            f.write("Profile stats:\n")
            f.write(s.getvalue())
    
    def get_profile_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all profiles
        """
        return {
            'profiles': list(self.profiles.keys()),
            'profile_times': self.profile_times,
            'total_profiled_time': sum(self.profile_times.values()),
            'profiling_enabled': self.config.profiling_enabled
        }
    
    def clear_profiles(self):
        """
        Clear all stored profiles
        """
        self.profiles.clear()
        self.profile_times.clear()


# Global profiler instance
profiler = PerformanceProfiler()


# Convenience functions
def profile_code_block(name: str):
    """
    Decorator to profile a function using the block profiler
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            with profiler.profile_block(name):
                return await func(*args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            with profiler.profile_block(name):
                return func(*args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def profile_slow_functions(threshold_ms: float = None):
    """
    Decorator to profile only slow functions (above threshold)
    """
    return profiler.profile_function(threshold_ms)


@contextmanager
def time_it(operation_name: str):
    """
    Simple timing context manager
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = (time.perf_counter() - start) * 1000  # Convert to milliseconds
        if profiler.config.profiling_enabled:
            print(f"[PERFORMANCE] {operation_name} took {elapsed:.2f}ms")


# Specific profilers for common operations
class SecurityProfiler(PerformanceProfiler):
    """
    Specialized profiler for security operations
    """
    
    def profile_sql_detection(self):
        """
        Profiler specifically for SQL injection detection
        """
        return self.profile_function(threshold_ms=50.0)  # 50ms threshold for security operations
    
    def profile_ai_model_calls(self):
        """
        Profiler specifically for AI model calls
        """
        return self.profile_function(threshold_ms=500.0)  # 500ms threshold for AI calls


# Pre-configured security profiler
security_profiler = SecurityProfiler()


def get_bottleneck_report() -> str:
    """
    Generate a report of performance bottlenecks
    """
    summary = profiler.get_profile_summary()
    
    report = [
        "PERFORMANCE BOTTLENECK REPORT",
        "=" * 50,
        f"Profiling Enabled: {summary['profiling_enabled']}",
        f"Total Functions Profiled: {len(summary['profiles'])}",
        f"Total Profiled Time: {summary['total_profiled_time']:.2f}s",
        "",
        "Recommendations:"
    ]
    
    # Add recommendations based on profile data
    if summary['total_profiled_time'] > 1.0:  # More than 1 second total
        report.append("- Consider implementing more aggressive caching")
        report.append("- Review functions with highest execution times")
    
    if profiler.config.profiling_enabled:
        report.append("- Profiling is enabled, which adds overhead, consider disabling in production")
    else:
        report.append("- Profiling is disabled, enable for performance analysis")
    
    return "\n".join(report)


# Example usage function
def run_performance_analysis():
    """
    Run a comprehensive performance analysis
    """
    print("Running performance analysis...")
    print(get_bottleneck_report())
    
    # Example of profiling a simple function
    @profile_slow_functions(threshold_ms=10.0)
    def example_function():
        # Simulate some work
        time.sleep(0.02)  # 20ms work
        return "done"
    
    result = example_function()
    print(f"Example function result: {result}")
    
    return profiler.get_profile_summary()
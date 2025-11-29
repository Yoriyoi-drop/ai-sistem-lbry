"""
Performance Monitoring Utilities
Real-time monitoring of resource usage and performance metrics
"""
import psutil
import time
import threading
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
import asyncio
import json
from datetime import datetime
from .config import get_optimization_config


@dataclass
class ResourceMetrics:
    """Data class for resource metrics"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_percent: float
    network_sent_mb: float
    network_recv_mb: float
    active_threads: int
    active_connections: int


class PerformanceMonitor:
    """
    Real-time performance monitoring
    """
    def __init__(self):
        self.config = get_optimization_config()
        self.metrics_history: List[ResourceMetrics] = []
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.callbacks: List[Callable[[ResourceMetrics], None]] = []
        
    def start_monitoring(self, interval_seconds: float = 1.0):
        """Start performance monitoring in a separate thread"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_interval = interval_seconds
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
    
    def _monitor_loop(self):
        """Internal monitoring loop"""
        while self.monitoring:
            metrics = self.get_current_metrics()
            self.metrics_history.append(metrics)
            
            # Keep only last 1000 metrics to prevent memory issues
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-1000:]
            
            # Call registered callbacks
            for callback in self.callbacks:
                try:
                    callback(metrics)
                except Exception:
                    pass  # Don't let callback errors break monitoring
            
            time.sleep(self.monitor_interval)
    
    def get_current_metrics(self) -> ResourceMetrics:
        """Get current resource metrics"""
        process = psutil.Process()
        
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=None)
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        network_info = psutil.net_io_counters()
        
        # Get process-specific metrics
        process_memory = process.memory_info()
        
        return ResourceMetrics(
            timestamp=time.time(),
            cpu_percent=cpu_percent,
            memory_percent=memory_info.percent,
            memory_used_mb=process_memory.rss / 1024 / 1024,  # RSS memory for this process
            memory_available_mb=memory_info.available / 1024 / 1024,
            disk_percent=disk_info.percent,
            network_sent_mb=network_info.bytes_sent / 1024 / 1024,
            network_recv_mb=network_info.bytes_recv / 1024 / 1024,
            active_threads=threading.active_count(),
            active_connections=self._count_active_connections()
        )
    
    def _count_active_connections(self) -> int:
        """Count active network connections for this process"""
        try:
            connections = psutil.Process().connections()
            return len([conn for conn in connections if conn.status == psutil.CONN_ESTABLISHED])
        except:
            return 0
    
    def register_callback(self, callback: Callable[[ResourceMetrics], None]):
        """Register a callback to be called when new metrics are collected"""
        self.callbacks.append(callback)
    
    def get_average_metrics(self, last_n: int = 10) -> Optional[ResourceMetrics]:
        """Get average metrics from the last N measurements"""
        if not self.metrics_history:
            return None
        
        recent_metrics = self.metrics_history[-last_n:]
        if not recent_metrics:
            return None
        
        count = len(recent_metrics)
        avg_metrics = ResourceMetrics(
            timestamp=sum(m.timestamp for m in recent_metrics) / count,
            cpu_percent=sum(m.cpu_percent for m in recent_metrics) / count,
            memory_percent=sum(m.memory_percent for m in recent_metrics) / count,
            memory_used_mb=sum(m.memory_used_mb for m in recent_metrics) / count,
            memory_available_mb=sum(m.memory_available_mb for m in recent_metrics) / count,
            disk_percent=sum(m.disk_percent for m in recent_metrics) / count,
            network_sent_mb=sum(m.network_sent_mb for m in recent_metrics) / count,
            network_recv_mb=sum(m.network_recv_mb for m in recent_metrics) / count,
            active_threads=sum(m.active_threads for m in recent_metrics) / count,
            active_connections=sum(m.active_connections for m in recent_metrics) / count
        )
        
        return avg_metrics
    
    def get_peak_metrics(self) -> Optional[ResourceMetrics]:
        """Get peak metrics observed during monitoring"""
        if not self.metrics_history:
            return None
        
        # Find metrics with highest values
        peak_cpu = max(self.metrics_history, key=lambda m: m.cpu_percent)
        peak_memory = max(self.metrics_history, key=lambda m: m.memory_percent)
        peak_connections = max(self.metrics_history, key=lambda m: m.active_connections)
        
        return ResourceMetrics(
            timestamp=max(m.timestamp for m in self.metrics_history),
            cpu_percent=peak_cpu.cpu_percent,
            memory_percent=peak_memory.memory_percent,
            memory_used_mb=peak_memory.memory_used_mb,
            memory_available_mb=min(m.memory_available_mb for m in self.metrics_history),
            disk_percent=max(m.disk_percent for m in self.metrics_history),
            network_sent_mb=max(m.network_sent_mb for m in self.metrics_history),
            network_recv_mb=max(m.network_recv_mb for m in self.metrics_history),
            active_threads=max(m.active_threads for m in self.metrics_history),
            active_connections=peak_connections.active_connections
        )
    
    def get_metrics_report(self) -> Dict:
        """Get a comprehensive metrics report"""
        current = self.get_current_metrics()
        average = self.get_average_metrics()
        peak = self.get_peak_metrics()
        
        return {
            "current": {
                "timestamp": datetime.fromtimestamp(current.timestamp).isoformat(),
                "cpu_percent": current.cpu_percent,
                "memory_percent": current.memory_percent,
                "memory_used_mb": round(current.memory_used_mb, 2),
                "active_threads": current.active_threads,
                "active_connections": current.active_connections
            },
            "average": {
                "cpu_percent": round(average.cpu_percent, 2) if average else 0,
                "memory_percent": round(average.memory_percent, 2) if average else 0,
                "memory_used_mb": round(average.memory_used_mb, 2) if average else 0,
                "active_threads": average.active_threads if average else 0,
                "active_connections": average.active_connections if average else 0
            } if average else None,
            "peak": {
                "cpu_percent": peak.cpu_percent if peak else 0,
                "memory_percent": peak.memory_percent if peak else 0,
                "memory_used_mb": round(peak.memory_used_mb, 2) if peak else 0,
                "active_connections": peak.active_connections if peak else 0
            } if peak else None,
            "history_size": len(self.metrics_history)
        }


class ResourceOptimizer:
    """
    Resource optimization based on monitoring data
    """
    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
        self.config = get_optimization_config()
        self.optimization_history: List[Dict] = []
    
    def should_apply_memory_optimization(self) -> bool:
        """Check if memory optimization should be applied"""
        current = self.monitor.get_current_metrics()
        return current.memory_percent > 80.0  # High memory usage
    
    def should_reduce_workers(self) -> bool:
        """Check if worker count should be reduced"""
        current = self.monitor.get_current_metrics()
        return (current.cpu_percent > 90.0 and 
                current.active_threads > 50)  # High CPU + many threads
    
    def apply_memory_optimization(self):
        """Apply memory optimization techniques"""
        import gc
        
        # Force garbage collection
        collected = gc.collect()
        
        # Log the optimization
        self.optimization_history.append({
            "timestamp": time.time(),
            "type": "memory_optimization",
            "action": "garbage_collection",
            "collected_objects": collected
        })
    
    def adjust_worker_count(self, current_workers: int) -> int:
        """Suggest optimal worker count based on current metrics"""
        current = self.monitor.get_current_metrics()
        
        if current.cpu_percent > 90.0:
            # Reduce workers if CPU is over 90%
            return max(1, current_workers - 1)
        elif current.cpu_percent < 30.0:
            # Increase workers if CPU is under 30% and we're not at max
            return min(self.config.async_workers, current_workers + 1)
        else:
            # Keep current worker count
            return current_workers


# Global monitor instance
performance_monitor = PerformanceMonitor()


def setup_resource_monitoring():
    """Setup resource monitoring with callbacks for optimization"""
    
    def optimization_callback(metrics: ResourceMetrics):
        """Callback to apply optimizations based on metrics"""
        optimizer = ResourceOptimizer(performance_monitor)
        
        if optimizer.should_apply_memory_optimization():
            optimizer.apply_memory_optimization()
        
        if optimizer.should_reduce_workers():
            # In a real application, this would adjust worker count
            pass
    
    # Register the optimization callback
    performance_monitor.register_callback(optimization_callback)
    
    # Start monitoring
    performance_monitor.start_monitoring(interval_seconds=2.0)


# Initialize monitoring when module is loaded
setup_resource_monitoring()


def get_performance_report():
    """Get the current performance report"""
    return performance_monitor.get_metrics_report()


def stop_performance_monitoring():
    """Stop the performance monitoring"""
    performance_monitor.stop_monitoring()


# Async wrapper for monitoring in async contexts
class AsyncPerformanceMonitor:
    """
    Async wrapper for performance monitoring
    """
    def __init__(self):
        self.monitor = performance_monitor
    
    async def get_metrics_async(self) -> Dict:
        """Get metrics in an async context"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, get_performance_report)
    
    async def start_monitoring_async(self, interval_seconds: float = 1.0):
        """Start monitoring from async context"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: self.monitor.start_monitoring(interval_seconds))


# Global async monitor instance
async_performance_monitor = AsyncPerformanceMonitor()
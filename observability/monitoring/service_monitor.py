"""
Service monitoring and health checks for the Infinite AI Security Platform
"""

import asyncio
import aiohttp
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ServiceStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


@dataclass
class ServiceHealth:
    name: str
    url: str
    status: ServiceStatus
    response_time: float
    timestamp: datetime
    details: Optional[Dict] = None


class ServiceMonitor:
    def __init__(self):
        self.services = {
            'api_gateway': 'http://localhost:8000/health',
            'ai_hub': 'http://localhost:8001/health', 
            'scanner': 'http://localhost:8080/health',
            'labyrinth': 'http://localhost:8081/health',
        }
        self.logger = logging.getLogger(__name__)
    
    async def check_service_health(self, name: str, url: str) -> ServiceHealth:
        """Check health of a single service"""
        start_time = datetime.now()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    response_time = (datetime.now() - start_time).total_seconds()
                    response_data = await response.json()
                    
                    status = ServiceStatus.HEALTHY if response.status == 200 else ServiceStatus.UNHEALTHY
                    
                    return ServiceHealth(
                        name=name,
                        url=url,
                        status=status,
                        response_time=response_time,
                        timestamp=start_time,
                        details=response_data
                    )
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Health check failed for {name}: {str(e)}")
            return ServiceHealth(
                name=name,
                url=url,
                status=ServiceStatus.UNHEALTHY,
                response_time=response_time,
                timestamp=start_time,
                details={"error": str(e)}
            )
    
    async def check_all_services(self) -> List[ServiceHealth]:
        """Check health of all services concurrently"""
        tasks = [
            self.check_service_health(name, url) 
            for name, url in self.services.items()
        ]
        results = await asyncio.gather(*tasks)
        return results
    
    async def get_platform_health_status(self) -> Dict:
        """Get overall platform health status"""
        service_healths = await self.check_all_services()
        
        healthy_count = sum(1 for sh in service_healths if sh.status == ServiceStatus.HEALTHY)
        total_count = len(service_healths)
        
        overall_status = ServiceStatus.HEALTHY
        if healthy_count == 0:
            overall_status = ServiceStatus.UNHEALTHY
        elif healthy_count < total_count:
            overall_status = ServiceStatus.DEGRADED
        
        return {
            "status": overall_status.value,
            "timestamp": datetime.now().isoformat(),
            "services_overview": {
                sh.name: {
                    "status": sh.status.value,
                    "response_time": sh.response_time,
                    "details": sh.details
                } for sh in service_healths
            },
            "summary": {
                "total_services": total_count,
                "healthy_services": healthy_count,
                "unhealthy_services": total_count - healthy_count
            }
        }


# Singleton instance
service_monitor = ServiceMonitor()


async def get_platform_health():
    """Get platform health - can be used in API endpoints"""
    return await service_monitor.get_platform_health_status()


# Example usage in main application
async def run_health_monitoring():
    """Run continuous health monitoring"""
    while True:
        health_status = await service_monitor.get_platform_health_status()
        print(f"Platform Health: {health_status['status']}")
        
        for service_name, service_info in health_status['services_overview'].items():
            print(f"  {service_name}: {service_info['status']} ({service_info['response_time']:.2f}s)")
        
        await asyncio.sleep(30)  # Check every 30 seconds


if __name__ == "__main__":
    asyncio.run(run_health_monitoring())
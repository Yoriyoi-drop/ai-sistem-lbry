"""
Client for communicating with the Rust Labyrinth Security Engine
"""
import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from ..config.config import settings


logger = logging.getLogger(__name__)


class LabyrinthClient:
    """
    Client for interacting with the Rust-based Infinite Labyrinth Security Engine
    """
    
    def __init__(self):
        self.base_url = settings.LABYRINTH_RUST_URL
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
            
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
        
    async def analyze_threat(self, payload: str, source_ip: str = "127.0.0.1") -> Dict[str, Any]:
        """
        Analyze a potential threat using the Rust Labyrinth engine
        
        Args:
            payload: The data/packet to analyze for threats
            source_ip: The source IP address of the request
            
        Returns:
            Dict containing threat analysis results
        """
        session = await self.get_session()
        
        try:
            # Prepare the request to the Rust engine
            url = f"{self.base_url}/analyze"
            data = {
                "payload": payload,
                "source_ip": source_ip,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Sending threat analysis request to Rust engine: {url}")
            
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Threat analysis completed: {result.get('severity', 'Unknown')} threat detected")
                    return result
                else:
                    error_text = await response.text()
                    logger.error(f"Rust engine analysis failed with status {response.status}: {error_text}")
                    raise Exception(f"Rust engine analysis failed: {response.status} - {error_text}")
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error when connecting to Rust engine: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error during threat analysis: {str(e)}")
            raise
            
    async def get_threat_statistics(self) -> Dict[str, Any]:
        """
        Get threat statistics from the Rust Labyrinth engine
        
        Returns:
            Dict containing threat statistics and performance metrics
        """
        session = await self.get_session()
        
        try:
            url = f"{self.base_url}/stats"
            
            logger.info(f"Fetching threat statistics from Rust engine: {url}")
            
            async with session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info("Successfully retrieved threat statistics")
                    return result
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to get statistics: {response.status} - {error_text}")
                    raise Exception(f"Failed to get statistics: {response.status}")
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error when connecting to Rust engine: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error getting threat statistics: {str(e)}")
            raise
            
    async def health_check(self) -> bool:
        """
        Check if the Rust Labyrinth engine is healthy and responding
        
        Returns:
            True if the engine is healthy, False otherwise
        """
        session = await self.get_session()
        
        try:
            # The Rust server responds to any request, so we'll use a basic GET
            url = f"{self.base_url}/stats"  # Use stats endpoint as it's implemented
            
            async with session.get(url) as response:
                # If we get any response, consider it healthy
                is_healthy = response.status == 200
                logger.info(f"Rust engine health check: {'Healthy' if is_healthy else 'Unhealthy'}")
                return is_healthy
                
        except Exception as e:
            logger.error(f"Rust engine health check failed: {str(e)}")
            return False


# Global instance for convenience
labyrinth_client = LabyrinthClient()
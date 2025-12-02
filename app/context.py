"""
App Context Module
Central application context for managing configuration and services
"""
from typing import Dict, Any, Optional
import logging
from datetime import datetime


class AppContext:
    """
    Central application context holding shared resources and configuration
    """
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)
        self.services: Dict[str, Any] = {}
        self.agents: Dict[str, Any] = {}
        self.cache: Optional[Any] = None
        self.database: Optional[Any] = None
        self.security_engine = None
        self.initialized = False
        
        self.logger.info("AppContext initialized")

    def initialize(self, config: Dict[str, Any]):
        """
        Initialize the application context with configuration
        """
        self.config = config
        self.initialized = True
        
        self.logger.info(f"AppContext initialized with config at {datetime.utcnow().isoformat()}")
        
        # Initialize services based on config
        self._initialize_services()
    
    def _initialize_services(self):
        """
        Initialize services based on configuration
        """
        from src.services.auth_service import AuthenticationService
        from src.services.organization_service import OrganizationService
        from src.services.tier_service import TierService
        from src.services.billing_service import StripeBillingService
        from src.services.usage_tracking_service import UsageTrackingService
        
        # Initialize core services
        self.services["auth"] = AuthenticationService(None)  # DB session will be injected per request
        self.services["organization"] = OrganizationService(None)
        self.services["tier"] = TierService(None)
        self.services["billing"] = StripeBillingService(None)
        self.services["usage_tracking"] = UsageTrackingService(None)
        
        self.logger.info("Core services initialized")
    
    def register_agent(self, name: str, agent_instance: Any):
        """
        Register an agent in the context
        """
        self.agents[name] = agent_instance
        self.logger.info(f"Agent {name} registered")
    
    def get_service(self, service_name: str) -> Optional[Any]:
        """
        Get a service by name
        """
        return self.services.get(service_name)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key
        """
        return self.config.get(key, default)
    
    def set_config(self, key: str, value: Any):
        """
        Set configuration value
        """
        self.config[key] = value
    
    def is_initialized(self) -> bool:
        """
        Check if app context is initialized
        """
        return self.initialized


# Global app context instance
app_context = AppContext()
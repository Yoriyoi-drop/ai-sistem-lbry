"""
Cache key definitions and utilities

Created: 2025-11-26
"""


class CacheKeys:
    """Centralized cache key definitions"""
    
    # Prefixes
    USER_PREFIX = "user"
    AGENT_PREFIX = "agent"
    SCAN_PREFIX = "scan"
    THREAT_PREFIX = "threat"
    SESSION_PREFIX = "session"
    RATE_LIMIT_PREFIX = "ratelimit"
    
    # TTL values (in seconds)
    TTL_SHORT = 60  # 1 minute
    TTL_MEDIUM = 300  # 5 minutes
    TTL_LONG = 3600  # 1 hour
    TTL_DAY = 86400  # 24 hours
    
    @staticmethod
    def user(user_id: int) -> str:
        """Cache key for user data"""
        return f"{CacheKeys.USER_PREFIX}:{user_id}"
    
    @staticmethod
    def user_profile(user_id: int) -> str:
        """Cache key for user profile"""
        return f"{CacheKeys.USER_PREFIX}:{user_id}:profile"
    
    @staticmethod
    def user_permissions(user_id: int) -> str:
        """Cache key for user permissions"""
        return f"{CacheKeys.USER_PREFIX}:{user_id}:permissions"
    
    @staticmethod
    def agent(agent_id: int) -> str:
        """Cache key for agent data"""
        return f"{CacheKeys.AGENT_PREFIX}:{agent_id}"
    
    @staticmethod
    def agent_list(user_id: int) -> str:
        """Cache key for user's agent list"""
        return f"{CacheKeys.USER_PREFIX}:{user_id}:agents"
    
    @staticmethod
    def agent_status(agent_id: int) -> str:
        """Cache key for agent status"""
        return f"{CacheKeys.AGENT_PREFIX}:{agent_id}:status"
    
    @staticmethod
    def scan(scan_id: int) -> str:
        """Cache key for scan data"""
        return f"{CacheKeys.SCAN_PREFIX}:{scan_id}"
    
    @staticmethod
    def scan_results(scan_id: int) -> str:
        """Cache key for scan results"""
        return f"{CacheKeys.SCAN_PREFIX}:{scan_id}:results"
    
    @staticmethod
    def scan_list(user_id: int, page: int = 1) -> str:
        """Cache key for user's scan list"""
        return f"{CacheKeys.USER_PREFIX}:{user_id}:scans:page:{page}"
    
    @staticmethod
    def threat_analysis(threat_id: int) -> str:
        """Cache key for threat analysis"""
        return f"{CacheKeys.THREAT_PREFIX}:{threat_id}:analysis"
    
    @staticmethod
    def session(session_id: str) -> str:
        """Cache key for user session"""
        return f"{CacheKeys.SESSION_PREFIX}:{session_id}"
    
    @staticmethod
    def api_key(api_key: str) -> str:
        """Cache key for API key validation"""
        return f"apikey:{api_key}"
    
    @staticmethod
    def rate_limit(user_id: int, endpoint: str) -> str:
        """Cache key for rate limiting"""
        return f"{CacheKeys.RATE_LIMIT_PREFIX}:{user_id}:{endpoint}"
    
    @staticmethod
    def security_stats(user_id: int) -> str:
        """Cache key for security statistics"""
        return f"{CacheKeys.USER_PREFIX}:{user_id}:stats:security"
    
    @staticmethod
    def dashboard_data(user_id: int) -> str:
        """Cache key for dashboard data"""
        return f"{CacheKeys.USER_PREFIX}:{user_id}:dashboard"
    
    @staticmethod
    def websocket_connection(connection_id: str) -> str:
        """Cache key for WebSocket connection"""
        return f"ws:{connection_id}"
    
    @staticmethod
    def temporary(key: str) -> str:
        """Cache key for temporary data"""
        return f"temp:{key}"

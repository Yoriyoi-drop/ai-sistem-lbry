"""
Rate limiting utility for Infinite AI Security Platform
"""
import time
from collections import defaultdict, deque
from typing import Dict
import threading


class RateLimiter:
    def __init__(self, requests_per_minute: int = 60, window_seconds: int = 60):
        """
        Initialize rate limiter
        :param requests_per_minute: Max requests per window
        :param window_seconds: Time window in seconds
        """
        self.requests_per_window = requests_per_minute
        self.window_seconds = window_seconds
        self.requests = defaultdict(deque)
        self.lock = threading.Lock()

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request from identifier is allowed
        :param identifier: Unique identifier (IP, user ID, etc.)
        :return: True if request is allowed, False otherwise
        """
        with self.lock:
            now = time.time()
            # Remove old requests outside the window
            while (self.requests[identifier] and 
                   now - self.requests[identifier][0] > self.window_seconds):
                self.requests[identifier].popleft()
            
            # Check if we're under the limit
            if len(self.requests[identifier]) < self.requests_per_window:
                self.requests[identifier].append(now)
                return True
            
            return False

    def get_remaining_requests(self, identifier: str) -> int:
        """
        Get number of remaining requests for identifier
        :param identifier: Unique identifier
        :return: Number of remaining requests
        """
        with self.lock:
            now = time.time()
            # Remove old requests outside the window
            while (self.requests[identifier] and 
                   now - self.requests[identifier][0] > self.window_seconds):
                self.requests[identifier].popleft()
            
            return self.requests_per_window - len(self.requests[identifier])

    def get_reset_time(self, identifier: str) -> float:
        """
        Get time when rate limit will reset for identifier
        :param identifier: Unique identifier
        :return: Unix timestamp for reset time
        """
        with self.lock:
            if not self.requests[identifier]:
                return time.time()
            
            oldest_request = self.requests[identifier][0]
            return oldest_request + self.window_seconds


class SlidingWindowRateLimiter:
    """
    Sliding window rate limiter implementation
    """
    def __init__(self):
        self.clients = {}
        self.lock = threading.Lock()

    def is_allowed(self, client_id: str, max_requests: int, window_ms: int) -> bool:
        """
        Check if request is allowed based on sliding window
        """
        with self.lock:
            now = time.time() * 1000  # Convert to milliseconds
            if client_id not in self.clients:
                self.clients[client_id] = deque()
            
            requests = self.clients[client_id]
            
            # Remove requests outside the window
            while requests and now - requests[0] > window_ms:
                requests.popleft()
            
            # Check if we're under the limit
            if len(requests) < max_requests:
                requests.append(now)
                return True
            
            return False


# Global rate limiter instance
default_rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """
    Get the default rate limiter instance
    """
    return default_rate_limiter
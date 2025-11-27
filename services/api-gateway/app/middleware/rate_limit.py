"""
Rate Limit Middleware
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from redis import Redis
import time
import os
import json

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_host: str = "localhost", redis_port: int = 6379,
                 redis_db: int = 0, default_limit: int = 100, window_size: int = 3600):
        super().__init__(app)
        self.redis_client = Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
        self.default_limit = default_limit
        self.window_size = window_size

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host

        # Create rate limit key
        key = f"rate_limit:{client_ip}"

        # Get current time
        current_time = int(time.time())
        window_start = current_time - (current_time % self.window_size)
        window_end = window_start + self.window_size

        # Use Redis to track requests
        try:
            # Create pipeline to execute multiple commands atomically
            pipe = self.redis_client.pipeline()

            # Check if key exists and get its value
            pipe.get(key)
            pipe.expireat(key, window_end)
            results = pipe.execute()

            current_requests = int(results[0]) if results[0] else 0

            # Check if limit is exceeded
            if current_requests >= self.default_limit:
                return JSONResponse(
                    status_code=429,
                    content={"error": "Rate limit exceeded", "retry_after": window_end - current_time}
                )

            # Increment request count
            self.redis_client.incr(key)

            # Set expiration for the key if it's a new key
            if current_requests == 0:
                self.redis_client.expireat(key, window_end)

        except Exception as e:
            # If Redis is unavailable, log the error and continue (fail open)
            print(f"Rate limiting failed: {str(e)}")

        response = await call_next(request)
        return response

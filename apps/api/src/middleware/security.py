"""
Security middleware for Infinite AI Security Platform
"""
import time
import json
from typing import Callable, Awaitable
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from ..utils.rate_limiter import RateLimiter


class SecurityMiddleware:
    def __init__(self, app):
        self.app = app
        self.rate_limiter = RateLimiter()

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        
        # Get client IP address
        client_ip = self.get_client_ip(request)
        
        # Rate limiting
        if not self.rate_limiter.is_allowed(client_ip):
            response = JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded"}
            )
            await response(scope, receive, send)
            return
        
        # Add security headers
        async def security_handler(receive, send):
            response_started = False
            
            async def send_with_security_headers(message):
                nonlocal response_started
                if message["type"] == "http.response.start":
                    # Add security headers to response
                    headers = [(k.lower(), v) for k, v in message.get("headers", [])]
                    headers.extend([
                        (b"X-Content-Type-Options", b"nosniff"),
                        (b"X-Frame-Options", b"DENY"),
                        (b"X-XSS-Protection", b"1; mode=block"),
                        (b"Strict-Transport-Security", b"max-age=31536000; includeSubDomains"),
                        (b"Content-Security-Policy", b"default-src 'self'"),
                    ])
                    message["headers"] = headers
                elif message["type"] == "http.response.body" and not response_started:
                    response_started = True
                
                await send(message)
            
            await self.app(scope, receive, send_with_security_headers)
        
        await security_handler(receive, send)

    def get_client_ip(self, request: Request) -> str:
        """Get client IP address from request"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host


class TimingMiddleware:
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        start_time = time.time()
        
        async def timing_send(response):
            if response["type"] == "http.response.start":
                response_time = time.time() - start_time
                response["headers"] = [
                    *response.get("headers", []),
                    (b"X-Response-Time", str(response_time).encode())
                ]
            await send(response)
        
        await self.app(scope, receive, timing_send)


class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        start_time = time.time()

        async def logging_send(response):
            nonlocal start_time
            if response["type"] == "http.response.start":
                duration = time.time() - start_time
                status_code = response["status"]
                
                # Log request information
                print(f"REQUEST: {request.method} {request.url.path} "
                      f"- Status: {status_code} - Duration: {duration:.3f}s "
                      f"- IP: {self.get_client_ip(request)}")
            
            await send(response)

        await self.app(scope, receive, logging_send)

    def get_client_ip(self, request: Request) -> str:
        """Get client IP address from request"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host


def add_security_middleware(app):
    """Add security middleware to the application"""
    app.add_middleware(SecurityMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(LoggingMiddleware)
    return app
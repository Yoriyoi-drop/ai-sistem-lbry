"""
Auth Middleware
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from jose import jwt, JWTError
import os
from typing import Optional

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key: str = None, algorithm: str = "HS256"):
        super().__init__(app)
        self.secret_key = secret_key or os.getenv("JWT_SECRET_KEY")  # No default to force environment variable
        if not self.secret_key:
            raise ValueError("JWT_SECRET_KEY environment variable must be set")
        self.algorithm = algorithm

    async def dispatch(self, request: Request, call_next):
        # Define public endpoints that don't require authentication
        public_paths = ["/", "/health", "/docs", "/redoc", "/openapi.json"]

        if request.url.path in public_paths:
            response = await call_next(request)
            return response

        # Get token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"error": "Authorization header missing or invalid"}
            )

        token = auth_header[7:]  # Remove "Bearer " prefix

        try:
            # Decode the JWT token
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # Add user info to request state for use in endpoints
            request.state.user = payload

        except JWTError as e:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid or expired token", "details": str(e)}
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"error": "Authentication error", "details": str(e)}
            )

        response = await call_next(request)
        return response

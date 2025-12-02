"""
Main API Application
Comprehensive FastAPI application with modular routes
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import os
from datetime import datetime

from api.routers import users, security
from api.dependencies.security import get_current_user, rate_limit_dependency


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    # Startup
    print(f"🚀 Infinite AI Security Platform starting up at {datetime.now()}")
    
    # Initialize any required services here
    # For example: database connections, external services, etc.
    
    yield
    
    # Shutdown
    print(f"🛑 Infinite AI Security Platform shutting down at {datetime.now()}")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Infinite AI Security Platform API",
    description="Enterprise AI Security Platform with real-time threat detection",
    version="2.0.0",  # Updated version to reflect major architectural improvements
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost,http://localhost:3000,http://localhost:8000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # In production, be more restrictive with origins
)

# Include API routers
app.include_router(users.router, prefix="/api/v1")
app.include_router(security.router, prefix="/api/v1")

# Add more routers as needed
# app.include_router(organizations.router, prefix="/api/v1")
# app.include_router(scans.router, prefix="/api/v1")
# app.include_router(billing.router, prefix="/api/v1")
# app.include_router(agents.router, prefix="/api/v1")


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Infinite AI Security Platform API",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/v1/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Welcome to Infinite AI Security Platform API v2.0",
        "description": "Enterprise AI Security Platform with multi-agent intelligence and labyrinth defense",
        "version": "2.0.0",
        "endpoints": [
            "/api/docs - Interactive API documentation",
            "/api/redoc - Alternative API documentation", 
            "/api/health - Health check",
            "/api/v1/users - User management",
            "/api/v1/security - Security analysis"
        ],
        "security_features": [
            "Prompt Injection Detection",
            "Jailbreak Attempt Prevention", 
            "Malicious Code Detection",
            "Sensitive Data Protection",
            "Multi-Agent Orchestration",
            "Labyrinth Defense Mechanism"
        ]
    }


@app.get("/api/v1/profile", dependencies=[Depends(get_current_user)])
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user profile
    """
    return {
        "user_info": current_user,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/v1/rate-limit", dependencies=[Depends(rate_limit_dependency(10, 60))])
async def get_rate_limit(current_user: dict = Depends(get_current_user)):
    """
    Get current rate limit information
    """
    from api.dependencies.security import get_rate_limit_info
    rate_info = get_rate_limit_info(current_user)
    return rate_info


# Error handlers
@app.exception_handler(429)
async def rate_limit_handler(request, exc):
    """
    Handle rate limit exceeded errors
    """
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "error": "Rate limit exceeded",
            "detail": "Too many requests, please try again later",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(401)
async def unauthorized_handler(request, exc):
    """
    Handle unauthorized access errors
    """
    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "error": "Unauthorized",
            "detail": "Authentication credentials were not provided or are invalid",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """
    Handle internal server errors
    """
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
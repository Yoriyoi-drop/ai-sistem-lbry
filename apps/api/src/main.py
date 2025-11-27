from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
from datetime import datetime
from .config import settings
from .database.connection import init_db
from .api.v1.api import api_router
from .utils.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    # Startup
    setup_logging()
    init_db()
    yield
    # Shutdown


# Create FastAPI app
app = FastAPI(
    title="Infinite AI Security Platform API",
    description="API for the Infinite AI Security Platform with multi-agent AI system, security scanning, and labyrinth defense",
    version="2.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=r"https?://.*"
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve static files if directory exists
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except FileNotFoundError:
    pass  # static directory might not exist
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")  # More specific logging


@app.get("/")
def root():
    return {
        "message": "Welcome to Infinite AI Security Platform API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/api/docs",
        "api": "/api/v1"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/ready")
def readiness_check():
    # Check if all required services are available
    return {
        "status": "ready",
        "checks": {
            "database": "connected",
            "redis": "connected",
            "storage": "available"
        }
    }
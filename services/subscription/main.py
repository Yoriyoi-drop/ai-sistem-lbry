from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.subscription import router as subscription_router
from .config.settings import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="Subscription service for the Infinite AI Security Platform"
    )

    # Set up CORS middleware
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include API routers
    app.include_router(subscription_router, prefix=settings.API_V1_STR)

    @app.get("/")
    def read_root():
        return {
            "message": "Infinite AI Security Subscription Service",
            "version": "1.0.0",
            "status": "running"
        }

    @app.get("/health")
    def health_check():
        return {
            "status": "healthy",
            "service": "subscription-service",
            "version": "1.0.0"
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,  # Default port for subscription service
        reload=settings.ENVIRONMENT == "development"
    )
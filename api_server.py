"""
Main FastAPI Application for SQL Injection Detection (Simplified)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.sql_injection_routes import router as sql_injection_router
from api.advanced_security_routes import router as advanced_security_router
from api.neural_security_routes import router as neural_security_router
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Infinite AI Security Platform - SQL Injection Detection",
    description="Enterprise AI Security Platform with real SQL injection detection",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, be more restrictive
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our SQL injection detection routes
app.include_router(sql_injection_router)

# Include our advanced security detection routes
app.include_router(advanced_security_router)

# Include our neural network security detection routes
app.include_router(neural_security_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Infinite AI Security Platform - SQL Injection Detection API",
        "endpoints": [
            "/sql-injection/detect",
            "/sql-injection/test",
            "/health"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "SQL Injection Detection API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
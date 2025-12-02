#!/usr/bin/env python3
"""
Infinite AI Security Platform - Startup Script
Production-ready startup script for the B2B SaaS platform
"""
import os
import sys
import subprocess
import signal
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

def check_environment():
    """Check if required environment variables are set"""
    required_vars = [
        "API_SECRET_KEY",
        "JWT_SECRET_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing required environment variables: {', '.join(missing_vars)}")
        print("   Please set them in .env file or environment")
        print("   Using development defaults...")
        
        # Set development defaults
        os.environ["API_SECRET_KEY"] = "dev-super-secret-key-change-in-production"
        os.environ["JWT_SECRET_KEY"] = "dev-jwt-secret-key-change-in-production"
        os.environ["API_DEBUG"] = "true"

def start_server():
    """Start the FastAPI server"""
    try:
        import uvicorn
        from api.main import app
        
        # Get port from environment or use default
        port = int(os.getenv("API_PORT", "8000"))
        host = os.getenv("API_HOST", "0.0.0.0")
        
        print(f"🚀 Starting Infinite AI Security Platform on {host}:{port}")
        print(f"   API Documentation: http://{host}:{port}/api/docs")
        print(f"   Health Check: http://{host}:{port}/api/health")
        print(f"   Base API: http://{host}:{port}/api/v1/")
        print("-" * 60)
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level=os.getenv("LOG_LEVEL", "info"),
            reload=os.getenv("API_DEBUG", "false").lower() == "true"
        )
        
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("   Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    print("🔐 Infinite AI Security Platform - B2B SaaS")
    print("   Enterprise AI Security with Multi-Agent Intelligence")
    print("   and Labyrinth Defense Mechanism")
    print()
    
    # Check environment variables
    check_environment()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
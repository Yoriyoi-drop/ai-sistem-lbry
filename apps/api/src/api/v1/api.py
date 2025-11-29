from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .agents import router as agents_router
from .scans import router as scans_router
from .health import router as health_router
from .security_scans import router as security_router
from .advanced_security import router as advanced_security_router
from .neural_security import router as neural_security_router


api_router = APIRouter()

# Include all API routers
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(agents_router, prefix="/agents", tags=["Agents"])
api_router.include_router(scans_router, prefix="/scans", tags=["Scans"])
api_router.include_router(security_router, prefix="", tags=["Security Scans"])
api_router.include_router(advanced_security_router, prefix="", tags=["Advanced Security Scans"])
api_router.include_router(neural_security_router, prefix="", tags=["Neural Security"])
api_router.include_router(health_router, prefix="/health", tags=["Health"])
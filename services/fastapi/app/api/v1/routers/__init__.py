# FastAPI
from fastapi import APIRouter

# Routers
from .home.router import router as home_router
from .users.router import router as auth_router

# Statics
from .home.router import STATIC_DIR as home_static_dir

router = APIRouter()

# Include routers
router.include_router(home_router, tags=["Página de Bienvenida"])
router.include_router(auth_router, prefix="/users", tags=["Usuarios"])

# Export the router
__all__ = ["router", "home_static_dir"]
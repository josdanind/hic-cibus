# FastAPI
from fastapi import APIRouter

# Routers
from .home.router import router as home_router

# Statics
from .home.router import STATIC_DIR as home_static_dir

router = APIRouter()

# Include routers
router.include_router(home_router, tags=["home"])

# Export the router
__all__ = ["router", "home_static_dir"]
# FastAPI
from fastapi import APIRouter

# Routers
from .home.router import router as home_router

# Inicialización del router principal
router = APIRouter()

# Inclusión de rutas en el router principal
router.include_router(home_router, tags=["Home"])

# Definición de los elementos exportados desde este módulo
__all__ = ["router", "home_static_dir"]
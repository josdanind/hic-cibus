# FastAPI
from fastapi import APIRouter

# Routers
from .home.router import router as home_router
from .crud.router import router as crud_auth_router

# Directorios estáticos
from .home.router import STATIC_DIR as home_static_dir

# Inicialización del router principal
router = APIRouter()

# Inclusión de rutas en el router principal
router.include_router(home_router, tags=["Página de Bienvenida"])
router.include_router(crud_auth_router, prefix="/crud_user", tags=["Usuarios CRUD"])

# Definición de los elementos exportados desde este módulo
__all__ = ["router", "home_static_dir"]
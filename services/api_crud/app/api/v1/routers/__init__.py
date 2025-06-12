# FastAPI
from fastapi import APIRouter

# Routers
from .home.router import router as home_router
from .crud.router import router as crud_auth_router
from .mqtt.router import router as mqtt_router
from .bots.router import router as bots_router

# Directorios estáticos
from .home.router import STATIC_DIR as home_static_dir

# Inicialización del router principal
router = APIRouter()

# Inclusión de rutas en el router principal
router.include_router(home_router, tags=["Página de Bienvenida"])
router.include_router(crud_auth_router, prefix="/crud_user", tags=["Usuarios CRUD"])
router.include_router(mqtt_router, prefix="/mqtt_user", tags=["Broker MQTT"])
router.include_router(bots_router, prefix="/bots", tags=["Bots de Telegram"])

# Definición de los elementos exportados desde este módulo
__all__ = ["router", "home_static_dir"]
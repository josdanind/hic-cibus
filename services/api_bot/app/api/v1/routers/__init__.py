# FastAPI
from fastapi import APIRouter

# Routers
from .home.router import router as home_router
from .telegram_webhook import router as telegram_webhook_router

# Inicialización del router principal
router = APIRouter()

# Inclusión de rutas en el router principal
router.include_router(home_router, tags=["Home"])
router.include_router(telegram_webhook_router, tags=["Telegram API"])

# Definición de los elementos exportados desde este módulo
__all__ = ["router", "home_static_dir"]
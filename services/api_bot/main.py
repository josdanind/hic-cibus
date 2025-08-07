"""
📌 Punto de entrada de la aplicación FastAPI para el bot Tlaloc.

Este módulo configura y lanza la aplicación principal:
- Gestiona el ciclo de vida (startup y shutdown).
- Inicializa servicios externos como Valkey y Ngrok.
- Define y registra los routers.
- Establece el webhook del bot de Telegram.
"""

# ─────────────────────────────
# 📦 IMPORTACIONES
# ─────────────────────────────
# 🐍 Librería estándar
from contextlib import asynccontextmanager
from typing import Final

# 🧩 Terceros
from fastapi import FastAPI

# 🏗️  Módulos internos de la aplicación
from app.api.v1.routers import router
from app.core.ngrok_service import init_ngrok, close_ngrok
from app.core.config import settings
from app.database import (
    init_token_cache,
    get_valkey,
    close_valkey
)
from app.TheaterHandler import theater_handler

# ─────────────────────────────
# ⚙️ METADATOS DE LA APP
# ─────────────────────────────
APP_TITLE: Final[str] = "Tlaloc Bot"
APP_DESC:  Final[str] = "Bot de Monitorización"
APP_VER:   Final[str] = "0.1.0"

# ─────────────────────────────
# 🔄 CICLO DE VIDA
# ─────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona la fase de ARRANQUE y APAGADO de la aplicación."""
    # ──────── ARRANQUE ────────
    # 1. Conexión Valkey
    app.state.valkey = await get_valkey()

    # 2. Precarga de token
    await init_token_cache()

    # 3. Determina la URL que usará el bot
    if settings.DEVELOPMENT_MODE:
        api_bot_url = init_ngrok(settings.NGROK_TOKEN)
    else:
        api_bot_url = settings.API_DOMAIN

    # 4. Establece el webhook
    await theater_handler.set_webhook(
        f"{api_bot_url}/webhook",
        secret_token=settings.TELEGRAM_SECRET_TOKEN
    )

    yield

    # ──────── APAGADO ────────
    # 1. Cierra Ngrok (si existía)
    if settings.DEVELOPMENT_MODE:
        close_ngrok()

    # 2. Elimina el webhook del bot
    await theater_handler.delete_webhook()

    # 3. Desconexión Valkey
    await close_valkey()



# ─────────────────────────────
# 🚀 FACTORY DE LA APLICACIÓN
# ─────────────────────────────
def create_app() -> FastAPI:
    """Devuelve una instancia configurada de FastAPI."""
    app = FastAPI(
        title=APP_TITLE,
        description=APP_DESC,
        version=APP_VER,
        lifespan=lifespan
    )
    app.include_router(router)
    return app

# Instancia global para ejecución con `uvicorn main:app`
app: Final[FastAPI] = create_app()
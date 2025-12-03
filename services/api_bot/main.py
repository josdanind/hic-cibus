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
from app.TheaterHandler import theater_handler_context
from app.TheaterHandler.handlers import register_commands

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
    # 1. Valkey (singleton por proceso)
    valkey_client = await get_valkey()

    # 2. Precarga de token
    await init_token_cache(valkey_client)

    # 3. Construye el TheaterHandler
    async with theater_handler_context(
        valkey_client=valkey_client,
    ) as theater_handler:
        app.state.theater_handler = theater_handler
        app.state.valkey = valkey_client

        # 4. Registra handlers
        register_commands(app.state.theater_handler)

        # 5. Determina la URL que usará el bot
        api_bot_url = (
            init_ngrok(settings.NGROK_TOKEN)
            if settings.DEVELOPMENT_MODE else
            settings.API_DOMAIN
        )

        # 6. Setea el webhook
        await app.state.theater_handler.set_webhook(
            f"{api_bot_url}/webhook",
            secret_token=settings.TELEGRAM_SECRET_TOKEN
        )

        try:
            # ⬇️ A partir de aquí FastAPI empieza a atender requests
            yield
        finally:
            # ──────── APAGADO ────────
            # 1. Quitar webhook
            try:
                await app.state.theater_handler.delete_webhook()
            except Exception:
                pass # evita que un fallo en Telegram bloquee el cierre

            # 2. Cerrar Ngrok
            if settings.DEVELOPMENT_MODE:
                try:
                    close_ngrok()
                except Exception:
                    pass # evita que un fallo en Ngrok bloquee el cierre

            # 3. Cerrar Valkey
            try:
                await close_valkey()
            except Exception:
                pass # evita que un fallo en Valkey bloquee el cierre


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
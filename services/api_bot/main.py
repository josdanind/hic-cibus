"""
Punto de entrada de la aplicación FastAPI.
Gestiona el ciclo de vida (startup/shutdown) y registra los routers.
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
from app.database import (
    init_token_cache,
    get_valkey,
    close_valkey
)

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
    """Arranca Valkey, precarga el token y cierra recursos al apagar."""
    app.state.valkey = await get_valkey()
    await init_token_cache()
    yield
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
# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería estándar
from typing import Final

# 🧩 Terceros
import aiohttp
import redis.asyncio as aioredis
import redis.exceptions as redis_exceptions

# 🏗️  Módulos internos de la aplicación
from app.core.security import fetch_crud_token
from app.utils.rich_format import print_success_message
import app.database.valkey as valkey_db

# ──────────────────────────────
# 🔖 CONSTANTES
# ──────────────────────────────
TOKEN_KEY: Final[str] = "api_crud_token"

# ──────────────────────────────
# 🗄️  VALKEY HELPERS
# ──────────────────────────────
async def get_valkey() -> aioredis.Redis:
    """Retorna la instancia singleton de Valkey"""
    return await valkey_db.get_valkey()


async def store_token(token: str) -> None:
    """Guarda la versión hasheada del token en Valkey"""
    await (await get_valkey()).set(TOKEN_KEY, token)

close_valkey = valkey_db.close_valkey

# ──────────────────────────────
# 🚀  START-UP
# ──────────────────────────────
async def init_token_cache() -> None:
    """
    Descarga el token desde el CRUD y lo guarda en Valkey.

    Lanza mensaje de éxito o error con Rich.
    Ideal para ejecutarse en el evento `startup` o `lifespan` de FastAPI.
    """
    try:
        token = await fetch_crud_token()
        await store_token(token)
    except aiohttp.ClientResponseError as e:
        print_success_message(
            message=f"Error HTTP {e.status} al obtener el token: {e.message}",
            success=False
        )
    except redis_exceptions.RedisError as e:
        print_success_message(
            message=f"No se pudo guardar el token en Valkey",
            success=False
        )

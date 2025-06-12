# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Terceros
from fastapi import Request
import redis.asyncio as aioredis
import app.database.valkey as valkey_db

async def get_valkey_client(request: Request) -> aioredis.Redis:
    """
    Obtiene el cliente Valkey desde el estado de la aplicación.

    Args:
        request (Request): La solicitud actual.

    Returns:
        valkey_client: El cliente Valkey.
    """
    valkey_client = getattr(request.app.state, 'valkey', None)

    if valkey_client is None:
        raise RuntimeError("Cliente de Valkey no inicializado.")

    return valkey_client

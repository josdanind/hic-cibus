"""Conexión singleton a Valkey (Redis)."""

from __future__ import annotations

# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Librerías de terceros
import redis.asyncio as aioredis

# 🏗️  Módulos internos de la aplicación
from app.core.config import settings
from app.utils.rich_format import print_panel, print_success_message

# ────────────────────────────────
# ⚙️  Configuración
# ────────────────────────────────
_POOL_KWARGS: dict[str, str | int | bool] = {
    "host": settings.VALKEY_HOST,
    "port": settings.VALKEY_PORT,
    "password": settings.VALKEY_PASSWORD,
    "decode_responses": True,  # convierte bytes → str
}

valkey_client: aioredis.Redis | None = None

async def get_valkey() -> aioredis.Redis:
    """
    Devuelve un cliente Valkey *singleton*.

    ✅ Crea la conexión la primera vez que se invoca
    🔁 La reutiliza en llamadas posteriores
    """
    global valkey_client

    if valkey_client is None:
        valkey_client = aioredis.Redis(**_POOL_KWARGS)

        try:
            await valkey_client.ping()
        except Exception as exc:  # noqa: BLE001
            await close_valkey()
            raise ConnectionError("No se pudo conectar a Valkey") from exc

        _print_status("Conectado")

    return valkey_client


async def close_valkey() -> None:
    """Cierra el cliente Valkey y libera recursos."""
    global valkey_client

    if valkey_client is not None:
        await valkey_client.close()
        valkey_client = None
        _print_status("Desconectado")

# ────────────────────────────────
# 🖨️  Utilidades internas
# ────────────────────────────────
def _print_status(state: str) -> None:
    """Muestra un panel con el estado de la conexión usando Rich."""
    print_panel(
        title="🔑 Conexión a Valkey",
        messages=[
            ("Host", _POOL_KWARGS["host"]),
            ("Puerto", _POOL_KWARGS["port"]),
            ("Estado", state),
        ],
        style="check arrow"
    )
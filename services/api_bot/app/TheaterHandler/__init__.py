# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería estándar
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from typing import Any

# 🧩 Terceros
import redis.asyncio as aioredis

# 🏗️  Módulos internos de la app
from app.core.config import settings
from app.database import get_valkey
from app.libraries.TheaterHandler import TheaterHandler, APIClient

@asynccontextmanager
async def theater_handler_context(
    valkey_client: aioredis.Redis,
    parse_mode: str | None = None,
):
    token = await valkey_client.get("api_crud_token")

    async with APIClient(
        base_url=settings.API_CRUD_URL,
        headers={"Authorization": f"Bearer {token}"},
    ) as api_client:
        kwargs: dict[str, Any] = {
            "bot_name": settings.TELEGRAM_BOT_NAME,
            "bot_token": settings.TELEGRAM_BOT_TOKEN,
            "api_client": api_client,
            "valkey_client": valkey_client,
        }

        if parse_mode is not None:
            kwargs["parse_mode"] = parse_mode

        theater_handler = TheaterHandler(**kwargs)

        await theater_handler.load_companies()

        try:
            yield theater_handler
        finally:
            pass


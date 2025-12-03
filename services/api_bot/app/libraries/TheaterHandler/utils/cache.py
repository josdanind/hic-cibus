# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería estándar
from typing import Any, TypeAlias
import json

# 🧩 Terceros
import redis.asyncio as aioredis

JSONScalar: TypeAlias = str | int | float | bool | None
JSONValue:  TypeAlias = JSONScalar | list["JSONValue"] | dict[str, "JSONValue"]

class ValkeyCache:
    def __init__(self, client: aioredis.Redis) -> None:
        self.client = client

    # ---------- Booleans ---------
    async def set_bool(
        self, key: str, value: bool, *, ttl_s: int | None = None
    ) -> None:
        await self.client.set(
            name=key,
            value="1" if value else "0",
            ex= ttl_s
        )

    async def get_bool(
        self, key: str, *, default: bool = False
    ) -> bool:
        raw = await self.client.get(key)
        if raw is None:
            return default
        if isinstance(raw, (bytes, bytearray)):
            raw = raw.decode()

        return raw == "1"

    # ---------- JSON ----------
    async def set_json(
        self, key: str, obj: JSONValue, *, ttl_s: int | None = None
    )-> None:
        payload = json.dumps(
            obj,
            ensure_ascii=False,
            separators=(",",":")
        )

        await self.client.set(key, payload)

    async def get_json(self, key:str)-> JSONValue | None:
        raw = await self.client.get(key)
        if raw is None:
            return None
        if isinstance(raw, (bytes, bytearray)):
            raw = raw.decode()

        return json.loads(raw)
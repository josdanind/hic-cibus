# ─────────────────
# 📦 Importaciones
# ─────────────────
from typing import Type
from pydantic import BaseModel, field_validator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine


class DatabaseConfig(BaseModel):
    models: dict[str, Type[SQLModel]]
    engine: AsyncEngine

    @field_validator("engine")
    @classmethod
    def engine_must_be_async(cls, v: AsyncEngine):
        if not isinstance(v, AsyncEngine):
            raise TypeError(
                f"'engine' debe ser sqlalchemy.ext.asyncio.AsyncEngine, "
                f"recibido {type(v).__name__}"
            )
        return v

    model_config = {
        'arbitrary_types_allowed': True
    }

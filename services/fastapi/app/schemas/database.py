# ─────────────────
# 📦 Importaciones
# ─────────────────
from typing import Type
from pydantic import BaseModel, field_validator
from sqlmodel import SQLModel
from sqlalchemy.engine import Engine


class DatabaseConfig(BaseModel):
    models: dict[str, Type[SQLModel]]
    engine: Engine

    @field_validator('engine')
    @classmethod
    def check_engine_instance(cls, v: Engine) -> Engine:
        if not isinstance(v, Engine):
            raise TypeError(
                f"Invalid type for 'engine': expected sqlalchemy.engine.Engine, got {type(v).__name__}"
            )
        return v

    model_config = {
        'arbitrary_types_allowed': True
    }

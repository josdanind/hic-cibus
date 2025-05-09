# ─────────────────
# 📦 Importaciones
# ─────────────────
# Librería Estándar
from typing import Type

# Librerías de terceros
from pydantic import BaseModel, PrivateAttr
from sqlmodel import SQLModel
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)


class DatabaseConfig(BaseModel):
    db_url: str
    models: dict[str, Type[SQLModel]]
    metadata: MetaData

    _engine: AsyncEngine = PrivateAttr()
    _session: async_sessionmaker[AsyncSession] = PrivateAttr()

    def model_post_init(self, __context):
        self._engine = create_async_engine(self.db_url, echo=False)
        self._session = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session(self) -> async_sessionmaker[AsyncSession]:
        return self._session

    model_config = {
        'arbitrary_types_allowed': True,
        "extra": "forbid"
    }

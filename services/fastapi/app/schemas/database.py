# ─────────────────
# 📦 Importaciones
# ─────────────────
# Librería Estándar
from typing import Type, TypeVar, Generic

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

T_ModelCollection = TypeVar('T_ModelCollection')

class DatabaseConfig(BaseModel, Generic[T_ModelCollection]):
    db_url: str
    models: Type[T_ModelCollection]
    # models: dict[str, Type[SQLModel]]
    metadata: MetaData

    _engine: AsyncEngine = PrivateAttr()
    _session_factory: async_sessionmaker[AsyncSession] = PrivateAttr()

    def model_post_init(self, __context):
        self._engine = create_async_engine(self.db_url, echo=False)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

    model_config = {
        'arbitrary_types_allowed': True,
        "extra": "forbid"
    }

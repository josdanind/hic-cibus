# Habilita anotaciones de tipo diferido para evitar problemas de dependencias circulares.
from __future__ import annotations

# Librería estándar
from datetime import datetime

# ORMs
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSON

# Modelos Mixins
from app.database.models.mixins import TimestampMixin

# 1. BotCredential
class BotCredential(SQLModel, TimestampMixin, table=True):
    """
    Credenciales de autenticación de un Bot.
    """
    __tablename__ = "bot_credentials"

    # Campos de identificación
    id: int | None = Field(default=None, primary_key=True)

    # Campos de autenticación
    hashed_password: str = Field(max_length=255)
    hashed_telegram_bot_token: str | None = Field(default=None, max_length=255)
    hashed_api_access_token: str | None = Field(default=None, max_length=255)

    # Relaciones
    bot_id: int | None = Field(
        foreign_key="bots.id",
        unique=True,
        ondelete="CASCADE"
    )
    bot: Bot | None = Relationship(
        back_populates="credentials",
        sa_relationship_kwargs={"uselist": False}
    )

# 2. BotModelStatus
class BotModelStatus(SQLModel, table=True):
    """
    Representa el estado de un modelo de bot (Activo, En desarrollo, Obsoleto, Experimental, etc.).
    """
    __tablename__ = "bot_model_statuses"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: str | None = Field(default=None)

    # Relaciones
    bot_models: list[BotModel] = Relationship(
        back_populates="status",
        passive_deletes="all"
    )

# 3. BotModel
class BotModel(SQLModel, TimestampMixin, table=True):
    """
    Representa un modelo de bot (Tlaloc V1.0, Quetzalcoatl V2.0, etc.).
    """
    __tablename__ = "bot_models"

    # Campos de identificación
    id: int | None = Field(default=None, primary_key=True)

    # Campos de información
    name: str = Field(unique=True, index=True)
    description: str | None = Field(default=None)
    version: str = Field(max_length=50)

    # Relación con `BotModelStatus` (Cada modelo tiene un único estado)
    status_id: int | None = Field(
        default=None,
        foreign_key="bot_model_statuses.id",
        ondelete="SET NULL"
    )
    status: BotModelStatus = Relationship(back_populates="bot_models")

    # Relación con `Bot` (Cada modelo tiene varios bots)
    bots: list[Bot] = Relationship(
        back_populates="bot_model",
        passive_deletes="all"
    )

# 4. BotStatus
class BotStatus(SQLModel, table=True):
    """
    Representa el estado de un bot (Operativo, En mantenimiento, Apagado, En espera, etc.).
    """
    __tablename__ = "bot_statuses"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=50, nullable=False, index=True)
    description: str | None = Field(default=None)

    # Relaciones
    bots: list[Bot] = Relationship(
        back_populates="status",
        passive_deletes="all"
    )

# 5. BotEnvironment
class BotEnvironment(SQLModel, table=True):
    """
    Representa el entorno en el que corre un bot (Producción, Desarrollo, Staging, etc.).
    """
    __tablename__ = "bot_environments"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, nullable=False, max_length=50)
    description: str | None = Field(default=None)

    # Relaciones
    bots: list[Bot] = Relationship(
        back_populates="environment",
        passive_deletes="all"
    )

# 6. BotCategoryLink
class BotCategoryLink(SQLModel, TimestampMixin, table=True):
    """
    Tabla de enlace entre Bots y Categorías.
    """
    __tablename__ = "bot_category_link"

    # Campos de enlace
    bot_id: int | None = Field(
        default=None,
        foreign_key="bots.id",
        primary_key=True
    )
    category_id: int | None = Field(
        default=None,
        foreign_key="bot_categories.id",
        primary_key=True
    )

# 7. BotCategory
class BotCategory(SQLModel, table=True):
    """
    Categoría de un Bot.
    """
    __tablename__ = "bot_categories"

    # Campos de identificación
    id: int | None = Field(default=None, primary_key=True)

    # Campos de la categoría
    name: str = Field(unique=True, index=True)
    description: str | None = Field(default=None)

    # Relaciones
    bots: list[Bot] = Relationship(
        back_populates="categories",
        link_model=BotCategoryLink
    )

# 8. Bot (requiere categorías, modelos, entornos, etc.)
class Bot(SQLModel, TimestampMixin, table=True):
    """
    Representa un Bot que utiliza credenciales para autenticación.

    📌 Ejemplo:
    - Bot de monitoreo de cultivos
    - Bot de análisis financiero
    - Bot de atención al cliente
    """
    __tablename__ = "bots"

    # Campos de identificación
    id: int | None = Field(default=None, primary_key=True)

    # Campos de información
    name: str = Field(index=True, max_length=50)
    description: str | None = Field(default=None)
    api_url: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    last_ping: datetime | None = Field(default=None)
    request_per_minute: int = Field(default=0)
    data: dict | None = Field(default=None, sa_column=Column(JSON))

    # Relaciones con BotCredential (Cada bot tiene un único conjunto de credenciales)
    credentials: BotCredential | None = Relationship(
        back_populates="bot",
        cascade_delete=True,
        sa_relationship_kwargs={"uselist": False}
    )

    # Relación con `BotModel` (Cada bot tiene un único modelo)
    bot_model_id: int | None = Field(
        default=None,
        foreign_key="bot_models.id",
        ondelete="SET NULL"
    )
    bot_model: BotModel = Relationship(back_populates="bots")

    # Relación con `BotStatus` (Cada bot tiene un único estado)
    status_id: int | None = Field(
        default=None,
        foreign_key="bot_statuses.id",
        ondelete="SET NULL"
    )
    status: BotStatus = Relationship(back_populates="bots")

    # Relación con `BotEnvironment` (Cada bot corre en un único entorno)
    environment_id: int | None = Field(
        default=None,
        foreign_key="bot_environments.id"
    )
    environment: BotEnvironment = Relationship(back_populates="bots")

    # Relación con `BotCategory` (Cada bot puede tener varias categorías)
    categories: list[BotCategory] = Relationship(
        back_populates="bots",
        link_model=BotCategoryLink
    )


# Librería estándar
from datetime import datetime
from typing import Optional

# ORMs
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import func, MetaData
from sqlalchemy.orm import registry

metadata = MetaData()
mqtt_users_db_registry = registry()

class MqttUsersDB_Base(SQLModel, registry=mqtt_users_db_registry, metadata=metadata):
    """Clase base para los modelos de la base de datos 'mqtt_users_db'."""
    __abstract__ = True

class MqttUser(MqttUsersDB_Base, table=True):
    __tablename__ = "mqtt_user"
    metadata = metadata

    # 🔑 Identificador único
    id: int = Field(default=None, primary_key=True)

    username: str = Field(unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    salt: str = Field(nullable=False)
    is_superuser: bool = Field(default=False)
    created: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}
    )

# Librería estándar
from datetime import datetime
from typing import Optional

# ORMs
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import func, MetaData

metadata = MetaData()

class MqttUser(SQLModel, table=True):
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

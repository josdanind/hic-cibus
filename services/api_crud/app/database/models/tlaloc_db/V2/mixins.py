# mixins.py
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func

class TimestampMixin(SQLModel):
    __abstract__ = True

    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),   # lo genera la BD en INSERT
        ),
        description="Fecha de creación (set por la BD).",
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),   # valor inicial
        ),
        description="Última actualización (trigger en BD).",
    )

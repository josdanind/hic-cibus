# Librería estándar
from datetime import datetime, timezone

# ORMs
from sqlmodel import SQLModel, Field

class TimestampMixin:
    """ Mixin para añadir campos de timestamp a los modelos."""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

"""
🗄️ Configuración de las bases de datos del sistema
"""
# ─────────────────
# 📦 Importaciones
# ─────────────────
# Variables de entorno
from app.core.config import settings

# Schemas
from app.schemas.database import DatabaseConfig as DatabaseConfigSchema

# ────────────────────────────────────────────────
# 🗄️ Modelos de la base de datos
# ────────────────────────────────────────────────
# Autenticación de Bots
from app.database.models.bot_auth_db import models as bot_auth_models
from app.database.models.bot_auth_db import metadata as bot_auth_metadata

# Autenticación de Usuarios
from app.database.models.user_auth_db import models as user_auth_models
from app.database.models.user_auth_db import metadata as user_auth_metadata

# ───────────────────────────────────────────────────
# 🗄️ Configuración de las bases de datos del sistema
# ───────────────────────────────────────────────────
# Configuración de las bases de datos del sistema.
# Cada clave representa una base de datos y contiene:
# - metadata: metadatos de la base de datos.
# - models: modelos SQLModel asociados.
# - db_url: URL de la base de datos (postgresql+asyncpg://...).

DATABASES: dict[str, DatabaseConfigSchema] = {
    "bot_auth_db": DatabaseConfigSchema(
        db_url=settings.BOT_AUTH_DB_URL,
        models=bot_auth_models,
        metadata=bot_auth_metadata,
    ),
    "user_auth_db": DatabaseConfigSchema(
        db_url=settings.USER_AUTH_DB_URL,
        models=user_auth_models,
        metadata=user_auth_metadata,
    )
}
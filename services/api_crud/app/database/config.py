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
# Autenticación de Usuarios
from app.database.models.crud_users_db import metadata as user_auth_metadata

# Autenticación de Usuarios MQTT
from app.database.models.mqtt_users_db import metadata as mqtt_auth_metadata

# Autenticación de Bots
from app.database.models.tlaloc_db import metadata as bot_auth_metadata

# ───────────────────────────────────────────────────
# 🗄️ Configuración de las bases de datos del sistema
# ───────────────────────────────────────────────────
# Configuración de las bases de datos del sistema.
# Cada clave representa una base de datos y contiene:
# - metadata: metadatos de la base de datos.
# - models: modelos SQLModel asociados.
# - db_url: URL de la base de datos (postgresql+asyncpg://...).

crud_users_db_name = settings.CRUD_USERS_DB_NAME
mqtt_users_db_name = settings.MQTT_USERS_DB_NAME
tlaloc_db_name = settings.TLALOC_DB_NAME

DATABASES: dict[str, DatabaseConfigSchema] = {
    f"{crud_users_db_name}": DatabaseConfigSchema(
        db_url=settings.CRUD_USERS_DB_URL,
        metadata=user_auth_metadata,
    ),
    f"{mqtt_users_db_name}": DatabaseConfigSchema(
        db_url=settings.MQTT_USERS_DB_URL,
        metadata=mqtt_auth_metadata,
    ),
    f"{tlaloc_db_name}": DatabaseConfigSchema(
        db_url=settings.TLALOC_DB_URL,
        metadata=bot_auth_metadata,
    ),
}
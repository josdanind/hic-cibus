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
from app.database.models.bot_auth_db import metadata as bot_auth_metadata
from app.database.models.bot_auth_db import BotModelTypes

# Autenticación de Usuarios
from app.database.models.user_auth_db import metadata as user_auth_metadata
from app.database.models.user_auth_db import CrudModelTypes

# Autenticación de Usuarios MQTT
from app.database.models.mqtt_auth_db import metadata as mqtt_auth_metadata
from app.database.models.mqtt_auth_db import MqttModelTypes

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
        models=BotModelTypes,
        metadata=bot_auth_metadata,
    ),
    "user_auth_db": DatabaseConfigSchema(
        db_url=settings.USER_AUTH_DB_URL,
        models=CrudModelTypes,
        metadata=user_auth_metadata,
    ),
    "mqtt_auth_db": DatabaseConfigSchema(
        db_url=settings.MQTT_USER_AUTH_DB_URL,
        models=MqttModelTypes,
        metadata=mqtt_auth_metadata,
    )
}
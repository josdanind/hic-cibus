"""
📂 databases.py

Este módulo configura las conexiones a las bases de datos del sistema y define
el procedimiento para inicializar sus tablas, utilizando los modelos definidos
con SQLModel. Además, muestra un resumen visual de la inicialización en consola
usando la librería Rich a través del módulo rich_format.
"""

# ─────────────────
# 📦 Importaciones
# ─────────────────
# Librerías estándar
from typing import AsyncGenerator

# Variables de entorno
from app.core.config import settings

# Schemas
from app.schemas.database import DatabaseConfig as DatabaseConfigSchema

# Librerías de terceros
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Utilidades de la app
from app.utils.rich_format import print_panel

# ────────────────────────────────────────────────
# 🗄️ Modelos de la base de datos
# ────────────────────────────────────────────────
# dockerAutenticación de Bots
from app.database.models.bot_auth_db import models as bot_auth_models
from app.database.models.bot_auth_db import metadata as bot_auth_metadata

# Autenticación de Usuarios
from app.database.models.user_auth_db import models as user_auth_models
from app.database.models.user_auth_db import metadata as user_auth_metadata

# ────────────────────────────────────────────────
# 🛠️ Utilidades para configuración de motores DB
# ────────────────────────────────────────────────
def create_async_db_engine(db_url: str, echo: bool = True):
    """Crea una instancia de motor SQLModel asincrónico."""
    return create_async_engine(db_url, echo=echo)

# ───────────────────────────────────────────────────
# 🗄️ Configuración de las bases de datos del sistema
# ───────────────────────────────────────────────────
# Configuración de las bases de datos del sistema.
# Cada clave representa una base de datos y contiene:
# - models: modelos SQLModel asociados.
# - engine: motor de conexión a la base de datos.
# - metadata: metadatos de la base de datos.
DATABASES: dict[str, DatabaseConfigSchema] = {
    "bot_auth_db": DatabaseConfigSchema(
        models=bot_auth_models,
        engine=create_async_db_engine(settings.BOT_AUTH_DB_URL),
        metadata=bot_auth_metadata,
    ),
    "user_auth_db": DatabaseConfigSchema(
        models=user_auth_models,
        engine=create_async_db_engine(settings.USER_AUTH_DB_URL),
        metadata=user_auth_metadata,
    ),
}

# ────────────────────────────────────────
# 🚀 Inicialización de las bases de datos
# ────────────────────────────────────────
async def initialize_databases(databases: dict[str, DatabaseConfigSchema] = DATABASES) -> None:
    """
    Inicializa las tablas de todas las bases de datos definidas.

    Este procedimiento recorre cada configuración de base de datos definida en `DATABASES`,
    extrae los modelos registrados y crea sus tablas en la base de datos correspondiente si
    aún no existen.

    Además, imprime un resumen visual en la consola con la lista de bases de datos
    inicializadas y sus URL de conexión utilizando la librería Rich.

    Args:
        databases (dict[str, DatabaseConfigSchema], opcional): Diccionario de configuraciones
        de bases de datos. Por defecto, se usa `DATABASES`.

    Returns:
        None
    """
    messages = []

    # Inicialización de la base de datos
    for db_name, config in databases.items():
        engine = config.engine
        metadata = config.metadata

        async with engine.begin() as conn:
            await conn.run_sync(
                lambda sync_conn: metadata.create_all(
                    sync_conn
                )
            )

        messages.append((db_name, str(engine.url)))

    if messages:
        print_panel(
            title="Bases de datos inicializadas",
            messages=messages,
            style="check arrow",
        )


# ─────────────────────────────────────────────
# 🗄️ Sesiones de base de datos
# ─────────────────────────────────────────────
SESSIONS = {
    "bot_auth_db": async_sessionmaker(
        bind=DATABASES["bot_auth_db"].engine,
        class_=AsyncSession,
        expire_on_commit=False,
    ),
    "user_auth_db": async_sessionmaker(
        bind=DATABASES["user_auth_db"].engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
}

async def get_bot_auth_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Sesión asincrónica para la base de datos 'bot_auth_db'
    """
    async with SESSIONS["bot_auth_db"]() as session:
        yield session

async def get_user_auth_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Sesión asincrónica para la base de datos 'user_auth_db'
    """
    async with SESSIONS["user_auth_db"]() as session:
        yield session
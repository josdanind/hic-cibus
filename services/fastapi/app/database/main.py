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

# 🧩 Librerías de terceros
from sqlmodel.ext.asyncio.session import AsyncSession

# 🧱 Modelos y esquemas
from app.database.models.user_auth_db.v1.models import UserAuthEmployee
from app.schemas.database import DatabaseConfig as DatabaseConfigSchema

# 🛠️ Utilidades, librerías y configuraciones
from app.utils.rich_format import print_panel
from app.core.config import settings
from app.libraries.CRUDManager import CRUDManager
from .config import DATABASES


# ─────────────────────────────
# 🧭 Instancia de gestores CRUD
# ─────────────────────────────
user_auth_crud = CRUDManager(DATABASES["user_auth_db"].session)
bot_auth_crud = CRUDManager(DATABASES["bot_auth_db"].session)


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
        engine = config._engine
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
async def get_bot_auth_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Sesión asincrónica para la base de datos 'bot_auth_db'
    """
    async with DATABASES["bot_auth_db"].session() as session:
        yield session

async def get_user_auth_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Sesión asincrónica para la base de datos 'user_auth_db'
    """
    async with DATABASES["user_auth_db"].session() as session:
        yield session


# ───────────────────────────────────────────────────
# 👤 Crea usuario administrador
# ───────────────────────────────────────────────────
async def create_crud_user():
    employee_model = UserAuthEmployee(
        telegram_username = settings.TELEGRAM_USERNAME,
        first_name = settings.FIRST_NAME,
        last_name = settings.LAST_NAME,
        mobile_phone = settings.MOBILE_PHONE,
        email = settings.EMAIL
    )

    print(employee_model)
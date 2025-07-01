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
from typing import AsyncGenerator, Callable

# 🧩 Librerías de terceros
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

# 🧱 Modelos y esquemas
from app.schemas.database import DatabaseConfig as DatabaseConfigSchema
from app.schemas.crud_user import CrudUserInDB as CrudUserInDBSchema

# 🏗️  Módulos internos de la aplicación
from app.utils.rich_format import print_panel
from app.core.config import settings
from app.core.security import generate_bcrypt_hash
from app.libraries.CRUDManager import CRUDManager
from .config import DATABASES

# 🧱 Modelos y esquemas
from .models.user_auth_db import (
    UserAuthEmployee as EmployeeModel,
    UserAuthCrudUser as CrudUserModel
)
from .models.mqtt_auth_db import MqttUser as MqttUserModel

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

# ──────────────────────────────
# 🧭 Instancias de gestores CRUD
# ──────────────────────────────
def make_session_dep(
    session_factory: Callable[[], AsyncSession],
) -> Callable[[], AsyncGenerator[AsyncSession, None]]:
    """
    Crea una dependencia FastAPI que
    - usa session_factory() para abrir una sesión
    - hace yield de AsyncSession
    - cierra/rollback al finalizar
    """
    async def _get_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    return _get_session

get_bot_auth_session = make_session_dep(DATABASES["bot_auth_db"].session_factory)
get_user_auth_session = make_session_dep(DATABASES["user_auth_db"].session_factory)
get_mqtt_session = make_session_dep(DATABASES["mqtt_auth_db"].session_factory)

def get_bot_crud (
    session: AsyncSession = Depends(get_bot_auth_session)
) -> CRUDManager:
    return CRUDManager(session)

def get_user_crud (
    session: AsyncSession = Depends(get_user_auth_session)
) -> CRUDManager:
    return CRUDManager(session)

def get_mqtt_crud(
    session: AsyncSession = Depends(get_mqtt_session)
) -> CRUDManager:
    return CRUDManager(session)

# ───────────────────────────────────────────────────
# 👤 Crea usuario administrador
# ───────────────────────────────────────────────────
async def create_crud_user():
    """
    Crea el usuario administrador por defecto si no existe.
    """
    # Obtener referencias a la sesión y los modelos
    user_db = DATABASES["user_auth_db"]
    session_factory = user_db.session_factory

    async with session_factory() as session:
        crud_manager = CRUDManager(session)

        # Datos del usuario administrativo por defecto
        employee_model = EmployeeModel(
            telegram_username = settings.TELEGRAM_USERNAME,
            first_name = settings.FIRST_NAME,
            last_name = settings.LAST_NAME,
            mobile_phone = settings.MOBILE_PHONE,
            email = settings.EMAIL
        )

        if await crud_manager.get(
            EmployeeModel,
            {"telegram_username": employee_model.telegram_username},
            single_result=True
        ):
            return

        # Crear registro de empleado
        employee = await crud_manager.add(employee_model)

        crud_user_model = CrudUserModel(
            ** CrudUserInDBSchema(
                password=settings.PASSWORD,
                employee_id=employee.id,
                access_role_id=4
            ).model_dump(by_alias=True)
        )

        user = await crud_manager.add(crud_user_model)

        print_panel(
            title="Registros creados en user_auth_db",
            messages=[
                (
                    EmployeeModel.__tablename__,
                    f"id: {employee.id}, telegram_username: {employee.telegram_username}",
                ),
                (
                    CrudUserModel.__tablename__,
                    f"id: {user.id}",
                ),
            ],
            style="check arrow",
        )

# ───────────────────────────────────────────────────
# 👤 Crea usuario MQTT
# ───────────────────────────────────────────────────
async def create_mqtt_user():
    """
    Crea el usuario mqtt por defecto si no existe.
    """
    mqtt_db = DATABASES["mqtt_auth_db"]
    session_factory = mqtt_db.session_factory
    # MqttUserModel = mqtt_db.models.User

    async with session_factory() as session:
        crud_manager = CRUDManager(session)
        password_hash = generate_bcrypt_hash(settings.MQTT_USER_PASSWORD)

        # Datos del usuario mqtt
        mqtt_user_model = MqttUserModel(
            username = settings.MQTT_USER,
            password_hash = password_hash,
            salt = " ",
            is_superuser = True
        )

        if await crud_manager.get(
            MqttUserModel,
            {"username": mqtt_user_model.username},
            single_result=True
        ):
            return

        user = await crud_manager.add(mqtt_user_model)

        print_panel(
            title="Registros creados en mqtt_auth_db",
            messages=[
                (
                    MqttUserModel.__tablename__,
                    f"id: {user.id}, username: {user.username}",
                )
            ],
            style="check arrow",
        )
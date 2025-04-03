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
# Variables de entorno
from app.core.config import settings

# Schemas
from app.schemas.database import DatabaseConfig as DatabaseConfigSchema

# Librerías de terceros
from sqlmodel import create_engine, SQLModel

# Modelos
from app.database.models.bot_auth_db import models as bot_auth_models

# Utilidades de la app
from app.utils.rich_format import print_panel

# ────────────────────────────────────────────────
# 🛠️ Utilidades para configuración de motores DB
# ────────────────────────────────────────────────

def create_db_engine(db_url: str, echo: bool = True):
    """Crea una instancia de motor SQLModel."""
    return create_engine(db_url, echo=echo)

# ───────────────────────────────────────────────────
# 🗄️ Configuración de las bases de datos del sistema
# ───────────────────────────────────────────────────

# Configuración de las bases de datos del sistema.
# Cada clave representa una base de datos y contiene:
# - models: modelos SQLModel asociados.
# - engine: motor de conexión a la base de datos.
DATABASES: dict[str, DatabaseConfigSchema] = {
    "bot_auth_db": DatabaseConfigSchema(
        models=bot_auth_models,
        engine=create_db_engine(settings.BOT_AUTH_DB_URL),
    ),
}

# ────────────────────────────────────────
# 🚀 Inicialización de las bases de datos
# ────────────────────────────────────────

def initialize_databases(databases: dict[str, DatabaseConfigSchema] = DATABASES) -> None:
    """
    Inicializa todas las bases de datos definidas y crea sus tablas si aún no existen.

    Este procedimiento recorre cada entrada del diccionario `databases`, accede al motor
    de conexión y a la lista de tablas asociadas, y crea las estructuras necesarias en
    la base de datos correspondiente.

    También imprime un resumen visual en consola usando Rich.

    Args:
        databases (dict): Diccionario con la configuración de las bases de datos.
            Cada entrada debe tener la siguiente estructura:
                {
                    "nombre_base_datos": {
                        "tables": List[Table],  # Tablas derivadas de modelos SQLModel
                        "engine": Engine        # Instancia del motor de conexión
                    },
                    ...
                }

    Returns:
        None
    """
    messages = []

    # Inicialización de la base de datos
    for db_name, config in databases.items():
        tables = [model.__table__ for model in config.models.values()]
        SQLModel.metadata.create_all(config.engine, tables=tables)

        messages.append((db_name, str(config.engine.url)))

    if messages:
        print_panel(
            title="Bases de datos inicializadas",
            messages=messages,
            style="check arrow",
        )

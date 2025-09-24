# Librería estándar
from decimal import Decimal
from typing import Optional, Any
from datetime import datetime

# ORMs
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (
    MetaData,
    Column,
    text,
    UniqueConstraint,
    DateTime,
    func
)
from sqlalchemy.orm import registry
from pydantic import model_validator, ConfigDict

# Validadores
from .validators import (
    CodeStr,
    NameStr,
    VersionStr,
    PhoneE164Str,
    EmailStr,
    HashedStr,
    MacAddressStr,
    MqttTopicStr
)

metadata = MetaData()
tlaloc_db_registry = registry()

class TlalocDB_Base(SQLModel, registry=tlaloc_db_registry, metadata=metadata):
    """Clase base para los modelos de la base de datos 'tlaloc_db'."""
    __abstract__ = True

    # 🔧 Pydantic v2: permite tipos arbitrarios (Mapped[...]) y lectura desde ORM
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
    )


#  ╭──────────────────────────────────────────────────────╮
#  │ 📚 1. Tablas de enlaces (relaciones muchos-a-muchos) │
#  ╰──────────────────────────────────────────────────────╯
# ---------------------------------------------------------------------------
# 1. 🔗 employee_role_links
# ---------------------------------------------------------------------------
class EmployeeRoleLink(TlalocDB_Base, table=True):
    """
    Tabla: employee_role_links
    Relación muchos-a-muchos entre empleados y roles.

    PK compuesta: (employee_id, role_id)
    """
    __tablename__ = "employee_role_links"
    metadata = metadata

    # 🔗 Claves compuestas (PK)
    employee_id: int = Field(
        primary_key=True,
        foreign_key="employees.id",
        description="Empleado al que se le asigna el rol.",
    )
    role_id: int = Field(
        primary_key=True,
        foreign_key="roles.id",
        description="Rol asignado al empleado.",
    )

    # 🕒 Metadatos del vínculo
    assigned_at: datetime | None = Field(
        default=None,
        description="Marca de tiempo de la asignación (set por la BD con DEFAULT now(), si lo tienes en el DDL).",
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
# ---------------------------------------------------------------------------
# 2. 🔗 bot_category_links
# ---------------------------------------------------------------------------
class BotCategoryLink(TlalocDB_Base, table=True):
    """
    Tabla: bot_category_links
    Relación muchos-a-muchos entre bots y categorías.
    PK compuesta: (bot_id, category_id).
    """
    __tablename__ = "bot_category_links"
    metadata = metadata

    # 🔗 Claves compuestas (PK)
    bot_id: int = Field(
        primary_key=True,
        foreign_key="bots.id",
        ondelete="CASCADE",
        description="Bot asociado a la categoría."
    )
    category_id: int = Field(
        primary_key=True,
        foreign_key="bot_categories.id",
        ondelete="CASCADE",
        description="Categoría asociada al bot."
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 3. 🔗 sensor_model_magnitude_links
# ---------------------------------------------------------------------------
class SensorModelMagnitudeLink(TlalocDB_Base, table=True):
    """
    Tabla: sensor_model_magnitude_links
    Relación muchos-a-muchos entre modelos de sensores y magnitudes.
    """
    __tablename__ = "sensor_model_magnitude_links"
    metadata = metadata

    # 🔗 Relaciones (PK compuesta)
    sensor_model_id: int = Field(
        foreign_key="sensor_models.id",
        primary_key=True,
        description="Identificador del modelo de sensor.",
        ondelete="CASCADE"
    )

    magnitude_id: int = Field(
        foreign_key="magnitudes.id",
        primary_key=True,
        description="Identificador de la magnitud asociada.",
        ondelete="CASCADE"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 4. 🔗 actuator_model_magnitude_links
# ---------------------------------------------------------------------------
class ActuatorModelMagnitudeLink(TlalocDB_Base, table=True):
    """
    Tabla: actuator_model_magnitude_links
    Relación muchos-a-muchos entre modelos de actuadores y magnitudes.
    """
    __tablename__ = "actuator_model_magnitude_links"
    metadata = metadata

    # 🔗 Relaciones (PK compuesta)
    actuator_model_id: int = Field(
        foreign_key="actuator_models.id",
        primary_key=True,
        ondelete="CASCADE",
        description="Identificador del modelo de actuador."
    )

    magnitude_id: int = Field(
        foreign_key="magnitudes.id",
        primary_key=True,
        ondelete="CASCADE",
        description="Identificador de la magnitud asociada."
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 5. 🔗 bot_user_subscription_links
# ---------------------------------------------------------------------------
class BotUserSubscriptionLink(TlalocDB_Base, table=True):
    """
    Tabla: bot_user_subscription_links
    Relación N:M entre bot_users y subscriptions.
    """
    __tablename__ = "bot_user_subscription_links"
    metadata = metadata

    # 🔗 Claves (PK compuesta)
    bot_user_id: int = Field(
        primary_key=True,
        foreign_key="bot_users.id",
        ondelete="CASCADE",
        description="Usuario del bot."
    )
    subscription_id: int = Field(
        primary_key=True,
        foreign_key="subscriptions.id",
        ondelete="CASCADE",
        description="Suscripción asociada."
    )

    created_at: datetime | None = Field(
        default=None,
        description="Marca de creación (la BD la establece con DEFAULT now()).",
    )

# ---------------------------------------------------------------------------
# 6. 🔗 user_process_permission_links
# ---------------------------------------------------------------------------
class UserProcessPermissionLink(TlalocDB_Base, table=True):
    """
    Tabla: user_process_permission_links
    Permisos que un usuario de bot posee sobre un proceso concreto.
    Relación muchos-a-muchos entre user_processes y user_process_permissions.
    """
    __tablename__ = "user_process_permission_links"
    metadata = metadata

    # 🔗 Relaciones (PK compuesta)
    user_process_id: int = Field(
        primary_key=True,
        foreign_key="user_processes.id",
        description="Proceso asignado al usuario.",
        ondelete="CASCADE",
    )

    permission_id: int = Field(
        primary_key=True,
        foreign_key="user_process_permissions.id",
        description="Permiso otorgado al usuario sobre el proceso.",
        ondelete="CASCADE",
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 7. 🔗 bot_process_permission_links
# ---------------------------------------------------------------------------
class BotProcessPermissionLink(TlalocDB_Base, table=True):
    """
    Tabla: bot_process_permission_links
    Permisos que un bot posee sobre un proceso concreto.
    Relación muchos-a-muchos entre bot_processes y bot_process_permissions.
    """
    __tablename__ = "bot_process_permission_links"
    metadata = metadata

    # 🔗 Relaciones (PK compuesta)
    bot_process_id: int = Field(
        primary_key=True,
        foreign_key="bot_processes.id",
        description="Proceso gestionado por un bot dentro de una suscripción.",
        ondelete="CASCADE",
    )

    permission_id: int = Field(
        primary_key=True,
        foreign_key="bot_process_permissions.id",
        description="Permiso asignado al bot sobre el proceso.",
        ondelete="CASCADE",
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

#  ╭──────────────────────────────────────────────────────╮
#  │ 📚 1. Catálogos base (sin dependencias)              │
#  ╰──────────────────────────────────────────────────────╯
# ---------------------------------------------------------------------------
# 8. 🤖 bot_model_statuses
# ---------------------------------------------------------------------------
class BotModelStatus(TlalocDB_Base, table=True):
    """
    Tabla: bot_model_statuses
    Catálogo de estados de desarrollo de un modelo de bot (p. ej. EN_DESARROLLO, EN_PRODUCCION).
    """
    __tablename__ = "bot_model_statuses"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(unique=True, nullable=False)
    name: NameStr = Field(unique=True, nullable=False)

    description: str | None = Field(
        default=None,
        nullable=True,
        description="Descripción del estado del modelo de bot."
    )

    # 🔗 Relaciones
    bot_models: list["BotModel"] = Relationship(
        back_populates="status",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 9. 🤖 bot_statuses
# ---------------------------------------------------------------------------
class BotStatus(TlalocDB_Base, table=True):
    """
    Tabla: bot_statuses
    Catálogo de estados operativos que puede tener un bot
    (p. ej. ONLINE, OFFLINE, ERROR).
    """
    __tablename__ = "bot_statuses"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(
        unique=True,
        nullable=False,
        description="Código único en mayúsculas, sin espacios, hasta 30 caracteres (ej: ONLINE)."
    )
    name: NameStr = Field(
        unique=True,
        nullable=False,
        description="Nombre legible y único (ej: En línea)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada del estado del bot."
    )

    # ⚙️ Estado de activación
    is_active: bool = Field(
        default=True,
        description="Indica si el estado está activo."
    )

    # 🔗 Relacion con `Bot`
    bots: list["Bot"] = Relationship(
        back_populates="status",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 10. 🤖 bot_environments
# ---------------------------------------------------------------------------
class BotEnvironment(TlalocDB_Base, table=True):
    """
    Tabla: bot_environments
    Catálogo de entornos donde puede ejecutarse un bot
    (p. ej. PRODUCCION, DESARROLLO, PRUEBAS).
    """
    __tablename__ = "bot_environments"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas, sin espacios, hasta 30 caracteres (ej: PRODUCCION)."
    )
    name: NameStr = Field(
        unique=True,
        description="Nombre legible y único (ej: Producción)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada del entorno."
    )

    # ⚙️ Estado de activación
    is_active: bool = Field(
        default=True,
        description="Indica si el entorno está activo."
    )

    # 🔗 Relacion con `Bot`
    bots: list["Bot"] = Relationship(
        back_populates="environment",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 11. 🤖 bot_categories
# ---------------------------------------------------------------------------
class BotCategory(TlalocDB_Base, table=True):
    """
    Tabla: bot_categories
    Catálogo de categorías funcionales de los bots
    (p. ej. MONITOREO, AUTOMATIZACION).
    """
    __tablename__ = "bot_categories"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas, sin espacios, hasta 30 caracteres (ej: MONITOREO)."
    )
    name: NameStr = Field(
        unique=True,
        description="Nombre legible y único (ej: Monitoreo)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada de la categoría del bot."
    )

    # 🔗 Relación con `Bot`
    bots: list["Bot"] = Relationship(
        back_populates="categories",
        link_model=BotCategoryLink,
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 12. 🧩 process_templates
# ---------------------------------------------------------------------------
class ProcessTemplate(TlalocDB_Base, table=True):
    """
    Tabla: process_templates
    Catálogo de plantillas estandarizadas de procesos operativos
    (p. ej. GERMINACION, RIEGO_ZONAL, TESTEO_MATERAS).
    Cada plantilla describe la lógica funcional común a múltiples
    procesos implementados en distintas unidades operativas.
    """
    __tablename__ = "process_templates"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas, sin espacios, hasta 30 caracteres (ej: GERMINACION)."
    )
    name: NameStr = Field(
        description="Nombre legible de la plantilla (ej: Germinación)."
    )

    # ⚙️ Flags
    is_experimental: bool = Field(
        default=False,
        description="Indica si el proceso está en fase experimental."
    )
    is_active: bool = Field(
        default=True,
        description="Indica si la plantilla está activa."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada de la plantilla de proceso."
    )

    # 🔗 Relaciones (1:N con subprocess_types)
    subprocess_types: list["SubprocessType"] = Relationship(
        back_populates="process_template",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 13. 📏 magnitudes
# ---------------------------------------------------------------------------
class Magnitude(TlalocDB_Base, table=True):
    """
    Tabla: magnitudes
    Catálogo de magnitudes físicas que los bots pueden medir o controlar
    (p. ej. TEMPERATURA, HUMEDAD, LUZ).
    """
    __tablename__ = "magnitudes"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas, sin espacios, hasta 30 caracteres (ej: TEMPERATURA)."
    )
    name: NameStr = Field(
        unique=True,
        description="Nombre legible y único (ej: Temperatura)."
    )

    # 📏 Unidades y símbolos
    unit: str = Field(
        max_length=20,
        description="Unidad de medida en formato legible (ej: Celsius, Lux, Pascal)."
    )
    symbol: str = Field(
        max_length=10,
        description="Símbolo asociado a la magnitud (ej: °C, lx, Pa)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada de la magnitud."
    )

    # 🔢 Precisión de lectura/control
    decimal_places: int = Field(
        default=2,
        ge=0,
        le=6,
        description="Número de decimales permitidos (0-6)."
    )

    # 🔗 Relación con `SensorModel`
    sensor_models: list["SensorModel"] = Relationship(
        back_populates="magnitudes",
        link_model=SensorModelMagnitudeLink,
    )

    # 🔗 Relación con `ActuatorModel`
    actuator_models: list["ActuatorModel"] = Relationship(
        back_populates="magnitudes",
        link_model=ActuatorModelMagnitudeLink,
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 14. 🏭 manufacturers
# ---------------------------------------------------------------------------
class Manufacturer(TlalocDB_Base, table=True):
    """
    Tabla: manufacturers
    Catálogo de fabricantes de hardware utilizado en los procesos
    (p. ej. MICROCHIP, BOSCH, TEXAS_INSTRUMENTS).
    """
    __tablename__ = "manufacturers"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas, sin espacios, hasta 30 caracteres (ej: BOSCH)."
    )
    name: NameStr = Field(
        unique=True,
        description="Nombre legible y único (ej: Bosch)."
    )

    # 🌐 Datos de contacto
    website: str | None = Field(
        default=None,
        description="URL del sitio web del fabricante (http/https/ftp)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción del fabricante o notas adicionales."
    )

    # 🔗 Relación con sensores
    sensor_models: list["SensorModel"] = Relationship(
        back_populates="manufacturer",
        passive_deletes="all"
    )

    # 🔗 Relación con actuadores
    actuator_models: list["ActuatorModel"] = Relationship(
        back_populates="manufacturer",
        passive_deletes="all"
    )

    # 🔗 Relación con microprocesadores
    controller_models: list["ControllerModel"] = Relationship(
        back_populates="manufacturer",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
#15. 🗓️ subscription_statuses
# ---------------------------------------------------------------------------
class SubscriptionStatus(TlalocDB_Base, table=True):
    """
    Tabla: subscription_statuses
    Catálogo de estados posibles de una suscripción
    (p. ej. ACTIVA, GRACE_PERIOD, CANCELADA).
    """
    __tablename__ = "subscription_statuses"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas, sin espacios, hasta 30 caracteres (ej: ACTIVA)."
    )
    name: NameStr = Field(
        description="Nombre legible del estado de la suscripción (ej: Activa)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada del estado de suscripción."
    )

    # ⚙️ Estado de activación
    is_active: bool = Field(
        default=True,
        description="Indica si el estado está activo."
    )

    # 🔗 Relación con `Subscription`
    subscriptions: list["Subscription"] = Relationship(
        back_populates="status",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 16. ⏳ period_units
# ---------------------------------------------------------------------------
class PeriodUnit(TlalocDB_Base, table=True):
    """
    Tabla: period_units
    Catálogo de unidades de periodo utilizadas en planes o suscripciones
    (p. ej. DIA, SEMANA, MES).
    """
    __tablename__ = "period_units"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Clave de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas (ej: DIA, SEMANA, MES)."
    )

    # 📛 Nombre en español
    name_es: NameStr = Field(
        unique=True,
        description="Nombre en español de la unidad de periodo (ej: Día, Semana, Mes)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada de la unidad de periodo."
    )

    # 🔗 Relaciones (1:N con subprocess_types)
    plans: list["Plan"] = Relationship(
        back_populates="period_unit",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 17. 💸 invoice_statuses
# ---------------------------------------------------------------------------
class InvoiceStatus(TlalocDB_Base, table=True):
    """
    Tabla: invoice_statuses
    Catálogo de estados que puede tener una factura
    (p. ej. PENDIENTE, PAGADA, VENCIDA).
    """
    __tablename__ = "invoice_statuses"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas, hasta 30 caracteres (ej: PAGADA)."
    )
    name: NameStr = Field(
        description="Nombre legible del estado de factura (ej: Pagada)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada del estado de la factura."
    )

    # ⚙️ Estado de activación
    is_active: bool = Field(
        default=True,
        description="Indica si el estado está activo."
    )

    # 🔗 Relación con `Invoice`
    invoices: list["Invoice"] = Relationship(
        back_populates="status",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 18. 💳 payment_statuses
# ---------------------------------------------------------------------------
class PaymentStatus(TlalocDB_Base, table=True):
    """
    Tabla: payment_statuses
    Catálogo de estados posibles de un pago
    (p. ej. PENDIENTE, CONFIRMADO, FALLIDO).
    """
    __tablename__ = "payment_statuses"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas, hasta 30 caracteres (ej: CONFIRMADO)."
    )
    name: NameStr = Field(
        description="Nombre legible del estado de pago (ej: Confirmado)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada del estado de pago."
    )

    # ⚙️ Estado de activación
    is_active: bool = Field(
        default=True,
        description="Indica si el estado está activo."
    )

    # 🔗 Relación con `PaymentStatus`
    payments_attempts: list["PaymentAttempt"] = Relationship(
        back_populates="status",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 19. 💳 payment_methods
# ---------------------------------------------------------------------------
class PaymentMethod(TlalocDB_Base, table=True):
    """
    Tabla: payment_methods
    Catálogo de métodos de pago aceptados
    (p. ej. TARJETA, NEQUI, DAVIPLATA, TRANSFERENCIA).
    """
    __tablename__ = "payment_methods"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas, hasta 30 caracteres (ej: NEQUI)."
    )
    name: NameStr = Field(
        unique=True,
        description="Nombre legible y único del método de pago (ej: Nequi)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada del método de pago."
    )

    # ⚙️ Estado de activación
    is_active: bool = Field(
        default=True,
        description="Indica si el método de pago está activo."
    )

    # 🔗 Relación con `Payment`
    payments: list["Payment"] = Relationship(
        back_populates="method",
        passive_deletes="all"
    )

    # 🔗 Relación con `PaymentAttempt`
    payment_attempts: list["PaymentAttempt"] = Relationship(
        back_populates="method",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 20. 🔐 user_process_permissions
# ---------------------------------------------------------------------------
class UserProcessPermission(TlalocDB_Base, table=True):
    """
    Tabla: user_process_permissions
    Catálogo de permisos que pueden tener los usuarios para ejecutar acciones
    en procesos (p. ej. READ_TELEMETRY, START_PROCESS).
    """
    __tablename__ = "user_process_permissions"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Clave de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas, hasta 30 caracteres (ej: READ_TELEMETRY)."
    )

    # 📛 Nombre legible (NO único en el DDL original)
    name: NameStr = Field(
        description="Nombre del permiso (ej: Leer telemetría)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción del permiso."
    )

    # 🔗 Relación con `UserProcess`
    user_processes: list["UserProcess"] = Relationship(
        back_populates="permissions",
        link_model=UserProcessPermissionLink,
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 21. 🤖 bot_process_permissions
# ---------------------------------------------------------------------------
class BotProcessPermission(TlalocDB_Base, table=True):
    """
    Tabla: bot_process_permissions
    Catálogo de permisos que pueden tener los bots sobre procesos
    (p. ej. SEND_DATA, EXECUTE_ACTION).
    """
    __tablename__ = "bot_process_permissions"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Clave de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas, hasta 30 caracteres (ej: SEND_DATA)."
    )

    # 📛 Nombre legible (NO único en el DDL original)
    name: NameStr = Field(
        description="Nombre del permiso (ej: Enviar datos)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción del permiso."
    )

    # 🔗 Relación con `BotProcess`
    bot_processes: list["BotProcess"] = Relationship(
        back_populates="permissions",
        link_model=BotProcessPermissionLink
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 22. 👥 roles
# ---------------------------------------------------------------------------
class Role(TlalocDB_Base, table=True):
    """
    Tabla: roles
    Catálogo de roles asignables a usuarios
    (p. ej. ADMIN, SUPERVISOR, VIEWER).
    """
    __tablename__ = "roles"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Clave de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas, hasta 30 caracteres (ej: ADMIN)."
    )

    # 📛 Nombre legible
    name: NameStr = Field(
        unique=True,
        description="Nombre del rol (ej: Administrador)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción del rol y sus responsabilidades."
    )

    # ⚙️ Estado de activación
    is_active: bool = Field(
        default=True,
        description="Indica si el rol está activo."
    )

    # 🔗 Relacion con `Employee`
    employees: list["Employee"] = Relationship(
        back_populates="roles",
        link_model=EmployeeRoleLink,
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

#  ╭──────────────────────────────────────────────────────╮
#  │ 🗂️ 2. Catálogos dependientes                         │
#  ╰──────────────────────────────────────────────────────╯

# ---------------------------------------------------------------------------
# 23. 🧩 subprocess_types
# ---------------------------------------------------------------------------
class SubprocessType(TlalocDB_Base, table=True):
    """
    Tabla: subprocess_types
    Catálogo de tipos funcionales de subproceso.
    Indica si un tipo puede agruparse (is_groupable) y si es experimental.
    """
    __tablename__ = "subprocess_types"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Código único
    code: CodeStr = Field(
        unique=True,
        description="Código único en mayúsculas (ej: SENSOR)."
    )

    # 📛 Nombre único
    name: NameStr = Field(
        unique=True,
        description="Nombre del tipo de subproceso (ej: Sensor ambiental)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada del tipo de subproceso."
    )

    # ⚙️ Estado
    is_active: bool = Field(
        default=True,
        description="Indica si el tipo de subproceso está activo."
    )

    # 🧩 Configuración
    is_groupable: bool = Field(
        default=False,
        description="Indica si este tipo de subproceso puede agruparse."
    )
    is_experimental: bool = Field(
        default=False,
        description="Indica si el tipo de subproceso está en fase experimental."
    )

    # 🔗 Relación con `ProcessTemplate`
    process_template_id: int | None = Field(
        default=None,
        foreign_key="process_templates.id",
        ondelete="RESTRICT",
        description="Plantilla de proceso a la que pertenece este tipo."
    )

    process_template: ProcessTemplate | None = Relationship(
        back_populates="subprocess_types"
    )

    # 🔗 Relación con `SubprocessGroup`
    subprocess_groups: list["SubprocessGroup"] = Relationship(
        back_populates="subprocess_type",
        passive_deletes="all"
    )

    # 🔗 Relación con `Subprocess`
    subprocesses: list["Subprocess"] = Relationship(
        back_populates="subprocess_type",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 24. 🗓️ plans
# ---------------------------------------------------------------------------
class Plan(TlalocDB_Base, table=True):
    """
    Tabla: plans
    Catálogo de planes de suscripción disponibles en la plataforma.
    Contiene información comercial, límites de uso y unidad de periodo.
    """
    __tablename__ = "plans"
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único del plan (ej: BASIC, PRO, ENTERPRISE)."
    )
    name: NameStr = Field(
        description="Nombre del plan de suscripción."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada del plan."
    )

    # 💰 Información comercial
    price_period: Decimal = Field(
        description="Precio del plan por cada periodo de facturación."
    )
    currency: str = Field(
        default="COP",
        min_length=3,
        max_length=3,
        description="Moneda ISO 4217 (ej: COP, USD, EUR)."
    )

    # 📊 Límites de uso
    max_users: int = Field(
        default=1,
        ge=1,
        description="Número máximo de usuarios permitidos en el plan."
    )
    max_processes: int = Field(
        default=1,
        ge=1,
        description="Número máximo de procesos que admite el plan."
    )
    max_mcus_x_process: int = Field(
        default=1,
        ge=1,
        description="Número máximo de MCUs permitidos por proceso."
    )

    # 🌟 Características extendidas (✅ JSONB en Postgres)
    features: dict[str, Any] | None = Field(
        default=None,
        description="Características adicionales del plan en formato JSON.",
        sa_column=Column(JSONB, nullable=True)
    )

    # ⚙️ Estado
    is_active: bool = Field(
        default=True,
        description="Indica si el plan está activo."
    )

    # 🔗 Relaciones con `PeriodUnit`
    period_unit_id: int = Field(
        foreign_key="period_units.id",
        ondelete="RESTRICT",
        description="Unidad de periodo asociada al plan (ej: mensual, anual)."
    )

    period_unit: PeriodUnit = Relationship(
        back_populates="plans"
    )

    # 🔗 Relaciones con `Subscription`
    subscriptions: list["Subscription"] = Relationship(
        back_populates="plan",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 25. 🤖 bot_models
# ---------------------------------------------------------------------------
class BotModel(TlalocDB_Base, table=True):
    """
    Tabla: bot_models
    Catálogo de modelos de bot disponibles en el sistema.
    Cada modelo tiene un nombre + versión únicos, y un estado de desarrollo.
    """
    __tablename__ = "bot_models"
    __table_args__ = (
        UniqueConstraint("name", "version", name="uq_bot_model_name_version"),
    )
    metadata = metadata

    # 🔑 Clave primaria
    id: int = Field(primary_key=True)

    # 📛 Identificación
    name: NameStr = Field(
        description="Nombre del modelo de bot."
    )
    version: VersionStr = Field(
        description="Versión del modelo en formato semántico (ej: 1.0, 2.1)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción del modelo de bot."
    )

    # 🔗 Relación con bot_model_statuses
    status_id: int | None = Field(
        default=None,
        foreign_key="bot_model_statuses.id",
        ondelete="RESTRICT",
        description="Estado del modelo (ej: EN_DESARROLLO, PRODUCCION)."
    )

    status: BotModelStatus | None = Relationship(
        back_populates="bot_models"
    )

    # 🔗 Relación con Bot
    bots: list["Bot"] = Relationship(
        back_populates="model",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 26. 🌡️ sensor_models
# ---------------------------------------------------------------------------
class SensorModel(TlalocDB_Base, table=True):
    """
    Tabla: sensor_models
    Catálogo de modelos de sensores disponibles en el sistema.
    (name, version) debe ser único.
    """
    __tablename__ = "sensor_models"
    __table_args__ = (
        UniqueConstraint("name", "version", name="uq_sensor_model_name_version"),
    )
    metadata = metadata

    # 🔑 PK
    id: int = Field(primary_key=True)

    # 📛 Identificación
    name: NameStr = Field(
        description="Nombre del modelo de sensor (ej: DHT22, DS18B20)."
    )
    version: VersionStr | None = Field(
        default=None,
        description="Versión opcional del modelo (ej: 1.0, 2.1)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción del modelo de sensor."
    )

    # 🔗 Relación con `Manufacturer`
    manufacturer_id: int | None = Field(
        default=None,
        foreign_key="manufacturers.id",
        ondelete="SET NULL",
        description="Fabricante del sensor."
    )

    manufacturer: Manufacturer | None = Relationship(
        back_populates="sensor_models"
    )

    # 🔗 Relación con `Sensor`
    sensors: list["Sensor"] = Relationship(
        back_populates="model",
        passive_deletes="all"
    )

    # 🔗 Relación con `Magnitude`
    magnitudes: list[Magnitude] = Relationship(
        back_populates="sensor_models",
        link_model=SensorModelMagnitudeLink,
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 27. ⚙️ actuator_models
# ---------------------------------------------------------------------------
class ActuatorModel(TlalocDB_Base, table=True):
    """
    Tabla: actuator_models
    Catálogo de modelos de actuadores disponibles en el sistema.
    (name, version) debe ser único.
    """
    __tablename__ = "actuator_models"
    __table_args__ = (
        UniqueConstraint("name", "version", name="uq_actuator_model_name_version"),
    )
    metadata = metadata

    # 🔑 PK
    id: int = Field(primary_key=True)

    # 📛 Identificación
    name: NameStr = Field(
        description="Nombre del modelo de actuador (ej: Relay, Solenoid Valve)."
    )
    version: VersionStr | None = Field(
        default=None,
        description="Versión opcional del modelo (ej: 1.0, 2.1)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción detallada del actuador."
    )

    # 🔗 Relación con `Manufacturer`
    manufacturer_id: int | None = Field(
        default=None,
        foreign_key="manufacturers.id",
        ondelete="SET NULL",
        description="Fabricante del actuador."
    )

    manufacturer: Manufacturer | None = Relationship(
        back_populates="actuator_models"
    )

    # 🔗 Relación con `Actuator`
    actuators: list["Actuator"] = Relationship(
        back_populates="model",
        passive_deletes="all"
    )

    # 🔗 Relación con `Magnitude`
    magnitudes: list[Magnitude] = Relationship(
        back_populates="actuator_models",
        link_model=ActuatorModelMagnitudeLink,
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 28. 🕹️ controller_models
# ---------------------------------------------------------------------------
class ControllerModel(TlalocDB_Base, table=True):
    """
    Tabla: controller_models
    Catálogo de modelos de controladores (p. ej. ESP32, PLC).
    """
    __tablename__ = "controller_models"
    __table_args__ = (
        UniqueConstraint("name", "version", name="uq_controller_model_name_version"),
    )
    metadata = metadata

    # 🔑 Clave primaria (en PG es SMALLINT; aquí mapeamos como int)
    id: int = Field(primary_key=True)

    # 📛 Identificación
    name: NameStr = Field(
        description="Nombre del modelo de controlador (ej: ESP32-WROOM)."
    )
    version: VersionStr = Field(
        description="Versión del modelo (formato 1.0, 2.1, 3.0.4)."
    )

    # 🧱 Arquitectura opcional
    architecture: str | None = Field(
        default=None,
        max_length=50,
        description="Arquitectura/SoC/MCU (ej: Xtensa LX6, ARM Cortex-M)."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción del modelo de controlador."
    )

    # 🔗 Relación con `Manufacturer`
    manufacturer_id: int | None = Field(
        default=None,
        foreign_key="manufacturers.id",
        ondelete="SET NULL",
        description="Fabricante del controlador."
    )

    manufacturer: Manufacturer | None = Relationship(
        back_populates="controller_models"
    )

    # 🔗 Relación con `ControllerDevice`
    controller_devices: list["ControllerDevice"] = Relationship(
        back_populates="model",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# # ╭──────────────────────────────────────────────────────╮
# # │ 🏢 3. Datos maestro                                  │
# # ╰──────────────────────────────────────────────────────╯

# ---------------------------------------------------------------------------
# 29. 🏢 companies
# ---------------------------------------------------------------------------
class Company(TlalocDB_Base, table=True):
    """
    Tabla: companies
    Catálogo de empresas que utilizan los bots y servicios.
    """
    __tablename__ = "companies"
    metadata = metadata

    # 🔑 PK
    id: int = Field(primary_key=True)

    # 🔐 Claves de negocio
    code: CodeStr = Field(
        unique=True,
        description="Código único de la empresa (ej: ACME_INC)."
    )
    name: NameStr = Field(
        unique=True,
        description="Nombre de la empresa."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción de la empresa."
    )

    # ⚙️ Estado
    is_active: bool = Field(
        default=True,
        description="Indica si la empresa está activa."
    )

    # ☎️ Contacto
    phone: PhoneE164Str = Field(
        unique=True,
        description="Teléfono en formato E.164 (ej: +573001112233)."
    )
    email: EmailStr = Field(
        unique=True,
        description="Correo electrónico de la empresa."
    )
    website: str | None = Field(
        default=None,
        description="Sitio web de la empresa (http/https/ftp)."
    )

    # 📍 Dirección física
    country: str | None = Field(default=None, description="País de la empresa.")
    state: str | None = Field(default=None, description="Departamento o estado.")
    city: str | None = Field(default=None, description="Ciudad.")
    zip_code: str | None = Field(default=None, description="Código postal.")
    address: str | None = Field(default=None, description="Dirección completa.")

    # 🔗 Relación con `Employee`
    employees: list["Employee"] = Relationship(
        back_populates="company",
        passive_deletes="all"
    )

    # 🔗 Relación con `Subscription`
    subscriptions: list["Subscription"] = Relationship(
        back_populates="company",
        passive_deletes="all"
    )

    # 🔗 Relación con `OperationalUnit`
    operational_units: list["OperationalUnit"] = Relationship(
        back_populates="company",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 30. 👤 employees
# ---------------------------------------------------------------------------
class Employee(TlalocDB_Base, table=True):
    """
    Tabla: employees
    Registro de empleados asociados a las empresas.
    """
    __tablename__ = "employees"
    metadata = metadata

    # 🔑 PK (en PG es BIGINT; aquí mapeamos como int)
    id: int = Field(primary_key=True)

    # 🧍‍♂️ Datos personales
    first_name: str = Field(
        description="Primer nombre del empleado (obligatorio).",
        max_length=50,
    )
    middle_name: str | None = Field(
        default=None,
        description="Segundo nombre (opcional).",
        max_length=50,
    )
    last_name: str = Field(
        description="Primer apellido (obligatorio).",
        max_length=50,
    )
    second_last_name: str | None = Field(
        default=None,
        description="Segundo apellido (opcional).",
        max_length=50,
    )

    # ✉️ / 📞 Contacto
    email: EmailStr = Field(
        unique=True,
        description="Correo electrónico corporativo único.",
    )
    mobile_phone: PhoneE164Str = Field(
        unique=True,
        description="Teléfono móvil en formato E.164 único (ej: +573001112233).",
        max_length=16,
    )

    # 💼 Información laboral
    position: str | None = Field(
        default=None,
        description="Cargo/posición (opcional).",
        max_length=100,
    )

    # 🔗 Relación con `Company`
    company_id: int = Field(
        foreign_key="companies.id",
        ondelete="CASCADE",
        description="Empresa a la que pertenece el empleado.",
    )

    company: Company = Relationship(
        back_populates="employees"
    )

    # 🔗 Relación con `CompanyContact`
    company_contact: Optional["CompanyContact"] = Relationship(
        back_populates="employee",
        cascade_delete=True,
        sa_relationship_kwargs={"uselist": False}
    )

    # 🔗 Relación con `Role`
    roles: list[Role] = Relationship(
        back_populates="employees",
        link_model=EmployeeRoleLink,
    )

    # 🔗 Relación con `BotUser`
    bot_user: Optional["BotUser"] = Relationship(
        back_populates="employee",
        passive_deletes="all",
        sa_relationship_kwargs={"uselist": False}
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 31. ☎️ company_contacts
# ---------------------------------------------------------------------------
class CompanyContact(TlalocDB_Base, table=True):
    """
    Tabla: company_contacts
    Contactos designados dentro de cada empresa.
    Relación 1:1 con un empleado.
    """
    __tablename__ = "company_contacts"
    metadata = metadata

    # 🔑 PK
    id: int = Field(primary_key=True)

    # 📌 Atributos del contacto
    is_primary: bool = Field(
        default=False,
        description="Indica si el contacto es el principal de la empresa."
    )
    notes: str | None = Field(
        default=None,
        description="Notas adicionales del contacto."
    )

    # 🔗 Relación 1:1 con Employee
    employee_id: int = Field(
        unique=True,
        foreign_key="employees.id",
        ondelete="CASCADE",
        description="Empleado asociado como contacto."
    )

    employee: Employee = Relationship(
        back_populates="company_contact",
        sa_relationship_kwargs={"uselist": False}
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 32. 🤖 bots
# ---------------------------------------------------------------------------
class Bot(TlalocDB_Base, table=True):
    """
    Tabla: bots
    Registro de bots disponibles en el sistema.
    """
    __tablename__ = "bots"
    metadata = metadata

    # 🔑 PK
    id: int = Field(primary_key=True)

    # 📛 Identificación
    name: NameStr = Field(
        unique=True,
        description="Nombre único del bot."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción del bot."
    )

    # 🌐 Endpoint del bot (http/https), único
    api_url: str = Field(
        unique=True,
        max_length=255,
        description="URL del endpoint del bot (http/https)."
    )

    # ⚙️ Estado y control
    is_active: bool = Field(
        default=True,
        description="Indica si el bot está activo."
    )
    last_ping: datetime | None = Field(
        default=None,
        description="Último ping recibido del bot."
    )
    request_per_minute: int = Field(
        default=0,
        ge=0,
        description="Límite de solicitudes por minuto."
    )

    # ✅ JSONB en Postgres
    data: dict[str, Any] | None = Field(
        default=None,
        description="Metadata adicional del bot (JSON).",
        sa_column=Column(JSONB, nullable=True)
    )

    # 🔗 Relación con `BotModel`
    bot_model_id: int = Field(
        foreign_key="bot_models.id",
        ondelete="CASCADE",
        description="Modelo del bot (ON DELETE CASCADE en la BD)."
    )

    model: BotModel = Relationship(
        back_populates="bots"
    )

    # 🔗 Relación con `BotStatus`
    status_id: int | None = Field(
        default=None,
        foreign_key="bot_statuses.id",
        ondelete="RESTRICT",
        description="Estado operativo del bot (ON DELETE RESTRICT en la BD)."
    )

    status: BotStatus | None = Relationship(
        back_populates="bots"
    )

    # 🔗 Relación con `BotEnvironment`
    environment_id: int | None = Field(
        default=None,
        foreign_key="bot_environments.id",
        ondelete="RESTRICT",
        description="Entorno del bot (ON DELETE RESTRICT en la BD)."
    )

    environment: BotEnvironment | None = Relationship(
        back_populates="bots"
    )

    # 🔗 Relación con `BotCredential`
    credentials: Optional["BotCredential"] = Relationship(
        back_populates="bot",
        passive_deletes="all",
        sa_relationship_kwargs={"uselist": False}
    )

    # 🔗 Relación con `BotCategory` (N:M)
    categories: list[BotCategory] = Relationship(
        back_populates="bots",
        link_model=BotCategoryLink,
    )

    # 🔗 Relación con `Subscription`
    subscriptions: list["Subscription"] = Relationship(
        back_populates="bot",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 33. 🔐 bot_credentials
# ---------------------------------------------------------------------------
class BotCredential(TlalocDB_Base, table=True):
    """
    Tabla: bot_credentials
    Credenciales asociadas 1:1 a cada bot.
    """
    __tablename__ = "bot_credentials"
    metadata = metadata

    # 🔑 PK
    id: int = Field(primary_key=True)

    # 🔐 Credenciales
    hashed_password: HashedStr = Field(
        description="Hash de la contraseña (no vacío, máx 255)."
    )

    # Token de acceso (opcional) — único si existe
    hashed_api_access_token: Optional[HashedStr] = Field(
        default=None,
        unique=True,
        description="Hash del token de acceso (opcional, único)."
    )

    # 🔗 Relación 1:1 con bots
    bot_id: int = Field(
        foreign_key="bots.id",
        unique=True,
        ondelete="CASCADE",
        description="Bot propietario de estas credenciales (relación 1:1)."
    )
    bot: Bot = Relationship(
        back_populates="credentials",
        sa_relationship_kwargs={"uselist": False}
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 34. 📝 subscriptions
# ---------------------------------------------------------------------------
class Subscription(TlalocDB_Base, table=True):
    """
    Tabla: subscriptions
    Suscripciones de empresas a un bot bajo un plan determinado.
    """
    __tablename__ = "subscriptions"
    __table_args__ = (
        UniqueConstraint("bot_id", "company_id", name="uq_subscriptions_bot_company"),
    )
    metadata = metadata

    # 🔑 PK
    id: int = Field(primary_key=True)

    # ⚙️ Estado y vigencia
    is_active: bool = Field(
        default=True,
        description="Indica si la suscripción está activa."
    )
    start_date: datetime | None = Field(
        default=None,
        description="Inicio de vigencia (TIMESTAMPTZ)."
    )
    end_date: datetime | None = Field(
        default=None,
        description="Fin de vigencia (TIMESTAMPTZ). Debe ser > start_date si ambos existen."
    )

    # 🔗 Relación con `Bot`
    bot_id: int = Field(
        foreign_key="bots.id",
        ondelete="CASCADE",
        description="Bot suscrito (ON DELETE CASCADE en la BD)."
    )
    bot: Bot = Relationship(
        back_populates="subscriptions"
    )

    # 🔗 Relación con `Company`
    company_id: int = Field(
        foreign_key="companies.id",
        ondelete="CASCADE",
        description="Empresa suscriptora (ON DELETE CASCADE en la BD)."
    )

    company: Company = Relationship(
        back_populates="subscriptions"
    )

    # 🔗 Relación con `Plan`
    plan_id: int = Field(
        foreign_key="plans.id",
        description="Plan contratado (ON DELETE RESTRICT en la BD)."
    )

    plan: Plan = Relationship(
        back_populates="subscriptions"
    )

    # 🔗 Relación con `SubscriptionStatus`
    status_id: int | None = Field(
        default=None,
        foreign_key="subscription_statuses.id",
        description="Estado de la suscripción (ON DELETE RESTRICT en la BD)."
    )

    status: SubscriptionStatus | None = Relationship(
        back_populates="subscriptions"
    )

    # 🔗 Relación con `BotUser`
    bot_users: list["BotUser"] = Relationship(
        back_populates="subscriptions",
        link_model=BotUserSubscriptionLink,
    )

    # 🔗 Relación con `BotProcess`
    process_links: list["BotProcess"] = Relationship(
        back_populates="subscription",
        passive_deletes="all"
    )

    # 🔗 Relación con `SubscriptionPeriod`
    periods: list["SubscriptionPeriod"] = Relationship(
        back_populates="subscription",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

    # ✅ Validación cross-field que refleja el CHECK del DDL
    @model_validator(mode="after")
    def _check_dates(self):
        if self.start_date is not None and self.end_date is not None:
            if not (self.start_date < self.end_date):
                raise ValueError("end_date debe ser mayor que start_date")
        return self

# ---------------------------------------------------------------------------
#35. 📝 OperationalUnit
# ---------------------------------------------------------------------------
class OperationalUnit(TlalocDB_Base, table=True):
    """
    Tabla: operational_units
    Unidades operativas pertenecientes a una empresa.
    """
    __tablename__ = "operational_units"
    metadata = metadata

    id: int = Field(
        primary_key=True,
        description="Identificador único de la unidad operativa."
    )

    code: CodeStr = Field(
        unique=True,
        nullable=False,
        description="Código único en formato normalizado (ej: PLANTA_01)."
    )

    name: NameStr = Field(
        unique=True,
        nullable=False,
        description="Nombre de la unidad operativa (ej: Vivero Autarquía)."
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
        description="Indica si la unidad está activa."
    )

    description: Optional[str] = Field(
        default=None,
        description="Descripción libre de la unidad operativa."
    )

    location: Optional[str] = Field(
        default=None,
        description="Ubicación o dirección de la unidad operativa."
    )

    # 🔗 Relación con `Company`
    company_id: int = Field(
        foreign_key="companies.id",
        ondelete="CASCADE",
        description="Referencia a la empresa propietaria."
    )

    company: Company = Relationship(
        back_populates="operational_units"
    )

    # 🔗 Relación con `Process`
    processes: list["Process"] = Relationship(
        back_populates="operational_unit",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 36. 📝 processes
# ---------------------------------------------------------------------------
class Process(TlalocDB_Base, table=True):
    """
    Tabla: processes
    Procesos que se ejecutan dentro de una unidad operativa.
    """
    __tablename__ = "processes"
    metadata = metadata

    id: int = Field(
        primary_key=True,
        description="Identificador único del proceso."
    )

    code: CodeStr = Field(
        unique=True,
        description="Código único normalizado (ej: GERMINACION_01)."
    )

    name: NameStr = Field(
        unique=True,
        description="Nombre único y legible del proceso."
    )

    is_active: bool = Field(
        default=True,
        description="Indica si el proceso está activo."
    )

    is_pilot: bool = Field(
        default=False,
        description="Indica si el proceso es piloto."
    )

    description: Optional[str] = Field(
        default=None,
        description="Descripción del proceso."
    )

    # 🔗 Relación con `OperationalUnit`
    operational_unit_id: int = Field(
        foreign_key="operational_units.id",
        ondelete="CASCADE",
        description="Unidad operativa a la que pertenece el proceso."
    )

    operational_unit: OperationalUnit = Relationship(
        back_populates="processes"
    )

    # 🔗 Relación con `SubprocessGroup`
    subprocess_groups: list["SubprocessGroup"] = Relationship(
        back_populates="process",
        passive_deletes="all"
    )

    # 🔗 Relación con `Subprocess`
    subprocesses: list["Subprocess"] = Relationship(
        back_populates="process",
        passive_deletes="all"
    )

    # 🔗 Relación con `UserProcess`
    user_links: list["UserProcess"] = Relationship(
        back_populates="process",
        passive_deletes="all"
    )

    # 🔗 Relación con `BotProcess`
    subscription_links: list["BotProcess"] = Relationship(
        back_populates="process",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )


# ---------------------------------------------------------------------------
# 37. 🧩 subprocess_groups
# ---------------------------------------------------------------------------
class SubprocessGroup(TlalocDB_Base, table=True):
    """
    Tabla: subprocess_groups
    Grupos homogéneos de subprocesos agrupables dentro de un proceso,
    según su tipo (solo si is_groupable = TRUE en subprocess_types).
    """
    __tablename__ = "subprocess_groups"
    metadata = metadata

    id: int = Field(
        primary_key=True,
        description="Identificador único del grupo de subprocesos."
    )

    # 📌 Campos propios
    name: NameStr = Field(
        nullable=False,
        description="Nombre del grupo de subprocesos (ej: Bombas Zona A)."
    )

    description: Optional[str] = Field(
        default=None,
        description="Descripción libre del grupo de subprocesos."
    )

    # 🔗 Relación con `SubprocessType`
    subprocess_type_id: int = Field(
        foreign_key="subprocess_types.id",
        ondelete="RESTRICT",
        description="Referencia al tipo de subproceso."
    )

    subprocess_type: SubprocessType = Relationship(
        back_populates="subprocess_groups"
    )

    # 🔗 Relación con `Process`
    process_id: int = Field(
        foreign_key="processes.id",
        ondelete="CASCADE",
        description="Proceso al que pertenece el grupo."
    )

    process: Process = Relationship(
        back_populates="subprocess_groups"
    )

    # 🔗 Relación con `Subprocess`
    subprocesses: list["Subprocess"] = Relationship(
        back_populates="group",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 38. 🪜 subprocesses
# ---------------------------------------------------------------------------
class Subprocess(TlalocDB_Base, table=True):
    """
    Tabla: subprocesses
    Subprocesos que conforman un proceso operativo.
    """
    __tablename__ = "subprocesses"
    metadata = metadata

    id: int = Field(
        primary_key=True,
        description="Identificador único del subproceso."
    )

    code: CodeStr = Field(
        unique=True,
        nullable=False,
        description="Código único normalizado del subproceso (ej: SP_GERMINA_01)."
    )

    name: NameStr = Field(
        unique=True,
        nullable=False,
        description="Nombre único y legible del subproceso."
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
        description="Indica si el subproceso está activo."
    )

    is_pilot: bool = Field(
        default=False,
        nullable=False,
        description="Indica si el subproceso está en fase piloto."
    )

    description: Optional[str] = Field(
        default=None,
        description="Descripción libre del subproceso."
    )

    # 🔗 Relación con `Process`
    process_id: int = Field(
        foreign_key="processes.id",
        ondelete="CASCADE",
        description="Proceso al que pertenece el subproceso."
    )

    process: Process = Relationship(
        back_populates="subprocesses"
    )

    # 🔗 Relación con `SubprocessType`
    subprocess_type_id: int = Field(
        foreign_key="subprocess_types.id",
        ondelete="RESTRICT",
        description="Tipo de subproceso."
    )

    subprocess_type: SubprocessType = Relationship(
        back_populates="subprocesses"
    )

    # 🔗 Relación con `SubprocessGroup`
    group_id: Optional[int] = Field(
        foreign_key="subprocess_groups.id",
        ondelete="SET NULL",
        description="Grupo al que pertenece (si aplica)."
    )

    group: Optional[SubprocessGroup] = Relationship(
        back_populates="subprocesses"
    )

    # 🔗 Relación con `ControllerDevice`
    controller_devices: list["ControllerDevice"] = Relationship(
        back_populates="subprocess",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 39. 🖥️  controller_devices
# ---------------------------------------------------------------------------
class ControllerDevice(TlalocDB_Base, table=True):
    """
    Tabla: controller_devices
    Dispositivos de control (p. ej. ESP32, PLC) instalados en un subproceso.
    """
    __tablename__ = "controller_devices"
    metadata = metadata

    # 🔑 PK
    id: int = Field(primary_key=True)

    # 🔐 Identificación
    code: CodeStr = Field(
        unique=True,
        description="Código único normalizado del dispositivo (ej: CTRL_ESP32_A1)."
    )
    name: NameStr = Field(
        description="Nombre legible del dispositivo (ej: Controlador Zona A)."
    )

    # 🔌 Identificadores de red
    mac_address: MacAddressStr | None = Field(
        default=None,
        unique=True,
        description="MAC del dispositivo (formato XX:XX:XX:XX:XX:XX o XX-XX-XX-XX-XX-XX)."
    )
    mqtt_topic: MqttTopicStr = Field(
        description="Tópico MQTT asociado (no vacío)."
    )

    # ⚙️ Estado
    is_active: bool = Field(
        default=True,
        description="Indica si el dispositivo está activo."
    )
    last_seen_at: datetime | None = Field(
        default=None,
        description="Último momento en que el dispositivo reportó actividad."
    )

    # 🔗 Relación con `Subprocess`
    subprocess_id: int = Field(
        foreign_key="subprocesses.id",
        ondelete="CASCADE",
        description="Subproceso al que está instalado el dispositivo (ON DELETE CASCADE en la BD)."
    )

    subprocess: Subprocess = Relationship(
        back_populates="controller_devices"
    )

    # 🔗 Relación con `ControllerModel`
    controller_model_id: int | None = Field(
        default=None,
        foreign_key="controller_models.id",
        description="Modelo del controlador (ON DELETE SET NULL en la BD)."
    )

    model: ControllerModel | None = Relationship(
        back_populates="controller_devices"
    )

    # 🔗 Relación con `Sensor`
    sensors: list["Sensor"] = Relationship(
        back_populates="controller_device",
        passive_deletes="all"
    )

    # 🔗 Relación con `Actuator`
    actuators: list["Actuator"] = Relationship(
        back_populates="controller_device",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 40. 📡  sensors
# ---------------------------------------------------------------------------
class Sensor(TlalocDB_Base, table=True):
    """
    Tabla: sensors
    Sensores físicos asociados a un dispositivo de control.
    """
    __tablename__ = "sensors"
    metadata = metadata

    # 🔑 PK
    id: int = Field(
        primary_key=True,
        description="Identificador único del sensor."
    )

    # 📌 Identificación
    code: CodeStr = Field(
        unique=True,
        description="Código único normalizado del sensor (ej: TEMP_CTRL_A1)."
    )
    name: NameStr = Field(
        unique=True,
        description="Nombre legible único del sensor (ej: Sensor de Temperatura Zona A)."
    )

    # ⚙️ Estado
    is_active: bool = Field(
        default=True,
        description="Indica si el sensor está activo."
    )

    description: str | None = Field(
        default=None,
        description="Descripción libre del sensor."
    )

    # 🔗 Relacion con `ControllerDevice`
    controller_device_id: int = Field(
        foreign_key="controller_devices.id",
        ondelete="CASCADE",
        description="Dispositivo de control al que pertenece el sensor."
    )

    controller_device: "ControllerDevice" = Relationship(
        back_populates="sensors"
    )

    # 🔗 Relacion con `SensorModel`
    sensor_model_id: Optional[int] = Field(
        default=None,
        foreign_key="sensor_models.id",
        description="Modelo del sensor (ON DELETE SET NULL).",
        ondelete="SET NULL"
    )

    model: Optional[SensorModel] = Relationship(
        back_populates="sensors"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 41. 🔧 actuators
# ---------------------------------------------------------------------------
class Actuator(TlalocDB_Base, table=True):
    """
    Tabla: actuators
    Actuadores físicos asociados a un dispositivo de control.
    """
    __tablename__ = "actuators"
    metadata = metadata

    # 🔑 PK
    id: int = Field(primary_key=True)

    # 📌 Identificación
    code: CodeStr = Field(
        unique=True,
        description="Código único normalizado del actuador (ej: VALVE_A1)."
    )
    name: NameStr = Field(
        description="Nombre legible del actuador."
    )

    # ⚙️ Estado
    is_active: bool = Field(
        default=True,
        description="Indica si el actuador está activo."
    )

    # 📄 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción del actuador."
    )

    # 🔗 Relacion con `ControllerDevice`
    controller_device_id: int = Field(
        foreign_key="controller_devices.id",
        ondelete="CASCADE",
        description="Dispositivo de control al que pertenece el actuador."
    )

    controller_device: "ControllerDevice" = Relationship(
        back_populates="actuators"
    )

    # 🔗 Relacion con `ActuatorModel`
    actuator_model_id: int | None = Field(
        default=None,
        foreign_key="actuator_models.id",
        description="Modelo del actuador.",
        ondelete="SET NULL"
    )

    model: ActuatorModel | None = Relationship(
        back_populates="actuators"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 42. 🤖 bot_users
# ---------------------------------------------------------------------------
class BotUser(TlalocDB_Base, table=True):
    """
    Tabla: bot_users
    Usuarios finales que interactúan con los bots a través de Telegram.
    """
    __tablename__ = "bot_users"
    metadata = metadata

    # 🔑 PK
    id: int = Field(
        primary_key=True,
        description="Identificador único del usuario de bot."
    )

    # 📌 Información de Telegram
    telegram_username: str = Field(
        unique=True,
        nullable=False,
        max_length=50,
        description="Username de Telegram del usuario (ej: @usuario123)."
    )

    telegram_user_id: Optional[int] = Field(
        default=None,
        unique=True,
        description="ID numérico de Telegram del usuario."
    )

    # ⚙️ Estado
    is_active: bool = Field(
        default=True,
        description="Indica si el usuario está activo."
    )

    # 🔗 Relación con `Employee`
    employee_id: int = Field(
        foreign_key="employees.id",
        unique=True,
        ondelete="CASCADE",
        description="Empleado asociado al usuario de bot (1:1).",
    )

    employee: Employee = Relationship(
        back_populates="bot_user",
        sa_relationship_kwargs={"uselist": False}
    )

    # 🔗 Relación con `Subscription`
    subscriptions: list["Subscription"] = Relationship(
        back_populates="bot_users",
        link_model=BotUserSubscriptionLink,
    )

    # 🔗 Relación con `UserProcess`
    process_links: list["UserProcess"] = Relationship(
        back_populates="bot_user",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 43. 👤 user_processes
# ---------------------------------------------------------------------------
class UserProcess(TlalocDB_Base, table=True):
    """
    Tabla: user_processes
    Procesos asignados a un usuario de bot.
    Cada vínculo indica qué procesos de negocio puede operar (o vigilar) un usuario.
    """
    __tablename__ = "user_processes"
    metadata = metadata

    # 🔑 PK
    id: int = Field(
        primary_key=True,
        description="Identificador único del vínculo usuario ↔ proceso."
    )

    # ⚙️ Estado
    is_active: bool = Field(
        default=True,
        description="Indica si el vínculo está activo."
    )

    # 🔗 Relación con `BotUser`
    bot_user_id: int = Field(
        foreign_key="bot_users.id",
        ondelete="CASCADE",
        description="Usuario del bot al que se asigna el proceso."
    )

    bot_user: BotUser = Relationship(
        back_populates="process_links"
    )

    # 🔗 Relación con `Process`
    process_id: int = Field(
        foreign_key="processes.id",
        ondelete="CASCADE",
        description="Proceso asignado al usuario.",
    )

    process: Process = Relationship(
        back_populates="user_links"
    )

    # 🔗 Relación con `UserProcessPermission`
    permissions: list["UserProcessPermission"] = Relationship(
        back_populates="user_processes",
        link_model=UserProcessPermissionLink
    )

    # 📌 Evita que un mismo proceso se asigne dos veces al mismo usuario
    __table_args__ = (
        UniqueConstraint(
            "bot_user_id",
            "process_id",
            name="uq_user_processes_user_process"
        ),
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 44. ⚙️ bot_processes
# ---------------------------------------------------------------------------
class BotProcess(TlalocDB_Base, table=True):
    """
    Tabla: bot_processes
    Procesos operativos administrados por un bot dentro de una suscripción específica.
    Cada fila enlaza un proceso de negocio con la suscripción activa que lo ejecuta.
    """
    __tablename__ = "bot_processes"
    metadata = metadata

    # 🔑 PK
    id: int = Field(
        primary_key=True,
        description="Identificador único del vínculo bot ↔ proceso."
    )

    # ⚙️ Estado
    is_active: bool = Field(
        default=True,
        nullable=False,
        description="Indica si el vínculo está activo."
    )

    # 🔗 Relacion con `Subscription`
    subscription_id: int = Field(
        foreign_key="subscriptions.id",
        ondelete="CASCADE",
        description="Suscripción a la que pertenece el proceso."
    )

    subscription: Subscription = Relationship(
        back_populates="process_links"
    )

    # 🔗 Relación con `Process`
    process_id: int = Field(
        foreign_key="processes.id",
        ondelete="CASCADE",
        description="Proceso asociado al bot dentro de la suscripción."
    )

    process: Process = Relationship(
        back_populates="subscription_links"
    )

    # 🔗 Relación con `BotProcessPermission`
    permissions: list["BotProcessPermission"] = Relationship(
        back_populates="bot_processes",
        link_model=BotProcessPermissionLink
    )

    # 📌 Restricciones adicionales
    __table_args__ = (
        UniqueConstraint(
            "subscription_id",
            "process_id",
            name="uq_bot_processes_subscription_process"
        ),
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

#  ╭──────────────────────────────────────────────────────╮
#  │ 💰 6. Facturación y pagos                            │
#  ╰──────────────────────────────────────────────────────╯
# ---------------------------------------------------------------------------
# 45. 📅 subscription_periods
# ---------------------------------------------------------------------------
class SubscriptionPeriod(TlalocDB_Base, table=True):
    """
    Tabla: subscription_periods
    Periodos de facturación pertenecientes a una suscripción.
    Cada fila resume el plan en vigor durante ese intervalo,
    así como su snapshot comercial para histórico de precios y límites.
    """
    __tablename__ = "subscription_periods"
    metadata = metadata

    # 🔑 PK
    id: int = Field(
        primary_key=True,
        description="Identificador único del periodo de suscripción."
    )

    # 📅 Intervalo de facturación
    period_start: datetime = Field(
        description="Inicio del periodo de facturación."
    )
    period_end: datetime = Field(
        description="Fin del periodo de facturación (debe ser mayor que period_start)."
    )

    # 📦 Snapshot comercial del plan
    plan_snapshot: dict[str, Any] = Field(
        default_factory=dict,
        description="Snapshot JSON del plan en vigor durante el periodo.",
        sa_column=Column(JSONB, server_default=text("'{}'::jsonb"), nullable=False),
    )

    # 🔗 Relación con `Subscription`
    subscription_id: int = Field(
        foreign_key="subscriptions.id",
        ondelete="CASCADE",
        description="Suscripción a la que pertenece el periodo.",
    )

    subscription: Subscription = Relationship(
        back_populates="periods"
    )

    # 🔗 Relación con `Invoice`
    invoice: "Invoice" = Relationship(
        back_populates="subscription_period",
        passive_deletes="all",
        sa_relationship_kwargs={"uselist": False}
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

    # ✅ Validación cross-field
    @classmethod
    def validate_dates(cls, values):
        start, end = values.get("period_start"), values.get("period_end")
        if start and end and end <= start:
            raise ValueError("period_end debe ser mayor que period_start")
        return values

# ---------------------------------------------------------------------------
# 46. 🧾 invoices
# ---------------------------------------------------------------------------
class Invoice(TlalocDB_Base, table=True):
    """
    Tabla: invoices
    Facturas emitidas para cada periodo de suscripción.
    Contiene montos, fechas clave y estado de cobranza.
    """
    __tablename__ = "invoices"
    metadata = metadata

    # 🔑 PK
    id: int = Field(
        primary_key=True,
        description="Identificador único de la factura."
    )

    # 📌 Identificación y monto
    invoice_number: str = Field(
        unique=True,
        max_length=50,
        description="Número de factura único (no vacío)."
    )

    amount_due: Decimal = Field(
        description="Monto total a pagar en la factura."
    )

    currency: str = Field(
        default="COP",
        max_length=3,
        description="Moneda de la factura en formato ISO 4217 (ej: COP, USD)."
    )

    # 📅 Fechas clave
    issued_at: datetime | None = Field(
        default=None,
        description="Fecha de emisión (la BD lo completa con DEFAULT now())."
    )
    due_date: datetime = Field(
        description="Fecha de vencimiento de la factura."
    )

    # 🔗 Relación con `InvoiceStatus`
    invoice_status_id: int | None = Field(
        default=None,
        foreign_key="invoice_statuses.id",
        ondelete="RESTRICT",
        description="Estado actual de la factura."
    )

    status: Optional["InvoiceStatus"] = Relationship(
        back_populates="invoices",
        sa_relationship_kwargs={"uselist": False}
    )

    # 🔗 Relación con `SubscriptionPeriod`
    subscription_period_id: int = Field(
        unique=True,
        foreign_key="subscription_periods.id",
        ondelete="CASCADE",
        description="Periodo de suscripción facturado (1:1).",
    )

    subscription_period: SubscriptionPeriod = Relationship(
        back_populates="invoice",
        sa_relationship_kwargs={"uselist": False}
    )

    # 🔗 Relación con `Payment`
    payments: list["Payment"] = Relationship(
        back_populates="invoice",
        passive_deletes="all"
    )

    # 🔗 Relación con `PaymentAttempt`
    payment_attempts: list["PaymentAttempt"] = Relationship(
        back_populates="invoice",
        passive_deletes="all"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 47. 💳 payments
# ---------------------------------------------------------------------------
class Payment(TlalocDB_Base, table=True):
    """
    Tabla: payments
    Pagos registrados para saldar facturas.
    """
    __tablename__ = "payments"
    metadata = metadata

    # 🔑 PK
    id: int = Field(primary_key=True)

    # 💰 Información del pago
    amount: Decimal = Field(
        ge=0,
        description="Monto del pago (NUMERIC(10,2) en BD).",
    )
    currency: str = Field(
        default="COP",
        description="Moneda ISO 4217 (CHAR(3)).",
    )

    # 🕒 Fecha del pago (DEFAULT now() en BD)
    paid_at: datetime | None = Field(
        default=None,
        description="Fecha/hora del pago; la BD la pone con DEFAULT now().",
    )

    # 🔐 Identificador del proveedor (único y no vacío)
    provider_transaction_id: str = Field(
        unique=True,
        min_length=1,
        max_length=100,
        description="ID de la transacción en el proveedor de pagos (UNIQUE).",
    )

    # 🔗 Relación con la factura (ON DELETE CASCADE)
    invoice_id: int = Field(
        foreign_key="invoices.id",
        ondelete="CASCADE",
        description="Factura asociada al pago."
    )

    invoice: "Invoice" = Relationship(
        back_populates="payments"
    )

    # 🔗 Relación con `PaymentMethod`
    payment_method_id: int = Field(
        foreign_key="payment_methods.id",
        ondelete="RESTRICT",
        description="Método utilizado para el pago."
    )

    method: "PaymentMethod" = Relationship(
        back_populates="payments"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

# ---------------------------------------------------------------------------
# 48. 🔁 payment_attempts
# ---------------------------------------------------------------------------
class PaymentAttempt(TlalocDB_Base, table=True):
    """
    Tabla: payment_attempts
    Registro de cada intento de pago asociado a una factura.
    """
    __tablename__ = "payment_attempts"
    __table_args__ = (
        UniqueConstraint("invoice_id", "attempt_no", name="uq_payment_attempts_invoice_attemptno"),
    )
    metadata = metadata

    # 🔑 PK
    id: int = Field(primary_key=True)

    # 🔢 Nº de intento (>= 1)
    attempt_no: int = Field(
        ge=1,
        description="Número de intento para la factura (1, 2, 3, ...)."
    )

    # 📝 Mensaje devuelto por el procesador
    message: str = Field(
        min_length=1,
        description="Mensaje/Descripción del procesador o del intento."
    )

    # 🔖 Código/respuesta del procesador (no vacío, máx 50)
    response_code: str = Field(
        min_length=1,
        max_length=50,
        description="Código de respuesta del proveedor."
    )

    # ✅ Marcador de intento final
    is_final: bool = Field(
        default=False,
        description="Indica si este intento cierra el flujo (sin más reintentos)."
    )

    # 🕒 Fecha del intento (DEFAULT now() en BD)
    attempted_at: datetime | None = Field(
        default=None,
        description="Momento del intento; la BD lo completa con DEFAULT now()."
    )

    # 🔗 Relación con `PaymentMethod`
    payment_method_id: int | None = Field(
        default=None,
        foreign_key="payment_methods.id",
        ondelete="RESTRICT",
        description="Método usado en el intento."
    )

    method: Optional["PaymentMethod"] = Relationship(
        back_populates="payment_attempts"
    )

    # 🔗 Relación con `Invoice`
    invoice_id: int = Field(
        foreign_key="invoices.id",
        ondelete="CASCADE",
        description="Factura asociada al intento."
    )

    invoice: "Invoice" = Relationship(
        back_populates="payment_attempts"
    )

    # 🔗 Relación con `PaymentStatus`
    payment_status_id: int | None = Field(
        default=None,
        foreign_key="payment_statuses.id",
        ondelete="RESTRICT",
        description="Estado reportado para el intento."
    )

    status: Optional["PaymentStatus"] = Relationship(
        back_populates="payments_attempts"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
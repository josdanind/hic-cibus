# Habilita anotaciones de tipo diferido para evitar problemas de dependencias circulares.
from __future__ import annotations

# Librería estándar
from datetime import datetime, timezone

# ORMs
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import UniqueConstraint, func, MetaData

# Utilidades de la aplicación
from app.utils.regex import E164_PHONE_RE, TELEGRAM_USERNAME_RE, EMAIL_RE

metadata = MetaData()

# ───────────────────────────────────────────────
# 📚 Catálogos Puros
# ───────────────────────────────────────────────
# ---------------------------------------------------------------------------
# 1. Role
# ---------------------------------------------------------------------------
class Role(SQLModel, table=True):
    """
    Define los roles que pueden asignarse a empleados dentro de una empresa.

    📌 Ejemplo de roles:
    - Responsable legal
    - Responsable de ventas
    - Responsable de soporte técnico

    Este modelo permite la asignación de un rol único por empleado, pero un mismo
    rol puede ser compartido por múltiples empleados.
    """
    __tablename__ = "roles"
    metadata = metadata

    # 🔑 Identificador único del rol
    id: int | None = Field(default=None, primary_key=True)

    # 📛 Nombre del rol (debe ser único)
    name: str = Field(
        max_length=50,
        unique=True,
        description="Ej: 'Responsable de ventas'"
    )

    # 📝 Descripción del rol
    description: str | None = Field(
        default=None,
        description="Descripción opcional del rol."
    )

    # 🔗 Relación con `Employee` (un rol puede tener muchos empleados asignados)
    employees: list[Employee] = Relationship(
        back_populates="role",
        passive_deletes="all"
    )


# ---------------------------------------------------------------------------
# 2. BotUserPermission
# ---------------------------------------------------------------------------
class BotUserPermission(SQLModel, table=True):
    """
    🔐 Define un conjunto de permisos que puede tener un usuario de bot.

    Ejemplos: viewer, editor, admin, owner.
    """
    __tablename__ = "bot_user_permissions"
    metadata = metadata

    # 🔑 Identificador
    id: int | None = Field(default=None, primary_key=True)

    # Campos de información
    name: str = Field(
        max_length=50,
        unique=True,
        description="Nombre del permiso (ej: 'viewer', 'admin')"
    )
    description: str | None = Field(
        default=None,
        description="Descripción del permiso y sus alcances"
    )

    # Relación con `BotUser` (Cada permiso puede ser asignado a varios usuarios)
    users: list[BotUser] = Relationship(
        back_populates="permission",
        passive_deletes="all"
    )


# ---------------------------------------------------------------------------
# 3. BotEnvironment
# ---------------------------------------------------------------------------
class BotEnvironment(SQLModel, table=True):
    """🌐 Entorno donde se ejecuta un :class:`Bot` (producción, desarrollo, etc.)."""

    __tablename__ = "bot_environments"
    metadata = metadata

    # 🔑 Identificador único del entorno
    id: int | None = Field(default=None, primary_key=True)

    # 📛 Nombre del entorno
    name: str = Field(
        max_length=50,
        unique=True,
        description="Nombre único del entorno (ej: 'producción', 'desarrollo')"
    )
    description: str | None = Field(
        default=None,
        description="Descripción detallada del entorno (uso, restricciones, etc.)"
    )

    # Relaciones
    bots: list[Bot] = Relationship(
        back_populates="environment",
        passive_deletes="all"
    )

# ---------------------------------------------------------------------------
# 4. BotStatus
# ---------------------------------------------------------------------------
class BotStatus(SQLModel, table=True):
    """
    ⚙️ Representa el estado operativo de un bot.

    Ejemplos comunes: 'operativo', 'en mantenimiento', 'apagado', 'en espera'.
    """
    __tablename__ = "bot_statuses"
    metadata = metadata

    # 🔑 Identificador
    id: int | None = Field(default=None, primary_key=True)

    # 📛 Nombre del estado
    name: str = Field(
        max_length=50,
        unique=True,
        description="Nombre único del estado del bot (ej: 'operativo', 'apagado')"
    )
    description: str | None = Field(
        default=None,
        description="Detalles adicionales sobre el estado"
    )

    # 🔗 Relación con bots que tienen este estado
    bots: list[Bot] = Relationship(
        back_populates="status",
        passive_deletes="all"
    )


# ---------------------------------------------------------------------------
# 5. BotModelStatus
# ---------------------------------------------------------------------------
class BotModelStatus(SQLModel, table=True):
    """
    ⚙️ Representa el estado actual de un modelo de bot.

    Ejemplos comunes: 'en desarrollo', 'en producción', 'obsoleto'.
    """
    __tablename__ = "bot_model_statuses"
    metadata = metadata

    # 🔑 Identificador
    id: int | None = Field(default=None, primary_key=True)

    # 📛 Nombre del estado
    name: str = Field(
        max_length=50,
        unique=True,
        description="Nombre del estado (ej: 'producción', 'desarrollo', 'obsoleto')"
    )
    # 📝 Descripción extendida (opcional)
    description: str | None = Field(
        default=None,
        description="Detalles adicionales del estado del modelo"
    )

    # 🔗 Relaciones con `BotModel` (Cada estado puede tener varios modelos de bot)
    bot_models: list[BotModel] = Relationship(
        back_populates="status",
        passive_deletes="all"
    )


# ---------------------------------------------------------------------------
# 6. PaymentStatus
# ---------------------------------------------------------------------------
class PaymentStatus(SQLModel, table=True):
    """Estado de un pago (pendiente, completado, cancelado…)."""

    __tablename__ = "payment_statuses"
    metadata = metadata

    # 🔑 Identificador
    id: int | None = Field(default=None, primary_key=True)

    # 📛 Nombre del estado
    name: str = Field(
        max_length=50,
        unique=True
    )
    description: str | None = Field(default=None)

    # Relación con `SubscriptionPayment` (Cada estado puede tener varios pagos asociados)
    payments: list[SubscriptionPayment] = Relationship(
        back_populates="status",
        passive_deletes="all"
    )


# ---------------------------------------------------------------------------
# 7. SubscriptionStatus
# ---------------------------------------------------------------------------
class SubscriptionStatus(SQLModel, table=True):
    """
    📦 Representa un estado posible para una suscripción de bot

    📌 Ejemplo:
    - Activa
    - Suspendida
    - Cancelada
    """
    __tablename__ = "subscription_statuses"
    metadata = metadata

    # 🔑 Identificador único del estado
    id: int | None = Field(default=None, primary_key=True)

    # 🏷️ Nombre único del estado
    name: str = Field(
        max_length=50,
        unique=True,
        description="Nombre único del estado (ej: 'activa', 'cancelada')"
    )

    # 📝 Descripción opcional del estado
    description: str | None = Field(
        default=None,
        max_length=255,
        description="Descripción adicional sobre el estado de suscripción"
    )

    # Relación con `Subscription` (Cada estado puede tener varias suscripciones)
    subscriptions: list[Subscription] = Relationship(
        back_populates="status",
        passive_deletes="all"
    )


# ---------------------------------------------------------------------------
# 8. SubscriptionPeriod
# ---------------------------------------------------------------------------
class SubscriptionPeriod(SQLModel, table=True):
    """
    📆 Representa la periodicidad de facturación de una suscripción.

    Ejemplos: 'mensual', 'trimestral', 'anual'.
    """
    __tablename__ = "subscription_periods"
    metadata = metadata

    # 🔑 Identificador
    id: int | None = Field(default=None, primary_key=True)

    # 🏷️ Nombre único del período
    name: str = Field(
        max_length=50,
        unique=True,
        description="Nombre único del período (ej: 'mensual', 'anual')"
    )

    # 📝 Descripción opcional
    description: str | None = Field(
        default=None,
        description="Descripción extendida del período de suscripción"
    )

    # Relación con `Subscription` (Cada período de facturación puede tener varias suscripciones)
    subscriptions: list[Subscription] = Relationship(
        back_populates="period",
        passive_deletes="all"
    )


# ───────────────────────────────────────────────
# 🔗 Tabla de unión M‑N
# ───────────────────────────────────────────────
# ---------------------------------------------------------------------------
# 9. BotCategoryLink
# ---------------------------------------------------------------------------
class BotCategoryLink(SQLModel, table=True):
    """
    🔗 Tabla de relación entre bots y categorías.

    Permite asignar múltiples categorías a un bot y viceversa.
    """
    __tablename__ = "bot_category_link"
    metadata = metadata

    # 🔑 Clave compuesta (bot + categoría)
    bot_id: int = Field(
        primary_key=True,
        foreign_key="bots.id",
        ondelete="CASCADE",
        description="ID del bot asociado a esta categoría"
    )
    category_id: int = Field(
        primary_key=True,
        foreign_key="bot_categories.id",
        ondelete="CASCADE",
        description="ID de la categoría asociada al bot"
    )


# ───────────────────────────────────────────────
# 🔗 Catálogo Dependiente de unión
# ───────────────────────────────────────────────
# ---------------------------------------------------------------------------
# 10. BotCategory
# ---------------------------------------------------------------------------
class BotCategory(SQLModel, table=True):
    """
    🗂️ Representa una categoría funcional a la que puede pertenecer un bot.

    Ejemplos: 'monitoreo', 'ventas', 'atención al cliente', 'agricultura'.
    """
    __tablename__ = "bot_categories"
    metadata = metadata

    # 🔑 Identificador único de la categoría
    id: int | None = Field(default=None, primary_key=True)

    # 📛 Nombre único de la categoría
    name: str = Field(
        max_length=50,
        unique=True,
        description="Nombre único de la categoría (ej: 'monitoreo')"
    )
    description: str | None = Field(
        default=None,
        description="Descripción general de la categoría"
    )

    # 🔗 Relación con bots (muchos a muchos)
    bots: list[Bot] = Relationship(
        back_populates="categories",
        link_model=BotCategoryLink,
        cascade_delete=True
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )


# ───────────────────────────────────────────────
# 🗄️ Núcleo de la base de datos
# ───────────────────────────────────────────────
# ---------------------------------------------------------------------------
# 11. Employee
# ---------------------------------------------------------------------------
class Employee(SQLModel, table=True):
    """
    📌 Representa a una persona empleada en una empresa.

    Incluye datos personales como nombre, correo, teléfono y su rol asignado.
    Además, cada empleado puede ser un contacto de una empresa o un usuario de bot.
    """
    __tablename__ = "employees"
    metadata = metadata

    # 🔑 Identificador único del empleado
    id: int | None = Field(default=None, primary_key=True)

    # 🧍 Información personal
    first_name: str = Field(
        max_length=50,
        index=True,
        description="Primer nombre del empleado"
    )
    middle_name: str | None = Field(
        default=None,
        max_length=50,
        description="Segundo nombre del empleado (opcional)"
    )
    last_name: str = Field(
        max_length=50,
        index=True,
        description="Primer apellido del empleado"
    )
    second_last_name: str | None = Field(
        default=None,
        max_length=50,
        description="Segundo apellido del empleado (opcional)"
    )
    mobile_phone: str = Field(
        max_length=15,
        regex=E164_PHONE_RE,
        unique=True,
        description="Teléfono móvil del empleado"
    )
    email: str = Field(
        max_length=50,
        regex=EMAIL_RE,
        unique=True,
        description="Correo electrónico del empleado"
    )
    position: str | None = Field(
        default=None,
        max_length=50,
        description="Cargo u ocupación dentro de la empresa"
    )

    # 🔗 Relación con `Role` (Cada empleado se le asigna un único rol)
    role_id: int | None = Field(
        default=None,
        foreign_key="roles.id",
        ondelete="SET NULL"
    )
    role: Role | None = Relationship(back_populates="employees")

    # 🔗 Relación con `Company` (Cada empleado pertenece a una única empresa)
    company_id: int = Field(
        foreign_key="companies.id",
        ondelete="CASCADE",
        description="ID de la empresa a la que pertenece el empleado"
    )
    company: Company = Relationship(back_populates="employees")

    # 🔗 Relación con `CompanyContact` (Cada empleado es un contacto de la empresa)
    company_contact: CompanyContact | None = Relationship(
        back_populates="employee",
        sa_relationship_kwargs={"uselist": False},
        cascade_delete=True
    )

    # 🔗 Relación con `BotUser` (Cada empleado puede ser un usuario de bot)
    bot_user: BotUser | None = Relationship(
        back_populates="employee",
        sa_relationship_kwargs={"uselist": False},
        cascade_delete=True
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )


# ---------------------------------------------------------------------------
# 12. Company
# ---------------------------------------------------------------------------
class Company(SQLModel, table=True):
    """
    Empresa cliente que contrata bots y gestiona empleados.

    Incluye información como contacto, estado, ubicación y relaciones con contactos,
    usuarios de bot y suscripciones.

    Atributos:
        id (int | None): Identificador único. Clave primaria.
        name (str): Nombre único de la empresa.
        description (str | None): Descripción general.
        is_active (bool): Indica si está activa. Por defecto True.
        phone (str): Teléfono de contacto.
        email (str): Correo electrónico único y válido.
        website (str | None): Sitio web.
        country, city, state, zip_code, address (str | None): Ubicación.
        contacts (list[CompanyContact]): Contactos asociados.
        bot_users (list[BotUser]): Usuarios de bot asociados.
        bot_subscriptions (list[Subscription]): Suscripciones a bots.
        created_at, updated_at (datetime): Timestamps de creación y actualización.

    Relaciones:
        - Múltiples contactos (`CompanyContact`).
        - Múltiples usuarios de bot (`BotUser`).
        - Múltiples suscripciones (`Subscription`).
    """
    __tablename__ = "companies"
    metadata = metadata

    # 🔑 Identificador único de la empresa
    id: int | None = Field(default=None, primary_key=True)

    # 🏢 Información de la empresa
    name: str = Field(
        max_length=50,
        unique=True,
        description="Nombre único de la empresa"
    )
    description: str | None = Field(
        default=None,
        description="Descripción general de la empresa"
    )
    is_active: bool = Field(
        default=True,
        index=True,
        description="Indica si la empresa está activa"
    )

    # ☎️ Información de contacto
    phone: str = Field(
        max_length=20,
        description="Número de contacto de la empresa"
    )
    email: str = Field(
        max_length=50,
        regex=EMAIL_RE,
        unique=True,
        description="Correo electrónico de la empresa"
    )
    website: str | None = Field(
        default=None,
        max_length=100,
        description="Sitio web de la empresa"
    )

    # 🌍 Ubicación
    country: str | None = Field(default=None, max_length=50)
    city: str | None = Field(default=None, max_length=50)
    state: str | None = Field(default=None, max_length=50)
    zip_code: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=255)

    # 🔗 Relación con `Employee` (Una empresa tiene varios empleados)\
    employees: list[Employee] = Relationship(
        back_populates="company",
        cascade_delete=True
    )

    # 🔗 Relaciones con `Subscription` (Cada empresa puede tener varias suscripciones a bots)
    bot_subscriptions: list[Subscription] = Relationship(
        back_populates="company",
        cascade_delete=True
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )


# ---------------------------------------------------------------------------
# 13. CompanyContact
# ---------------------------------------------------------------------------
class CompanyContact(SQLModel, table=True):
    """Empleado designado como contacto para una :class:`Company`."""

    __tablename__ = "company_contacts"
    metadata = metadata

    # 🔑 Identificador único del contacto
    id: int | None = Field(default=None, primary_key=True)

    # ✅ Información del contacto
    is_primary: bool = Field(
        default=False,
        description="Indica si es el contacto principal de la empresa"
    )
    notes: str | None = Field(
        default=None,
        description="Notas adicionales sobre el contacto"
    )

    # 🔗 Relación con `Employee` (Un contacto es un empleado)
    employee_id: int = Field(
        foreign_key="employees.id",
        ondelete="CASCADE",
        unique=True,
        description="Empleado asignado como contacto"
    )
    employee: Employee = Relationship(
        back_populates="company_contact",
        sa_relationship_kwargs={"uselist": False}
    )


# ---------------------------------------------------------------------------
# 14. BotModel
# ---------------------------------------------------------------------------
class BotModel(SQLModel, table=True):
    """
    🤖 Representa un modelo funcional de bot.

    Ejemplos: 'Tlaloc V1.0', 'Quetzalcoatl V2.1'.
    Incluye su versión, descripción y estado de desarrollo.
    """
    __tablename__ = "bot_models"
    metadata = metadata

    # 🔑 Identificador
    id: int | None = Field(default=None, primary_key=True)

    # 📛 Información del modelo
    name: str = Field(
        max_length=50,
        unique=True,
        description="Nombre único del modelo (ej: 'Tlaloc V1.0')"
    )
    description: str | None = Field(
        default=None,
        description="Descripción funcional del modelo de bot"
    )
    version: str = Field(
        max_length=50,
        description="Versión del modelo (ej: 'v1.0', '2.3.1')"
    )

    # 🔗 Relación con `BotModelStatus` (Cada modelo tiene un único estado)
    status_id: int | None = Field(
        default=None,
        foreign_key="bot_model_statuses.id",
        ondelete="SET NULL",
        description="Estado actual del modelo de bot"
    )
    status: BotModelStatus = Relationship(back_populates="bot_models")

    # Relación con `Bot` (Cada modelo tiene varios bots)
    bots: list[Bot] = Relationship(
        back_populates="bot_model",
        cascade_delete=True
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )


# ---------------------------------------------------------------------------
# 15. Bot
# ---------------------------------------------------------------------------
class Bot(SQLModel, table=True):
    """
    🤖 Representa un bot dentro del sistema, vinculado a una empresa y un modelo de operación.

    Cada bot cuenta con su URL de API, configuración activa y relaciones con usuarios y suscripciones.
    """
    __tablename__ = "bots"
    metadata = metadata

    # 🔑 Identificador
    id: int | None = Field(default=None, primary_key=True)

    # 📛 Información general
    name: str = Field(
        max_length=50,
        unique=True,
        description="Nombre único del bot (ej: 'Tlaloc', 'Quetzalcoatl')"
    )
    description: str | None = Field(
        default=None,
        description="Descripción funcional del bot"
    )
    api_url: str = Field(
        max_length=255,
        unique=True,
        description="URL base para acceder a la API del bot"
    )
    is_active: bool = Field(
        default=True,
        index=True,
        description="Estado de activación del bot"
    )
    last_ping: datetime | None = Field(
        default=None,
        description="Última vez que el bot respondió a una verificación (ping)"
    )
    request_per_minute: int = Field(
        default=0,
        index=True,
        description="Número máximo de solicitudes permitidas por minuto"
    )
    data: dict | None = Field(
        default=None,
        sa_column=Column(JSON),
        description="Datos adicionales del bot en formato JSON (configuración, estado, etc.)"
    )

    # 🔗 Relaciones con BotCredential (Cada bot tiene un único conjunto de credenciales)
    credentials: BotCredential | None = Relationship(
        back_populates="bot",
        cascade_delete=True,
        sa_relationship_kwargs={"uselist": False}
    )

    # 🔗 Relación con `BotModel` (Cada bot tiene un único modelo)
    bot_model_id: int = Field(
        foreign_key="bot_models.id",
        ondelete="CASCADE",
        description="ID del modelo de bot asociado"
    )
    bot_model: BotModel = Relationship(back_populates="bots")

    # 🔗 Relación con `BotStatus` (Cada bot tiene un único estado)
    status_id: int | None = Field(
        default=None,
        foreign_key="bot_statuses.id",
        ondelete="SET NULL",
        index=True,
        description="Estado actual del bot (ej: activo, en mantenimiento)"
    )
    status: BotStatus = Relationship(back_populates="bots")

    # 🔗 Relación con `BotEnvironment` (Cada bot corre en un único entorno)
    environment_id: int | None = Field(
        default=None,
        foreign_key="bot_environments.id",
        ondelete="SET NULL",
        description="Entorno en el que corre el bot (ej: producción, desarrollo)"
    )
    environment: BotEnvironment = Relationship(back_populates="bots")

    # 🔗 Relación con `BotCategory` (Cada bot puede tener varias categorías)
    categories: list[BotCategory] = Relationship(
        back_populates="bots",
        link_model=BotCategoryLink,
        cascade_delete=True
    )

    # 🔗 Relación con `Subscription` (Cada bot puede estar vinculado a varias empresas)
    company_subscriptions: list[Subscription] = Relationship(
        back_populates="bot",
        cascade_delete=True
    )

    # 🔗 Relación con `UserBotLink` (Cada bot puede tener varios enlaces a usuarios)
    user_links: list[UserBotLink] = Relationship(
        back_populates="bot",
        cascade_delete=True
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )


# ---------------------------------------------------------------------------
# 16. BotCredential
# ---------------------------------------------------------------------------
class BotCredential(SQLModel, table=True):
    """
    🔐 Almacena las credenciales de autenticación de un bot.

    Incluye contraseñas cifradas y tokens para comunicación segura entre servicios.
    """
    __tablename__ = "bot_credentials"
    metadata = metadata

    # 🔑 Identificador
    id: int | None = Field(default=None, primary_key=True)

    # 🔒 Credenciales cifradas
    hashed_password: str = Field(
        max_length=255,
        description="Contraseña cifrada para autenticación interna del bot"
    )
    hashed_telegram_bot_token: str | None = Field(
        default=None,
        max_length=255,
        description="Token cifrado del bot de Telegram (opcional)"
    )
    hashed_api_access_token: str | None = Field(
        default=None,
        max_length=255,
        description="Token cifrado para acceso externo vía API"
    )

    # 🔗 Relación 1:1 con `Bot`
    bot_id: int = Field(
        foreign_key="bots.id",
        unique=True,
        ondelete="CASCADE",
        description="ID del bot al que pertenecen estas credenciales"
    )
    bot: Bot | None = Relationship(
        back_populates="credentials",
        sa_relationship_kwargs={"uselist": False}
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )


# ---------------------------------------------------------------------------
# 17. BotUser
# ---------------------------------------------------------------------------
class BotUser (SQLModel, table=True):
    """
    🤖 Representa a un usuario (empleado de una empresa) que interactúa con un bot.

    Cada bot user está vinculado a un empleado, una empresa y puede tener permisos específicos.    
    """
    __tablename__ = "bot_users"
    metadata = metadata

    # 🔑 Identificador
    id: int | None = Field(default=None, primary_key=True)

    # Campos de información
    telegram_username: str = Field(
        max_length=50,
        regex=TELEGRAM_USERNAME_RE,
        unique=True,
        description="Nombre de usuario único en Telegram (sin @)"
    )

    telegram_user_id: int | None = Field(
        default=None,
        unique=True,
        description="ID numérico único asignado por Telegram"
    )
    is_active: bool = Field(
        default=True,
        description="Indica si el usuario está activo en la plataforma"
    )

    # 🔗 Relación 1:1 con `Employee`
    employee_id: int = Field(
        foreign_key="employees.id",
        ondelete="CASCADE",
        unique=True,
        description="Empleado asociado a este usuario de bot"
    )
    employee: Employee = Relationship(
        back_populates="bot_user",
        sa_relationship_kwargs={"uselist": False}
    )

    # 🔗 Relación con `BotUserPermission` (Cada usuario se le asigna un único permiso)
    permissions_id: int | None = Field(
        default=None,
        foreign_key="bot_user_permissions.id",
        ondelete="SET NULL",
        description="Permisos asignados al usuario"
    )
    permission: BotUserPermission = Relationship(
        back_populates="users"
    )

    # 🔗 Relación con `UserBotLink` (Un usuario puede acceder a varios bots)
    bot_links: list[UserBotLink] = Relationship(
        back_populates="user",
        cascade_delete=True
    )


# ───────────────────────────────────────────────
# 🔗 Tabla de unión M‑N
# ───────────────────────────────────────────────
# ---------------------------------------------------------------------------
# 18. UserBotLink
# ---------------------------------------------------------------------------
class UserBotLink(SQLModel, table=True):
    """
    🔗 Representa el acceso de un usuario a un bot específico.

    Se usa para controlar los vínculos entre múltiples usuarios y múltiples bots,
    así como su historial de acceso y revocación.
    """
    __tablename__ = "user_bot_link"
    metadata = metadata

    # 🔑 Claves compuestas
    # 🔗 Relación con `BotUser` (Cada enlace pertenece a un único usuario de bot)
    user_id: int = Field(
        foreign_key="bot_users.id",
        primary_key=True,
        ondelete="CASCADE",
        description="ID del usuario que tiene acceso al bot"
    )
    user: BotUser = Relationship(
        back_populates="bot_links"
    )

    # 🔗 Relación con `Bot` (Cada enlace pertenece a un único bot)
    bot_id: int = Field(
        foreign_key="bots.id",
        primary_key=True,
        ondelete="CASCADE",
        description="ID del bot al que el usuario tiene acceso"
    )
    bot: Bot = Relationship(
        back_populates="user_links"
    )

    # ✅ Control de acceso
    can_access: bool = Field(
        default=True,
        description="¿El usuario tiene acceso activo?"
    )
    granted_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()},
        description="Fecha-hora en que se otorgó el acceso",
    )
    revoked_at: datetime | None = Field(
        default=None,
        description="Fecha-hora en que se revocó el acceso (NULL = vigente)",
    )


# ───────────────────────────────────────────────
# 🔄 Transaccionales
# ───────────────────────────────────────────────
# ---------------------------------------------------------------------------
# 19. Subscription
# ---------------------------------------------------------------------------
class Subscription(SQLModel, table=True):
    """
    🔄 Representa una suscripción activa o histórica a un bot por parte de una empresa.
    Permite gestionar el estado de la suscripción, fechas de pago y detalles de la empresa.
    """
    __tablename__ = "subscriptions"
    metadata = metadata
    __table_args__ = (
        # Definición de un índice único compuesto por bot_id y company_id
        UniqueConstraint("bot_id", "company_id", name="uq_bot_company"),
    )

    # 🔑 Identificador único de la suscripción
    id: int | None = Field(default=None, primary_key=True)

    # ⚙️ Configuración de la suscripción
    is_active: bool = Field(
        default=True,
        index=True,
        description="Indica si la suscripción está actualmente activa"
    )
    max_users: int = Field(
        default=1,
        index=True,
        description="Número máximo de usuarios permitidos en esta suscripción"
    )
    start_date: datetime | None = Field(
        default=None,
        index=True,
        description="Fecha de inicio de la suscripción"
    )
    end_date: datetime | None = Field(
        default=None,
        index=True,
        description="Fecha de finalización de la suscripción"
    )
    next_payment_date: datetime | None = Field(
        default=None,
        index=True,
        description="Fecha del siguiente pago programado"
    )
    last_payment_date: datetime | None = Field(
        default=None,
        index=True,
        description="Fecha del último pago realizado"
    )
    notes: str | None = Field(
        default=None,
        description="Notas o detalles adicionales de la suscripción"
    )

    # 🔗 Relacion con `Bot` (Cada suscripción está vinculada a un único bot)
    bot_id: int = Field(
        foreign_key="bots.id",
        ondelete="CASCADE",
        description="ID del bot asociado a la suscripción"
    )
    bot: Bot = Relationship(back_populates="company_subscriptions")

    # 🔗 Relación con Company (Cada suscripción está vinculada a una única empresa)
    company_id: int = Field(
        foreign_key="companies.id",
        ondelete="CASCADE",
        description="ID de la empresa que posee esta suscripción"
    )
    company: Company = Relationship(back_populates="bot_subscriptions")

    # 🔗 Relación con `SubscriptionStatus` (Cada suscripción tiene un único estado)
    status_id: int | None = Field(
        default=None,
        foreign_key="subscription_statuses.id",
        ondelete="SET NULL",
        description="Estado actual de la suscripción"
    )
    status: SubscriptionStatus | None = Relationship(back_populates="subscriptions")

    # 🔗 Relación con `SubscriptionPeriod` (Cada suscripción tiene un único período de facturación)
    subscription_period_id: int | None = Field(
        default=None,
        foreign_key="subscription_periods.id",
        ondelete="SET NULL",
        description="Frecuencia de facturación de la suscripción"
    )
    period: SubscriptionPeriod | None = Relationship(back_populates="subscriptions")

    # 🔗 Relación con `SubscriptionPayment` (Las suscripción tienen varios pagos)
    payments: list[SubscriptionPayment] = Relationship(
        back_populates="subscription",
        cascade_delete=True,
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )


# ---------------------------------------------------------------------------
# 20. SubscriptionPayment
# ---------------------------------------------------------------------------
class SubscriptionPayment(SQLModel, table=True):
    """
    💰 Representa un pago asociado a una suscripción de bot.

    Cada registro indica un intento o ejecución de pago, su estado,
    método de pago y su identificación transaccional.
    """
    __tablename__ = "subscription_payments"
    metadata = metadata

    # 🔑 Identificador
    id: int | None = Field(default=None, primary_key=True)

    # 💸 Detalles del pago
    amount: float = Field(
        default=0.0,
        description="Valor pagado en la transacción"
    )
    payment_date: datetime | None = Field(
        default=None,
        description="Fecha en la que se efectuó el pago"
    )
    payment_method: str | None = Field(
        default=None,
        max_length=50,
        description="Método utilizado para realizar el pago (ej: tarjeta, PSE)"
    )
    transaction_id: str = Field(
        max_length=100,
        unique=True,
        description="Identificador único de la transacción, generado por la pasarela de pagos"
    )

    # 🔗 Relación con `PaymentStatus` (Cada pago tiene un único estado)
    payment_status_id: int | None = Field(
        default=None,
        foreign_key="payment_statuses.id",
        ondelete="SET NULL",
        description="Estado actual del pago (ej: pendiente, completado)"
    )
    status: PaymentStatus | None = Relationship(back_populates="payments")

    # 🔗 Relación con `Subscription` (Cada pago pertenece a una única suscripción)
    subscription_id: int  = Field(
        foreign_key="subscriptions.id",
        ondelete="CASCADE",
        description="ID de la suscripción a la que pertenece el pago"
    )
    subscription: Subscription = Relationship(back_populates="payments")

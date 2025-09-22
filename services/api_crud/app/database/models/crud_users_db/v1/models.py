# Librería estándar
from datetime import datetime
from typing import Optional

# ORMs
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import func, MetaData
from sqlalchemy.orm import registry

# Utilidades de la aplicación
from app.utils.regex import E164_PHONE_RE, TELEGRAM_USERNAME_RE, EMAIL_RE

metadata  = MetaData()
crud_users_db_registry = registry()

class CrudUsersDB_Base(SQLModel, registry=crud_users_db_registry, metadata=metadata):
    """Clase base para los modelos de la base de datos 'crud_users_db'."""
    __abstract__ = True


# ---------------------------------------------------------------------------
# 1. UserAuthJobPosition
# ---------------------------------------------------------------------------
class JobPosition(CrudUsersDB_Base, table=True):
    """
    Modelo base para datos de puestos de trabajo.
    """
    __tablename__ = "job_positions"
    metadata = metadata

    # 🔑 Identificador único
    id: int = Field(default=None, primary_key=True)

    # 📛 Nombre del puesto (debe ser único)
    name: str = Field(
        max_length=50,
        unique=True,
        description="Ej: 'Responsable de ventas'"
    )

    # 📝 Descripción del puesto
    description: str | None = Field(
        default=None,
        description="Descripción opcional del puesto."
    )

    # 🔗 Relación con 'UserAuthEmployee'
    employees: list["Employee"] = Relationship(
        back_populates="job_position",
        passive_deletes="all"
    )

# ---------------------------------------------------------------------------
# 2. UserAuthAccessRole
# ---------------------------------------------------------------------------
class AccessRole(CrudUsersDB_Base, table=True):
    """
    Modelo base para datos de roles de acceso.
    """
    __tablename__ = "access_roles"
    metadata = metadata

    # 🔑 Identificador único
    id: int = Field(default=None, primary_key=True)

    # 📛 Nombre del rol (debe ser único)
    name: str = Field(
        max_length=50,
        unique=True,
        index=True,
        description="Ej: 'Responsable de ventas'"
    )

    # 📝 Descripción del rol
    description: str | None = Field(
        default=None,
        description="Descripción opcional del rol."
    )

    # 🔗 Relación con 'UserAuthCrudUser'
    crud_users: list["CrudUser"] = Relationship(
        back_populates="access_role",
        passive_deletes="all"
    )

    # 🔗 Relación con 'UserAuthBotUser'
    bot_users: list["BotUser"] = Relationship(
        back_populates="access_role",
        passive_deletes="all"
    )


# ---------------------------------------------------------------------------
# 3. UserAuthEmployee
# ---------------------------------------------------------------------------
class Employee(CrudUsersDB_Base, table=True):
    """
    Modelo base para datos de personas.
    """
    __tablename__ = "employees"
    metadata = metadata

    # 🔑 Identificador único
    id: int = Field(default=None, primary_key=True)

    # Telegram
    telegram_username: str = Field(
        max_length=50,
        regex=TELEGRAM_USERNAME_RE,
        unique=True,
        index=True
    )
    telegram_chat_id: int | None = Field(
        default=None,
        unique=True,
        index=True
    )

    # 🧍 Información personal
    first_name: str = Field(max_length=50)
    middle_name: str | None = Field(default=None,max_length=50)
    last_name: str = Field(max_length=50, index=True)
    second_last_name: str | None = Field(default=None,max_length=50)
    mobile_phone: str = Field(max_length=15, regex=E164_PHONE_RE,unique=True)
    email: str = Field(max_length=50, regex=EMAIL_RE, unique=True, index=True)

    # 🔗 Relación con 'UserAuthJobPosition'
    job_position_id: int | None = Field(
        default=None,
        foreign_key="job_positions.id",
        ondelete="SET NULL"
    )
    job_position: Optional[JobPosition] = Relationship(
        back_populates="employees"
    )

    # 🔗 Relación con 'UserAuthCrudUser'
    crud_user: Optional["CrudUser"] = Relationship(
        back_populates="employee",
        cascade_delete=True,
        sa_relationship_kwargs={"uselist": False}
    )

    # 🔗 Relación con 'UserAuthBotUser'
    bot_user: Optional["BotUser"] = Relationship(
        back_populates="employee",
        cascade_delete=True,
        sa_relationship_kwargs={"uselist": False}
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )


# ---------------------------------------------------------------------------
# 4. UserAuthCrudUser
# ---------------------------------------------------------------------------
class CrudUser(CrudUsersDB_Base, table=True):
    """
    Modelo base para datos de usuarios.
    """
    __tablename__ = "crud_users"
    metadata = metadata

    # 🔑 Identificador único
    id: int = Field(default=None, primary_key=True)

    # 🛡️ Información de acceso
    hashed_password: str = Field(max_length=100)
    is_active: bool = Field(default=True, index=True)
    data: dict | None = Field(default=None, sa_column=Column(JSON))

    # 🔗 Relación con 'UserAuthEmployee'
    employee_id: int = Field(
        foreign_key="employees.id",
        ondelete="CASCADE",
        unique=True
    )
    employee: Employee = Relationship(
        back_populates="crud_user",
        sa_relationship_kwargs={"uselist": False}
    )

    # 🔗 Relación con 'UserAuthAccessRole'
    access_role_id: int | None = Field(
        default=None,
        foreign_key="access_roles.id",
        ondelete="SET NULL"
    )
    access_role: Optional[AccessRole] = Relationship(
        back_populates="crud_users"
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )


# ---------------------------------------------------------------------------
# 5. UserAuthBotUser
# ---------------------------------------------------------------------------
class BotUser(CrudUsersDB_Base, table=True):
    """
    Modelo base para datos de usuarios de bots.
    """
    __tablename__ = "bot_users"
    metadata = metadata

    # 🔑 Identificador único
    id: int = Field(default=None, primary_key=True)

    # 🛡️ Información de acceso
    is_active: bool = Field(default=True, index=True)
    data: dict | None = Field(default=None, sa_column=Column(JSON))

    # 🔗 Relación con 'UserAuthAccessRole'
    access_role_id: int | None= Field(
        default=None,
        foreign_key="access_roles.id",
        ondelete="SET NULL"
    )
    access_role: Optional[AccessRole] = Relationship(
        back_populates="bot_users"
    )

    # 🔗 Relación con 'UserAuthEmployee'
    employee_id: int = Field(
        foreign_key="employees.id",
        ondelete="CASCADE",
        unique=True
    )
    employee: Employee = Relationship(
        back_populates="bot_user",
        sa_relationship_kwargs={"uselist": False}
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
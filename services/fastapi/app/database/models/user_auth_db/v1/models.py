# Librería estándar
from __future__ import annotations
from datetime import datetime

# ORMs
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import func, MetaData


# Utilidades de la aplicación
from app.utils.regex import E164_PHONE_RE, TELEGRAM_USERNAME_RE, EMAIL_RE

metadata  = MetaData()

# ---------------------------------------------------------------------------
# 1. PersonData
# ---------------------------------------------------------------------------
class PersonData(SQLModel, table=True):
    """
    Modelo base para datos de personas.
    """
    __tablename__ = "person_data"
    metadata = metadata

    # 🔑 Identificador único
    id: int = Field(default=None, primary_key=True)

    # 🧍 Información personal
    first_name: str = Field(max_length=50, index=True)
    middle_name: str | None = Field(default=None,max_length=50)
    last_name: str = Field(max_length=50, index=True)
    second_last_name: str | None = Field(default=None,max_length=50)
    mobile_phone: str = Field(max_length=15, regex=E164_PHONE_RE,unique=True)
    email: str = Field(max_length=50, regex=EMAIL_RE, unique=True)

    # 🔗 Relación con 'CrudUser'
    user: User | None = Relationship(
        back_populates="person",
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
# 2. RoleUserLink
# ---------------------------------------------------------------------------
class UserRoleLink(SQLModel, table=True):
    """
    Tabla de relación entre empleados y roles.

    Permite asignar múltiples roles a un empleado y un rol a múltiples empleados.
    """
    __tablename__ = "user_role_link"
    metadata = metadata

    # 🔑 Clave compuesta
    crud_user_id: int = Field(
        primary_key=True,
        foreign_key="users.id",
        ondelete="CASCADE",
        description="ID del usuario al que se le asigna el rol."
    )
    role_id: int = Field(
        primary_key=True,
        foreign_key="roles.id",
        ondelete="CASCADE",
        description="ID del rol asignado al usuario."
    )


# ---------------------------------------------------------------------------
# 3. CrudUser
# ---------------------------------------------------------------------------
class User(SQLModel, table=True):
    """
    Modelo base para datos de usuarios.
    """
    __tablename__ = "users"
    metadata = metadata

    # 🔑 Identificador único
    id: int = Field(default=None, primary_key=True)

    # 🧍 Información personal
    telegram_username: str = Field(max_length=50, regex=TELEGRAM_USERNAME_RE, unique=True)
    hashed_password: str = Field(max_length=100)
    is_active: bool = Field(default=True, index=True)
    data: dict | None = Field(default=None, sa_column=Column(JSON))

    # 🔗 Relación con 'PersonData'
    person_id: int = Field(
        foreign_key="person_data.id",
        ondelete="CASCADE",
        unique=True
    )
    person: PersonData = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )

    # 🔗 Relación con 'Role'
    roles: list[Role] = Relationship(
        back_populates="users",
        link_model=UserRoleLink
    )

    # 📆 Auditoría
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )


# ---------------------------------------------------------------------------
# 4. Role
# ---------------------------------------------------------------------------
class Role(SQLModel, table=True):
    """
    Modelo base para roles de usuario.
    Permite definir roles y asignar permisos a los usuarios.
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

    # 🔗 Relación con 'User'
    users: list[User] = Relationship(
        back_populates="roles",
        link_model=UserRoleLink
    )


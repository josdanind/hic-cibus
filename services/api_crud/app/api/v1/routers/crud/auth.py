# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería Estándar
from datetime import timedelta
from typing import TypeAlias, Callable, NoReturn

# 🧩 Terceros
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload

# 🏗️  Módulos internos de la aplicación
from app.database import DATABASES
from app.libraries.CRUDManager import CRUDManager
from app.core.config import settings
from app.core.security import (
    verify_password,
    create_access_token,
    decode_jwt
)

# 🧱 Modelos y esquemas
from app.database.models.user_auth_db import UserAuthEmployee as EmployeeModel
from app.schemas.auth import Token

# ────────────────────────────────
# 🗄️  Base de datos
# ────────────────────────────────
crud_user_db = DATABASES["user_auth_db"]
session_factory = crud_user_db.session_factory

# ────────────────────────────────
# 🔖  Alias y constantes
# ────────────────────────────────
TokenDecoder: TypeAlias = Callable[[str], dict]
_UNAUTHORIZED_HEADERS = {"WWW-Authenticate": "Bearer"}

# ────────────────────────────────
# 🔧  Helpers
# ────────────────────────────────
def _raise_unauthorized(detail:str) -> NoReturn:
    """Lanza un 401 con cabeceras y mensaje estándar."""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers=_UNAUTHORIZED_HEADERS,
    )


async def get_employee(
    *,
    username: str,
    crud: CRUDManager
) -> EmployeeModel | None:
    """Obtiene un empleado y su CrudUser asociado."""
    return await crud.get(
        EmployeeModel,
        {"telegram_username": username},
        single_result=True,
        load_options = [selectinload(EmployeeModel.crud_user)]
    )


def _verify_password(*, plain: str, hashed: str) -> None:
    """Valida la contraseña en texto plano contra la almacenada."""
    if not verify_password(plain, hashed):
        _raise_unauthorized("Incorrect username or password")


# ────────────────────────────────
# 🔑  API pública
# ────────────────────────────────
async def authenticate_crud_user(username: str, password: str) -> EmployeeModel:
    """
    Autentica un usuario CRUD.

    Devuelve el modelo Employee si las credenciales son válidas.
    """
    async with session_factory() as session:
        crud_manager = CRUDManager(session)

        employee = await get_employee(username=username, crud=crud_manager)
        crud_user = employee.crud_user if employee else None

        if employee is None or crud_user is None:
            _raise_unauthorized("Usuario o Contraseña incorrecta.")

        _verify_password(plain=password, hashed=crud_user.hashed_password)

        return employee


async def generate_access_token(username: str, password: str) -> Token:
    employee = await authenticate_crud_user(username=username,password=password)
    expires_delta = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)

    token = create_access_token(
        data={"sub": employee.telegram_username},
        expires_delta= expires_delta
    )

    return token


async def decode_token(
    *, token: str, token_decoder: TokenDecoder = decode_jwt
) -> EmployeeModel:
    """
    Decodifica un JWT y devuelve el empleado autenticado.

    Lanza 401 si el token es inválido o el usuario no existe.
    """
    payload: dict = token_decoder(token)
    username: str | None = payload.get("sub")
    if username is None:
        _raise_unauthorized("Invalid token")

    async with session_factory() as session:
        crud_manager = CRUDManager(session)
        employee = await get_employee(username=username, crud=crud_manager)

        if employee is None or employee.crud_user is None:
            _raise_unauthorized("Invalid token")

        return employee
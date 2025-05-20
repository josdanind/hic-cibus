# ─────────────────
# 📦 Importaciones
# ─────────────────
# Librería Estandar
from datetime import timedelta
from typing import TypeAlias, Callable

# Terceros
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import selectinload

# Aplicación Local
from app.core.config import settings
from app.core.security import verify_password, create_access_token, decode_jwt
from app.database import DATABASES
from app.libraries.CRUDManager import CRUDManager
# schemas
from app.schemas.auth import Token

# Configuración de base de datos y modelos
user_db = DATABASES["user_auth_db"]
EmployeeModel = user_db.models.Employee
CrudUserModel = user_db.models.CrudUser

# Alias de tipo para la función decodificadora de tokens
TokenDecoder: TypeAlias = Callable[[str], dict]

def raise_unauthorized_error(detail:str):
    """Lanza una HTTPException con código 401 y detalles predefinidos."""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )

# ───────────────────────────
# 🔑 Lógica de Autenticación
# ───────────────────────────
async def get_employee(username: str, crud_manager: CRUDManager):
    employee = await crud_manager.get(
        EmployeeModel,
        {"telegram_username": username},
        load_options = [selectinload(EmployeeModel.crud_user)]
    )

    return employee

async def authenticate_crud_user(
    username: str,
    password: str,
    crud_manager: CRUDManager
):
    """
    Autentica a un empleado utilizando su nombre de usuario (telegram_username) y contraseña.

    Args:
        username: El nombre de usuario de Telegram del empleado.
        password: La contraseña en texto plano del empleado.
        crud_manager: Instancia de CRUDManager para acceder a la base de datos.

    Returns:
        El objeto EmployeeModel si la autenticación es exitosa.

    Raises:
        HTTPException: Si el empleado no se encuentra o la contraseña es incorrecta.
    """
    employee = await get_employee(username, crud_manager)
    crud_user = employee.crud_user

    if not employee or not crud_user:
        raise_unauthorized_error(
            detail="Incorrect username or password"
        )

    hashed_password = crud_user.hashed_password

    if not verify_password(password, hashed_password):
        raise_unauthorized_error(
            detail="Incorrect username or password"
        )

    return employee


async def generate_access_token(
    form_data: OAuth2PasswordRequestForm,
    crud_manager: CRUDManager
) -> Token | None:
    """
    Valida las credenciales del formulario y genera un token de acceso.

    Args:
        form_data: Datos del formulario OAuth2 (username y password).
        crud_manager: Instancia de CRUDManager para la autenticación.

    Returns:
        Un objeto Token con el token de acceso y el tipo de token.

    Raises:
        HTTPException: Si la autenticación falla.
    """
    username = form_data.username
    password = form_data.password

    crud_user = await authenticate_crud_user(
        username,
        password,
        crud_manager
    )

    access_token_expires = timedelta(
        days=settings.ACCESS_TOKEN_EXPIRE_DAYS
    )

    access_token = create_access_token(
        data={"sub": crud_user.telegram_username},
        expires_delta= access_token_expires
    )

    return access_token

async def decode_token(
    token: str,
    crud_manager: CRUDManager,
    token_decoder: TokenDecoder = decode_jwt,
) -> dict | None:
    payload: dict = token_decoder(token)
    username: str | None = payload.get("sub")

    employee = await get_employee(username, crud_manager)

    if not username or not employee or not employee.crud_user:
        raise_unauthorized_error(
            detail="Invalid token"
        )

    return employee
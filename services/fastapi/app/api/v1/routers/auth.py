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
from app.libraries import CRUDManager
# schemas
from app.schemas.auth import Token

# Configuración de base de datos y modelos
crud_user_db = DATABASES["user_auth_db"]
session_factory = crud_user_db.session_factory
EmployeeModel = crud_user_db.models.Employee
CrudUserModel = crud_user_db.models.CrudUser

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
# Obtiene Empleado
async def get_employee(username: str, crud_manager: CRUDManager):
    employee = await crud_manager.get(
        EmployeeModel,
        {"telegram_username": username},
        load_options = [selectinload(EmployeeModel.crud_user)]
    )

    return employee

# Autenticar usuario CRUD
async def authenticate_crud_user(
    username: str,
    password: str
):
    async with session_factory() as session:
        crud_manager = CRUDManager(session)

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

# Generar access Token
async def generate_access_token(
    username: str,
    password: str
) -> Token | None:
    crud_user = await authenticate_crud_user(
        username,
        password,
    )

    access_token_expires = timedelta(
        days=settings.ACCESS_TOKEN_EXPIRE_DAYS
    )

    access_token = create_access_token(
        data={"sub": crud_user.telegram_username},
        expires_delta= access_token_expires
    )

    return access_token

# Decodificador del Token
async def decode_token(
    token: str,
    token_decoder: TokenDecoder = decode_jwt,
) -> dict | None:
    payload: dict = token_decoder(token)
    username: str | None = payload.get("sub")

    async with session_factory() as session:
        crud_manager = CRUDManager(session)
        employee = await get_employee(username, crud_manager)

        if not username or not employee or not employee.crud_user:
            raise_unauthorized_error(
                detail="Invalid token"
            )

    return employee
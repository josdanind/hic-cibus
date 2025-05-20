# ─────────────────
# 📦 Importaciones
# ─────────────────
# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# SQLModel y SQLAlchemist
from sqlmodel.ext.asyncio.session import AsyncSession

# Utilidades y esquemas de la App
from app.schemas.auth import Token
from app.database import get_user_crud

# Utilidades del router
from .auth import generate_access_token, decode_token

router = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="crud_user/auth")

@router.post("/auth", response_model=Token)
async def login_for_access_token(
    form_data:OAuth2PasswordRequestForm = Depends(),
    crud_manager: AsyncSession = Depends(get_user_crud)
):
    """
    Autentica al usuario y genera un token de acceso.

    - **Requiere**: Nombre de usuario y contraseña.
    - **Retorna**: Un token JWT si las credenciales son correctas.
    - **Error**: Devuelve un error 401 si las credenciales son inválidas.
    """
    access_token = await generate_access_token(form_data, crud_manager)

    return Token(access_token=access_token)

@router.get("")
async def get_user(
    token: str = Depends(oauth2_schema),
    crud_manager: AsyncSession = Depends(get_user_crud)
):
    user = await decode_token(token, crud_manager)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
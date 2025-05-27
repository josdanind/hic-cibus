# ─────────────────
# 📦 Importaciones
# ─────────────────
# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# Utilidades y esquemas de la App
from app.schemas.auth import Token

# Utilidades del router
from .auth import generate_access_token
from .auth import decode_token as user_crud_decode_token

router = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="crud_user/auth")

@router.post("/auth", response_model=Token)
async def login_for_access_token(
    form_data:OAuth2PasswordRequestForm = Depends()
):
    """
    Autentica al usuario y genera un token de acceso.

    - **Requiere**: Nombre de usuario y contraseña.
    - **Retorna**: Un token JWT si las credenciales son correctas.
    - **Error**: Devuelve un error 401 si las credenciales son inválidas.
    """
    username, password = form_data.username, form_data.password

    access_token = await generate_access_token(username, password)

    return Token(access_token=access_token)

@router.get("")
async def get_user(
    token: str = Depends(oauth2_schema),
):
    user = await user_crud_decode_token(token)

    return user
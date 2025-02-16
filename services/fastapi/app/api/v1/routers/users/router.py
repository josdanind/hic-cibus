# Schemas
from app.schemas.auth import Token

# Librerías de terceros
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# Dependencias propias del router
from .auth import generate_access_token, decode_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth")

@router.post("/auth", response_model=Token, summary="Autenticar usuario y obtener token de acceso")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Autentica al usuario y genera un token de acceso.

    - **Requiere**: Nombre de usuario y contraseña.
    - **Retorna**: Un token JWT si las credenciales son correctas.
    - **Error**: Devuelve un error 401 si las credenciales son inválidas.
    """

    token = generate_access_token(form_data.username, form_data.password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token

@router.get("", summary="Obtener información del usuario autenticado")
async def get_user(token: str = Depends(oauth2_scheme)):
    """
    Obtiene la información del usuario autenticado a partir del token de acceso.

    - **Requiere**: Un token JWT válido.
    - **Retorna**: Información del usuario si el token es válido.
    - **Error**: Devuelve un error 401 si el token es inválido.
    """

    user = decode_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
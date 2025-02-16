# Librerías estándar
from datetime import timedelta
from typing import TypeAlias, Callable

# Core de la aplicación
from app.core.security import verify_password, create_access_token, decode_jwt
from app.core.config import settings

# Base de datos simulada
from app.database.fake_db import fake_users_db

# Alias de tipo para la función decodificadora de tokens
TokenDecoder: TypeAlias = Callable[[str], dict]

def authenticate_fake_user(username: str, password: str) -> dict | None:
    """
    Autentica a un usuario en la base de datos simulada.

    - **Parámetros**:
        - `username` (str): Nombre de usuario.
        - `password` (str): Contraseña del usuario.

    - **Retorna**:
        - `dict`: Información del usuario si las credenciales son correctas.
        - `None`: Si las credenciales son incorrectas.
    """

    user = fake_users_db.get(username)

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user

def generate_access_token(username: str, password: str) -> dict | None:
    """
    Genera un token de acceso para un usuario autenticado.

    - **Parámetros**:
        - `username` (str): Nombre de usuario.
        - `password` (str): Contraseña del usuario.

    - **Retorna**:
        - `dict`: Contiene el token de acceso y el tipo de token.
        - `None`: Si la autenticación falla.
    """

    user = authenticate_fake_user(username, password)

    if not user:
        return None

    access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def decode_token(
    token: str, token_decoder: TokenDecoder = decode_jwt
) -> dict | None:
    """
    Decodifica un token JWT y retorna la información del usuario si existe en la base de datos.

    - **Parámetros**:
        - `token` (str): Token JWT a decodificar.
        - `token_decoder` (Callable): Función encargada de decodificar el token. (Por defecto: `decode_jwt`).

    - **Retorna**:
        - `dict`: Información del usuario si el token es válido y el usuario existe.
        - `None`: Si el token es inválido o el usuario no está registrado.
    """

    payload: dict = token_decoder(token)
    username: str | None  = payload.get("sub")

    if not username or username not in fake_users_db:
        return None

    return fake_users_db[username]
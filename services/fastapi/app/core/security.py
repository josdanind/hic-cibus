# Librería Estándar
from datetime import datetime, timedelta, timezone

# Variables de entorno
from app.core.config import settings

# Librerías de terceros
from passlib.context import CryptContext
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Genera un token de acceso JWT.

    - **Parámetros**:
        - `payload` (dict): Datos que se incluirán en el token.
        - `expires_delta` (timedelta | None): Tiempo de expiración del token.
          Si no se proporciona, usa el valor por defecto de la configuración.

    - **Retorna**:
        - `str`: Token JWT generado.
    """

    to_encode = data.copy()
    current_time = datetime.now(timezone.utc)

    expire_time = current_time + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({
        "exp": expire_time,
        "iat": current_time
    })

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_password_hash(password: str) -> str:
    """
    Hashea una contraseña utilizando bcrypt.

    - **Parámetros**:
        - `password` (str): Contraseña en texto plano.

    - **Retorna**:
        - `str`: Contraseña hasheada.
    """

    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su versión hasheada.

    - **Parámetros**:
        - `plain_password` (str): Contraseña en texto plano.
        - `hashed_password` (str): Contraseña hasheada.

    - **Retorna**:
        - `bool`: `True` si la contraseña es válida, `False` en caso contrario.
    """

    return pwd_context.verify(plain_password, hashed_password)

def decode_jwt(token: str) -> dict:
    """
    Decodifica un token JWT y retorna su contenido.

    - **Parámetros**:
        - `token` (str): Token JWT a decodificar.

    - **Retorna**:
        - `dict`: Contenido del token si es válido.
        - `dict`: `{"error": "Token expirado"}` si el token ha expirado.
        - `dict`: `{"error": "Token inválido"}` si el token es inválido.
    """

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expirado"}
    except jwt.InvalidTokenError:
        return {"error": "Token inválido"}
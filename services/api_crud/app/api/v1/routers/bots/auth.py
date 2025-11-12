"""Utilidades de autenticación para bots."""
# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería Estandar
from datetime import timedelta
from typing import TypeAlias, Callable, NoReturn, Annotated

# 🧩 Terceros
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import selectinload

# 🏗️  Módulos internos de la aplicación
from app.core.config import settings
from app.schemas.bot import BotTokenPayload
from app.core.security import (
    verify_password,
    create_access_token,
    get_password_hash,
    decode_jwt
)
from app.libraries.CRUDManager import CRUDManager
from app.database import DATABASES

# 🧱 Modelos y esquemas
from app.database.models.tlaloc_db import Bot, BotCredential
from app.schemas.auth import Token



# ────────────────────────────────
# 🔖  Alias y constantes
# ────────────────────────────────
TokenDecoder: TypeAlias = Callable[[str], dict]
_UNAUTHORIZED_HEADERS = {"WWW-Authenticate": "Bearer"}

# ──────────────────────────────────────────────────────────────────────────────
# 🗄️  Base de datos
# ──────────────────────────────────────────────────────────────────────────────
bot_db = DATABASES[settings.TLALOC_DB_NAME]
session_factory = bot_db.session_factory

# ──────────────────────────────────────────────────────────────────────────────
# 🔐  Dependencias de seguridad
# ──────────────────────────────────────────────────────────────────────────────
bearer = HTTPBearer(auto_error=False)

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

async def _get_bot_by_name(name: str, crud_manager: CRUDManager) -> Bot | None:
    """Obtiene un bot por nombre junto a sus credenciales.

    Args:
        name: Nombre único del bot.
        crud: Gestor CRUD con sesión activa.

    Returns:
        Instancia `Bot` con relación `credentials` precargada o `None`.
    """
    return await crud_manager.get(
        model=Bot,
        filters={"name": name},
        single_result=True,
        load_options=[selectinload(Bot.credentials)]
    )

# ──────────────────────────────────────────────────────────────────────────────
# 🧾  Decodificación y validación de tokens
# ──────────────────────────────────────────────────────────────────────────────
async def decode_token(
    *,
    token:str,
    token_decoder: TokenDecoder = decode_jwt
):
    """Valida un JWT y retorna el bot asociado (si está activo).

    Flujo:
    1) Decodifica el JWT (sin I/O).
    2) Obtiene `sub` (bot_name) del payload.
    3) Carga el bot desde BD y verifica que esté activo.

    Args:
        token: JWT recibido (sin el prefijo Bearer).
        token_decoder: Función de decodificación (por defecto `decode_jwt`).

    Returns:
        Instancia `Bot` válida y activa.

    Raises:
        HTTPException: 401 si el token es inválido, el bot no existe o no está activo.
    """
    payload: dict = token_decoder(token)
    bot_name: str | None = payload.get("sub")

    if bot_name is None:
        _raise_unauthorized("Invalid token")

    async with session_factory() as session:
        crud_manager = CRUDManager(session)
        bot = await _get_bot_by_name(name=bot_name, crud_manager=crud_manager)

        if bot is None or not bot.is_active:
            _raise_unauthorized("Invalid token")

        if not bot.is_active:
            _raise_unauthorized("Bot desactivado")

    return bot


async def get_current_subject(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]
)-> BotTokenPayload:
    """Dependencia de FastAPI que retorna el `Bot` autenticado a partir del header Bearer.

    Ejemplo de uso:
        @router.get("/me")
        async def me(bot: Annotated[Bot, Depends(get_current_subject)]):
            return {"name": bot.name}

    Args:
        credentials: Extraído automáticamente por FastAPI desde `Authorization: Bearer <token>`.

    Returns:
        Bot autenticado y activo.

    Raises:
        HTTPException: 401 si falta el header o el esquema no es Bearer/si el token no es válido.
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta Authorization Bearer"
        )

    return await decode_token(token=credentials.credentials)


# ──────────────────────────────────────────────────────────────────────────────
# 🔑  Autenticación por usuario/contraseña y emisión de JWT
# ──────────────────────────────────────────────────────────────────────────────
async def authenticate_bot(name: str, password: str, crud_manager: CRUDManager) -> Bot:
    bot = await _get_bot_by_name(name=name, crud_manager=crud_manager)
    credentials = bot.credentials if bot else None

    if bot is None or credentials is None:
        _raise_unauthorized("Bot no encontrado o sin credenciales.")

    # Verificar la contraseña
    hashed_password = credentials.hashed_password

    if not verify_password(password, hashed_password):
        _raise_unauthorized("Usuario o Contraseña incorrecta.")

    return bot


async def _update_bot_credentials(
    crud: CRUDManager,
    bot_id: int,
    **data: dict
) -> None:
    """Actualiza las credenciales asociadas al bot."""
    await crud.update(
        model=BotCredential,
        filters={"bot_id": bot_id},
        data=data,
    )


async def generate_access_token(
    bot_name: str,
    password: str,
    crud_manager: CRUDManager
) -> Token:
    """
    Autentica un bot y genera un access token JWT.

    El token se almacena (hash) en la tabla de credenciales.
    """
    bot = await authenticate_bot(bot_name, password, crud_manager)
    expires_delta = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)

    token: str = create_access_token(
        data={
            "sub": bot.name,
            "is_active": bot.is_active
        },
        expires_delta= expires_delta
    )

    await _update_bot_credentials(
        crud=crud_manager,
        bot_id=bot.id,
        hashed_api_access_token=get_password_hash(token),
    )

    return token


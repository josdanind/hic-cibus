"""Utilidades de autenticación para bots."""

# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería Estandar
from datetime import timedelta
from typing import TypeAlias, Callable, NoReturn

# 🧩 Terceros
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload

# 🏗️  Módulos internos de la aplicación
from app.core.config import settings
from app.core.security import verify_password, create_access_token, get_password_hash
from app.database import DATABASES
from app.libraries.CRUDManager import CRUDManager

# 🧱 Modelos y esquemas
from app.database.models.bot_auth_db import Bot, BotCredential
from app.schemas.auth import Token

# ────────────────────────────────
# 🗄️  Base de datos
# ────────────────────────────────
bot_db = DATABASES["bot_auth_db"]
session_factory = bot_db.session_factory

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


async def get_bot(username: str, crud: CRUDManager) -> Bot | None:
    """Devuelve un bot (con sus credenciales) por nombre de usuario."""
    return await crud.get(
        Bot,
        {"name": username},
        single_result=True,
        load_options=[selectinload(Bot.credentials)]
    )


async def update_bot_credentials(
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


# ────────────────────────────────
# 🔑  API pública
# ────────────────────────────────
async def authenticate_bot(username: str, password: str) -> Bot:
    async with session_factory() as session:
        crud_manager = CRUDManager(session)

        bot = await get_bot(username=username, crud=crud_manager)
        credentials = bot.credentials if bot else None

        if bot is None or credentials is None:
            _raise_unauthorized("Bot no encontrado o sin credenciales.")

        # Verificar la contraseña
        hashed_password = credentials.hashed_password

        if not verify_password(password, hashed_password):
            _raise_unauthorized("Usuario o Contraseña incorrecta.")

        return bot


async def generate_access_token(username: str, password: str) -> Token:
    """
    Autentica un bot y genera un access token JWT.

    El token se almacena (hash) en la tabla de credenciales.
    """
    bot = await authenticate_bot(username, password)
    expires_delta = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)

    token: str = create_access_token(
        data={"sub": bot.name},
        expires_delta= expires_delta
    )

    async with session_factory() as session:
        crud_manager = CRUDManager(session)

        await update_bot_credentials(
            crud=crud_manager,
            bot_id=bot.id,
            hashed_api_access_token=get_password_hash(token),
            hashed_telegram_bot_token="Hola"
        )

    return token





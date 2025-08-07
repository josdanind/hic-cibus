# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Terceros
from app.libraries.TheaterHandler import TheaterHandler

# 🏗️  Módulos internos de la app
from app.core.config import settings
from app.database import get_valkey

theater_handler = TheaterHandler(
    bot_token=settings.TELEGRAM_BOT_TOKEN,
    api_crud_url=settings.API_CRUD_URL,
    valkey_client=get_valkey()
)

from .handlers import *

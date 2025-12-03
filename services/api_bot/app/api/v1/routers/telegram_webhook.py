# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería estándar
import json

# 🧩 Terceros
from fastapi import APIRouter, status, Request, Depends

# 🏗️  Módulos internos de la aplicación
from app.core.config import settings
from app.libraries.TheaterHandler import TheaterHandler
from app.dependencies.theater_handler import get_theater
from app.utils.http_exceptions import (
    unsupported_media_type,
    internal_server_error,
    forbidden
)

# ─────────────────────────────
# ⚙️ Configuración
# ─────────────────────────────
router = APIRouter()

JSON_CT = "application/json"
X_TELEGRAM_TOKEN_HEADER: str = "X-Telegram-Bot-Api-Secret-Token"

# ─────────────────────────────
# 🚦 Endpoint Webhook
# ─────────────────────────────
@router.post("/webhook",
    status_code=status.HTTP_200_OK,
    summary="Recibe y reenvía actualizaciones de Telegram al bot",
)
async def telegram_webhook(
    request: Request,
    theater_handler: TheaterHandler = Depends(get_theater)
) -> dict[str, bool]:
    """
    Valida el token secreto de Telegram, verifica el tipo de contenido
    y reenvía el cuerpo del mensaje al bot asíncrono.
    """
    # Validación del token secreto de Telegram
    secret_token = request.headers.get(X_TELEGRAM_TOKEN_HEADER)
    if secret_token != settings.TELEGRAM_SECRET_TOKEN:
        raise forbidden()

    # Validación del tipo de contenido
    content_type = request.headers.get("content-type", "").lower()
    if not content_type.startswith(JSON_CT):
        raise unsupported_media_type()

    try:
        # Decodifica y procesa el cuerpo de la solicitud
        raw_body: bytes = await request.body()
        print(raw_body)
        await theater_handler.process_update(raw_body.decode())

        return {"ok": True}
    except Exception as exc:
        raise internal_server_error()
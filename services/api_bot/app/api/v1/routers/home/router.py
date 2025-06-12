# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Terceros
from fastapi import APIRouter, Depends

# 🏗️  Módulos internos de la aplicación
from .auth import verify_token

router = APIRouter()

@router.get(
    "/ping",
    summary="Ping Bot",
    description="Endpoint de prueba de vida: responde con «Pong».",
    dependencies=[Depends(verify_token)]
)
async def get_home_frontend() -> dict[str, str]:
    """Devuelve un *pong* si la autenticación es válida."""
    return {
        "message": "Pong"
    }
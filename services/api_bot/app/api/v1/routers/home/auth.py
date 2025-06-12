# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Terceros
from fastapi import Header, HTTPException, status

# 🏗️  Módulos internos de la aplicación
from app.core.security import verify_hash
from app.database import get_valkey

# ─────────────────────────────
# 🗄️ VALKEY HELPERS
# ─────────────────────────────
async def load_hashed_token() -> str | None:
    client = await get_valkey()
    return await client.get("api_crud_token")

# ─────────────────────────────
# 🚦 DEPENDENCIA FASTAPI
# ─────────────────────────────
async def verify_token(hashed_token: str = Header(...)):
    token = await load_hashed_token()

    if not verify_hash(token, hashed_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
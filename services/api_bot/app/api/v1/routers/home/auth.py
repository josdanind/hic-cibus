# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Terceros
from fastapi import Header

# 🏗️  Módulos internos de la aplicación
from app.core.security import verify_hash
from app.database import get_valkey
from app.utils.regex import is_bcrypt_hash
from app.utils.http_exceptions import unauthorized

# ─────────────────────────────
# 🛠️ HELPERS VALKEY
# ─────────────────────────────
async def load_hashed_token() -> str | None:
    """
    Obtiene el token almacenado desde Valkey.

    Returns:
        str | None: Token hasheado o None si no existe.
    """
    client = await get_valkey()
    return await client.get("api_crud_token")

# ─────────────────────────────
# 🚦 DEPENDENCIA FASTAPI
# ─────────────────────────────
async def verify_token(hashed_token: str = Header(...)):
    """
    Verifica que el token recibido tenga formato y contenido válidos.

    Args:
        hashed_token (str): Token hasheado recibido en el header.

    Raises:
        HTTPException: Si el token tiene un formato inválido o no coincide.
    """
    # 🧪 Verificación de formato
    if not is_bcrypt_hash(hashed_token):
        raise unauthorized("Formato inválido")

    stored_token = await load_hashed_token()

    # 🔐 Verificación de coincidencia con el almacenado
    if not verify_hash(stored_token, hashed_token):
        raise unauthorized("token incorrecto")
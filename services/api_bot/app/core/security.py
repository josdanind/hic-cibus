# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Terceros
import aiohttp
from passlib.context import CryptContext

# 🏗️  Módulos internos de la aplicación
from app.core.config import settings
from app.utils.rich_format import print_success_message

# ───────────────────────────────
# 🔐 Seguridad y Autenticación
# ───────────────────────────────
__AUTH_BOT_URL = f"{settings.API_CRUD_URL}/auth"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash(plain_str: str):
    """Genera un hash a partir de una cadena en texto plano."""
    return pwd_context.hash(plain_str)

def verify_hash(plain_str: str, hashed_str: str) -> bool:
    """Verifica si la cadena coincide con el hash."""
    return pwd_context.verify(plain_str, hashed_str)

# ───────────────────────────────
# 🔄 Comunicación con API CRUD
# ───────────────────────────────
async def fetch_crud_token():
    """Obtiene un token «fresco» del API CRUD."""

    async with aiohttp.ClientSession() as session:
        async with session.post(
            __AUTH_BOT_URL,
            data = {
                "username": settings.TELEGRAM_BOT_NAME,
                "password": settings.TELEGRAM_BOT_PASSWORD,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        ) as response:
            response.raise_for_status()  # lanza error si status != 2xx

            data: dict = await response.json()
            token = data.get("access_token")

            print_success_message("Token para la API CRUD obtenido exitosamente.")

            return token


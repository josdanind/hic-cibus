# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Terceros
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# 🏗️  Módulos internos de la aplicación
from app.schemas.auth import Token

# 🛠️ Utilidades del router
from .auth import generate_access_token

router = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="bot/auth")

@router.post("/auth", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    bot_name, password = form_data.username, form_data.password

    access_token = await generate_access_token(bot_name, password)

    return Token(access_token=access_token)


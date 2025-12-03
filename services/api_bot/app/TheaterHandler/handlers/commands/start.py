# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Terceros
from telebot import types

# 🏗️  Módulos internos de la app
from app.libraries.TheaterHandler import TheaterHandler, UserCtx

async def start_cmd(
    message: types.Message,
    ctx: UserCtx,
    theater_handler: TheaterHandler
):
    print("Hola")
    print(ctx)
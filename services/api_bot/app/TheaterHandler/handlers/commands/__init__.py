# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🏗️  Módulos internos de la app
from app.libraries.TheaterHandler import TheaterHandler, UserCtx

# 🧩 Terceros
from telebot import types

# 💻 Comandos
from .start import start_cmd

def register_commands(
    theater_handler: TheaterHandler,
) -> None:
    cmdx = theater_handler.cmd_with_ctx

    @cmdx("start")
    async def start(message: types.Message, ctx: UserCtx):
        await start_cmd(message, ctx, theater_handler)

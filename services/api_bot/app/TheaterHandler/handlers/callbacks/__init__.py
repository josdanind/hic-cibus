# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Terceros
from telebot import types

# 🏗️  Módulos internos - Theater Handler
from ... import theater_handler

# ──────────────────────────────
# Callbacks desconocidos
# ──────────────────────────────
@theater_handler.callback()
async def cb_unknown(call: types.CallbackQuery):
    """
    Manejador de callbacks para callbacks desconocidos.
    """
    await theater_handler.answer_callback_query(
        call.id,
        "⚠️ Botón no soportado"
    )

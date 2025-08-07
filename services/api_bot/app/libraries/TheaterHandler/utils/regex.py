# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería estándar
import re

# ──────────────────────────────────────────────
# 🤖 Token de Bot de Telegram
# ──────────────────────────────────────────────
# - Ejemplo válido: 123456789:AAAbbbCccDddEeeFffGggHhhIiiJjjKkkL
TELEGRAM_BOT_TOKEN_RE = r"^\d{6,12}:[a-zA-Z0-9_-]{35}$"

# ──────────────────────────────────────────────
# 🔐 Token de autenticación Ngrok
# ──────────────────────────────────────────────
NGROK_TOKEN_RE = r"^[a-zA-Z0-9_-]{40,64}$"
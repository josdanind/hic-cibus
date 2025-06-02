# Librería Estándar
import re

# ╭───────────────────────────────────────────────────────╮
# │ 📞  Número de teléfono en formato internacional E.164 │
# ╰───────────────────────────────────────────────────────╯
# - Debe iniciar con '+' seguido de 10 a 15 dígitos
# - El primer dígito (después de '+') debe estar entre 1 y 9
E164_PHONE_RE = r"^\+[1-9]\d{9,14}$"


# ╭─────────────────────────────────────────╮
# │ 👤 Nombre de usuario válido en Telegram │
# ╰─────────────────────────────────────────╯
# - Longitud entre 5 y 32 caracteres
# - Debe comenzar con letra o número
# - Puede contener letras, números y guiones bajos
TELEGRAM_USERNAME_RE = r"^[a-zA-Z0-9](?:[a-zA-Z0-9_]{4,31})$"

# ╭───────────────────────╮
# │ 📧 Correo electrónico |                                              │
# ╰───────────────────────╯
# Ejemplo válido: ejemplo@dominio.com
EMAIL_RE = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,63}$"
# Librería Estándar
import re

# ──────────────────────────────────────────────
# 📞 Teléfono en formato internacional E.164
# ──────────────────────────────────────────────
# - Debe iniciar con '+' seguido de 10 a 15 dígitos
# - El primer dígito (después de '+') debe estar entre 1 y 9
E164_PHONE_RE = r"^\+[1-9]\d{9,14}$"


# ──────────────────────────────────────────────
# 👤 Nombre de usuario válido en Telegram
# ──────────────────────────────────────────────
# - Longitud entre 5 y 32 caracteres
# - Debe comenzar con letra o número
# - Puede contener letras, números y guiones bajos
TELEGRAM_USERNAME_RE = r"^[a-zA-Z0-9](?:[a-zA-Z0-9_]{4,31})$"


# ──────────────────────────────────────────────
# 📧 Correo electrónico válido
# ──────────────────────────────────────────────
# Ejemplo válido: ejemplo@dominio.com
EMAIL_RE = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,63}$"

# ──────────────────────────────────────────────
# 🔐 Verificación de hash bcrypt
# ──────────────────────────────────────────────
def is_bcrypt_hash(s: str) -> bool:
    """
    Verifica si una cadena tiene el formato de un hash bcrypt válido.

    Args:
        s (str): Cadena a verificar.

    Returns:
        bool: True si parece un hash bcrypt, False si no.
    """
    bcrypt_pattern = r'^\$2[abxy]?\$\d{2}\$[./A-Za-z0-9]{53}$'
    return bool(re.match(bcrypt_pattern, s))
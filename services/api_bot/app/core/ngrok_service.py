# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería estándar
from typing import Final
import re, sys

# 🧩 Terceros
from pyngrok import ngrok, conf

# 🏗️  Módulos internos de la librería
from app.utils.regex import NGROK_TOKEN_RE
from app.utils.rich_format import print_success_message, print_panel

# ────────────────────────────────
# ⚙️  Constantes
# ────────────────────────────────
DEFAULT_PORT: Final = "8000"
CONFIG_PATH:  Final = "./config_ngrok.yml"
REGION:       Final = "sa"

# ────────────────────────────────────────────────
# 🔧 Helpers privados
# ────────────────────────────────────────────────
def _delete_local_tunnels() -> None:
    """
    Llama a la Agent API local en http://127.0.0.1:4040
    para eliminar todos los túneles abiertos por este host.
    """
    try:
        ngrok.api_request("DELETE", "http://127.0.0.1:4040/api/tunnels")
    except Exception:
        # Silenciar si el agente no está corriendo todavía
        pass

# ────────────────────────────────────────────────
# 🚀 Inicialización de Ngrok
# ────────────────────────────────────────────────
def init_ngrok(token: str,  *, port: str | None = None) -> str:
    """
    Inicia un túnel HTTPS a un puerto local y retorna la URL pública.

    Args:
        token (str): Token de autenticación de Ngrok.
        port (str | None): Puerto local a exponer (por defecto 8000 o desde CLI).

    Returns:
        str: URL pública generada por Ngrok.
    """
    if not re.fullmatch(NGROK_TOKEN_RE, token):
        print_success_message("Token Ngrok inválido", success=False)
        return ""
    else:
        # Determinar el puerto
        port = (
            sys.argv[sys.argv.index("--port") + 1]
            if "--port" in sys.argv
            else (port or DEFAULT_PORT)
        )

        # Configuración personalizada
        config = conf.get_default()
        config.config_path = CONFIG_PATH
        config.region = REGION
        ngrok.set_auth_token(token)

        # Cierre de túneles anteriores
        _delete_local_tunnels()

        # Apertura del túnel
        tunnel = ngrok.connect(addr=port, bind_tls=True)
        public_url = tunnel.public_url

        print_panel(
        title="NGROK ACTIVO",
        messages=[
            ("URL Pública", public_url),
            ("Puerto Local", port)
        ],
        style="check arrow"
    )

        return public_url

# ────────────────────────────────────────────────
# 🛑 Cierre de Ngrok
# ────────────────────────────────────────────────
def close_ngrok(url: str | None = None) -> None:
    """
    Cierra uno o todos los túneles Ngrok activos.

    Args:
        url (str | None): Si se proporciona, cierra solo ese túnel.
                          Si es None, cierra todos los túneles.
    """
    try:
        if url:
            ngrok.disconnect(url)
        else:
            _delete_local_tunnels()

        ngrok.kill()
        print_success_message("Ngrok cerrado correctamente.")
    except Exception as exc:
        print_success_message("ERROR AL CERRAR NGROK", False)


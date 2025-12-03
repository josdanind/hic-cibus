# Librerías de terceros
from pydantic_settings import BaseSettings
import os

api_key = os.getenv("TLALOC_BOT_DOMAIN_DEV")
print("API_KEY:", api_key)
class Settings(BaseSettings):
    # Configuración general
    PORT: int
    API_DOMAIN: str
    DEVELOPMENT_MODE: bool

    # 🔑 Credenciales del Bot
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_SECRET_TOKEN: str
    TELEGRAM_BOT_NAME: str
    TELEGRAM_BOT_PASSWORD: str

    # 🔑 Clave de acceso para Valkey
    VALKEY_HOST:str
    VALKEY_PORT:int
    VALKEY_PASSWORD: str

    # 🌐 URL base del servicio API CRUD
    API_CRUD_URL:str

    # Ngrok Token
    NGROK_TOKEN:str

# Instancia global de configuración
settings = Settings()
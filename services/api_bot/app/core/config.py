# Librerías de terceros
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configuración general
    PORT: int
    API_DOMAIN: str
    ENVIRONMENT: str

    # 🔑 Credenciales del Bot
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_BOT_NAME: str
    TELEGRAM_BOT_PASSWORD: str

    # 🔑 Clave de acceso para Valkey
    VALKEY_HOST:str
    VALKEY_PORT:int
    VALKEY_PASSWORD: str

    # 🌐 URL base del servicio API CRUD
    API_CRUD_URL:str

# Instancia global de configuración
settings = Settings()
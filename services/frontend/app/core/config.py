# Librerías de terceros
from pydantic_settings import BaseSettings
from pydantic import computed_field, Field

class Settings(BaseSettings):
    # Configuración general
    FRONTEND_DOMAIN: str


# Instancia global de configuración
settings = Settings()
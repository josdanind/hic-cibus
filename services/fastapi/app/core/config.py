# Librerías de terceros
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configuración general
    PORT: int
    API_DOMAIN: str
    ENVIRONMENT: str

    # Configuración de seguridad y autenticación JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Usuario simulado para pruebas
    FASTAPI_DUMMY_USER: str
    FASTAPI_DUMMY_PASSWORD: str
    FASTAPI_DUMMY_FULLNAME: str
    FASTAPI_DUMMY_EMAIL: str

# Instancia global de configuración
settings = Settings()
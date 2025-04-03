# Librerías de terceros
from pydantic_settings import BaseSettings
from pydantic import computed_field, Field

class Settings(BaseSettings):
    # Configuración general
    PORT: int
    API_DOMAIN: str
    ENVIRONMENT: str

    # Configuración de la base de datos para la autenticación de Bots
    BOT_AUTH_DB_HOST: str
    BOT_AUTH_DB_PORT: int
    BOT_AUTH_DB_USER: str
    BOT_AUTH_DB_PASSWORD: str
    BOT_AUTH_DB_NAME: str

    # Configuración de seguridad y autenticación JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Autenticación de Bots
    BOT_API_KEY_EXPIRATION: int

    # Usuario simulado para pruebas
    FASTAPI_DUMMY_USER: str
    FASTAPI_DUMMY_PASSWORD: str
    FASTAPI_DUMMY_FULLNAME: str
    FASTAPI_DUMMY_EMAIL: str

    @computed_field
    def BOT_AUTH_DB_URL(self) -> str:
        user = self.BOT_AUTH_DB_USER
        password = self.BOT_AUTH_DB_PASSWORD
        host = self.BOT_AUTH_DB_HOST
        port = self.BOT_AUTH_DB_PORT
        name = self.BOT_AUTH_DB_NAME

        return f"postgresql://{user}:{password}@{host}:{port}/{name}"

# Instancia global de configuración
settings = Settings()
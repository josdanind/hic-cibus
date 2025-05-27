# Librerías de terceros
from pydantic_settings import BaseSettings
from pydantic import computed_field, Field

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

    # Usuario CRUD
    TELEGRAM_USERNAME: str
    FIRST_NAME: str
    LAST_NAME: str
    MOBILE_PHONE: str
    EMAIL: str
    PASSWORD: str

    # 🐘🤖 Configuración de la base de datos para la autenticación de Bots
    BOT_AUTH_DB_HOST: str
    BOT_AUTH_DB_PORT: int
    BOT_AUTH_DB_USER: str
    BOT_AUTH_DB_PASSWORD: str
    BOT_AUTH_DB_NAME: str

    @computed_field
    def BOT_AUTH_DB_URL(self) -> str:
        user = self.BOT_AUTH_DB_USER
        password = self.BOT_AUTH_DB_PASSWORD
        host = self.BOT_AUTH_DB_HOST
        port = self.BOT_AUTH_DB_PORT
        name = self.BOT_AUTH_DB_NAME

        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

    # 🐘👱 Configuración de la base de datos para la autenticación de Usuarios
    USER_AUTH_DB_HOST: str
    USER_AUTH_DB_PORT: int
    USER_AUTH_DB_USER: str
    USER_AUTH_DB_PASSWORD: str
    USER_AUTH_DB_NAME: str

    @computed_field
    def USER_AUTH_DB_URL(self) -> str:
        user = self.USER_AUTH_DB_USER
        password = self.USER_AUTH_DB_PASSWORD
        host = self.USER_AUTH_DB_HOST
        port = self.USER_AUTH_DB_PORT
        name = self.USER_AUTH_DB_NAME

        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

    # 🐘🖥️ Configuración de la base de datos para la autenticación de Usuarios MQTT
    MQTT_USER_AUTH_DB_HOST: str
    MQTT_USER_AUTH_DB_PORT: int
    MQTT_USER_AUTH_DB_USER: str
    MQTT_USER_AUTH_DB_PASSWORD: str
    MQTT_USER_AUTH_DB_NAME: str

    @computed_field
    def MQTT_USER_AUTH_DB_URL(self) -> str:
        user = self.MQTT_USER_AUTH_DB_USER
        password = self.MQTT_USER_AUTH_DB_PASSWORD
        host = self.MQTT_USER_AUTH_DB_HOST
        port = self.MQTT_USER_AUTH_DB_PORT
        name = self.MQTT_USER_AUTH_DB_NAME

        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

    # Usuario MQTT por defecto
    MQTT_USER:str
    MQTT_USER_PASSWORD_HASH: str

# Instancia global de configuración
settings = Settings()
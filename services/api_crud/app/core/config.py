# Librerías de terceros
from pydantic_settings import BaseSettings
from pydantic import computed_field, Field

class Settings(BaseSettings):
    # Configuración general
    DEVELOPMENT_MODE: bool

    # Configuración de seguridad y autenticación JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # 👤 Usuario predeterminado para la API CRUD
    CRUD_USER_TELEGRAM_USERNAME: str
    CRUD_USER_FIRST_NAME: str
    CRUD_USER_LAST_NAME: str
    CRUD_USER_MOBILE_PHONE: str
    CRUD_USER_EMAIL: str
    CRUD_USER_PASSWORD: str

    # 🐘👱 Configuración de la base de datos para la autenticación de Usuarios
    CRUD_USERS_DB_HOST: str
    CRUD_USERS_DB_PORT: int
    CRUD_USERS_DB_USER: str
    CRUD_USERS_DB_PASSWORD: str
    CRUD_USERS_DB_NAME: str

    @computed_field
    def CRUD_USERS_DB_URL(self) -> str:
        user = self.CRUD_USERS_DB_USER
        password = self.CRUD_USERS_DB_PASSWORD
        host = self.CRUD_USERS_DB_HOST
        port = self.CRUD_USERS_DB_PORT
        name = self.CRUD_USERS_DB_NAME

        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

    # 🐘🖥️ Configuración de la base de datos para la autenticación de Usuarios MQTT
    MQTT_USERS_DB_HOST: str
    MQTT_USERS_DB_PORT: int
    MQTT_USERS_DB_USER: str
    MQTT_USERS_DB_PASSWORD: str
    MQTT_USERS_DB_NAME: str

    @computed_field
    def MQTT_USERS_DB_URL(self) -> str:
        user = self.MQTT_USERS_DB_USER
        password = self.MQTT_USERS_DB_PASSWORD
        host = self.MQTT_USERS_DB_HOST
        port = self.MQTT_USERS_DB_PORT
        name = self.MQTT_USERS_DB_NAME

        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

    # 👤 Usuario MQTT predeterminado
    MQTT_USER_USERNAME:str
    MQTT_USER_PASSWORD: str
    BCRYPT_ROUNDS: int

    # # 🐘🤖 Configuración de la base de datos para Tlaloc Bot
    TLALOC_DB_HOST: str
    TLALOC_DB_PORT: int
    TLALOC_DB_USER: str
    TLALOC_DB_PASSWORD: str
    TLALOC_DB_NAME: str

    @computed_field
    def TLALOC_DB_URL(self) -> str:
        user = self.TLALOC_DB_USER
        password = self.TLALOC_DB_PASSWORD
        host = self.TLALOC_DB_HOST
        port = self.TLALOC_DB_PORT
        name = self.TLALOC_DB_NAME

        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"


# Instancia global de configuración
settings = Settings()
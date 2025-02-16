from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int
    API_DOMAIN: str
    ENVIRONMENT: str
    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    # Usuario simulado
    FASTAPI_DUMMY_USER: str
    FASTAPI_DUMMY_PASSWORD: str
    FASTAPI_DUMMY_FULLNAME: str
    FASTAPI_DUMMY_EMAIL: str

settings = Settings()
# Seguridad
from app.core.security import get_password_hash
from app.core.config import settings

# Schemas
from app.schemas.auth import UserInDB

# Datos de usuario según el entorno
default_user = {
    "username": "admin",
    "password": "admin",
    "full_name": "Administrador",
    "email": "admin@example.com",
}

prod_user = {
    "username": settings.FASTAPI_DUMMY_USER,
    "password": settings.FASTAPI_DUMMY_PASSWORD,
    "full_name": settings.FASTAPI_DUMMY_FULLNAME,
    "email": settings.FASTAPI_DUMMY_EMAIL,
}

# Seleccionar los datos según el entorno
user_data = default_user if settings.ENVIRONMENT == "development" else prod_user

# Base de datos simulada
fake_users_db = {
    user_data["username"]: UserInDB(
        username=user_data["username"],
        email=user_data["email"],
        full_name=user_data["full_name"],
        disabled=False,
        hashed_password=get_password_hash(user_data["password"]),
    )
}

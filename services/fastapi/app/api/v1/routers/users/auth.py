# Librería Estándar
from datetime import timedelta

# Core de la aplicación
from app.core.security import verify_password, create_access_token, decode_token
from app.core.config import settings

# Database: usuario simulado
from app.database.fake_db import fake_users_db

def authenticate_fake_user(username: str, password: str):
    user = fake_users_db.get(username)

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user

def create_token(username: str, password: str):
    user = authenticate_fake_user(username, password)

    if not user:
        return None

    access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

def decode_user_token(token: str):
    payload = decode_token(token)
    username: str = payload.get("sub")

    if not username or username not in fake_users_db:
        return None

    return fake_users_db[username]
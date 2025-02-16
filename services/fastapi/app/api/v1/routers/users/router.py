# Schemas
from app.schemas.auth import Token

# Librerías de terceros
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# Dependencias propias del router
from .auth import create_token, decode_user_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth")

@router.post("/auth", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    token = create_token(form_data.username, form_data.password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token

@router.get("")
async def get_user(token: str = Depends(oauth2_scheme)):
    user = decode_user_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
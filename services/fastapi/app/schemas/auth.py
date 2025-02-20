# Librerías de terceros
from pydantic import BaseModel

class Token(BaseModel):
    """
    Esquema para la respuesta de autenticación con JWT.

    - `access_token` (str): Token de acceso generado.
    - `token_type` (str): Tipo de token (generalmente "bearer").
    """

    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Esquema para la información contenida en el token.

    - `username` (str | None): Nombre de usuario asociado al token.
      Puede ser `None` si no se encuentra en el token.
    """

    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

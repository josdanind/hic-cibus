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

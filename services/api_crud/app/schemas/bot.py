# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Librerías de terceros
from pydantic import BaseModel, field_validator, Field, ConfigDict

# 🛠️ Utilidades, librerías y configuraciones
from app.core.security import get_password_hash

class RegisterBot(BaseModel):
    """
    Modelo de datos para representar un bot en la base de datos.
    """
    model_config = ConfigDict(populate_by_name=True)

    name: str
    api_url: str
    bot_model_id: int
    password: str = Field(serialization_alias="hashed_password")

    @field_validator("password", mode="before")
    @classmethod
    def _hash_token(cls, plain: str) -> str:
        """
        Recibe la contraseña en claro (plain), la hashea
        y devuelve el string resultante.
        """
        return get_password_hash(plain)
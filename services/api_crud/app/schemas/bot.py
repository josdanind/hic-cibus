# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Librerías de terceros
from pydantic import (
    BaseModel,
    field_validator,
    Field,
    ConfigDict,
    AliasChoices
)

# 🛠️ Utilidades, librerías y configuraciones
from app.core.security import get_password_hash


# ---- helpers de seguridad (evita doble hash) ----
def is_bcrypt_hash(value: str) -> bool:
    # Heurística común para bcrypt: "$2a$" | "$2b$" | "$2y$"
    return isinstance(value, str) and value.startswith(("$2a$", "$2b$", "$2y$"))


# -------------------- MIXINS REUTILIZABLES --------------------

class HashedPasswordMixin(BaseModel):
    """
    Aporta el campo 'password' y lo serializa como 'hashed_password'.
    Acepta tanto 'password' (plano) como 'hashed_password' (ya hasheado) al validar.
    """
    model_config = ConfigDict(populate_by_name=True)

    password: str = Field(
        ...,
        # permitir que el input venga como 'password' o 'hashed_password'
        validation_alias=AliasChoices("password", "hashed_password"),
        # pero al serializar, exponerlo como 'hashed_password'
        serialization_alias="hashed_password",
        description="Se almacena como hash; se serializa bajo 'hashed_password'.",
    )

    @field_validator("password", mode="before")
    @classmethod
    def _hash_password(cls, v: str) -> str:
        if v is None:
            raise ValueError("password requerido")
        # Evita re-hashear si ya llega hasheado
        return v if is_bcrypt_hash(v) else get_password_hash(v)



# -------------------- MODELOS FINALES --------------------

class RegisterBot(HashedPasswordMixin):
    """
    Modelo de datos para representar un bot en la base de datos.
    """
    model_config = ConfigDict(populate_by_name=True)

    name: str
    api_url: str
    bot_model_id: int


class BotCredential(HashedPasswordMixin):
    """
    Modelo de datos para representar las credenciales de un bot.
    """
    model_config = ConfigDict(populate_by_name=True)

    name: str

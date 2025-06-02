from pydantic import BaseModel, field_validator, Field, ConfigDict

from app.core.security import get_password_hash

class CrudUserInDB(BaseModel):
    # model_config = ConfigDict(populate_by_name=True)

    password: str = Field(serialization_alias="hashed_password")
    is_active: bool = True
    data: dict | None = None
    employee_id: int
    access_role_id: int | None = None

    @field_validator("password", mode="before")
    @classmethod
    def _hash_password(cls, plain:str) -> str:
        """
        Recibe la contraseña en claro (plain), la hashea
        y devuelve el string resultante.
        """
        return get_password_hash(plain)


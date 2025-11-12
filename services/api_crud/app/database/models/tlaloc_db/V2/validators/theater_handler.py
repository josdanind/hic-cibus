# Librería estándar
from typing_extensions import Annotated

# Librerías de terceros
from pydantic import StringConstraints, AfterValidator

# Asegura que no esté vacío y sin espacios al inicio o final
def _check_not_empty(v: str) -> str:
    if not v:
        raise ValueError("name no puede estar vacío")
    return v

# ---------------------------------------------------------------------------
#  1. 📽️ Reel
# ---------------------------------------------------------------------------
ButtonText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=2,
        max_length=15
    ),
    AfterValidator(_check_not_empty)
]


# ---------------------------------------------------------------------------
#  1. 🔍 Query SQL
# ---------------------------------------------------------------------------
# sql_query
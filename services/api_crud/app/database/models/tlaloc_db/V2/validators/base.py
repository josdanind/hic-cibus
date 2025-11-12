# Librería estándar
from typing_extensions import Annotated

# Librerías de terceros
from pydantic import StringConstraints, AfterValidator

# Asegura que no esté vacío y sin espacios al inicio o final
def _check_not_empty(v: str) -> str:
    if not v:
        raise ValueError("name no puede estar vacío")
    return v

# Convierte a mayúsculas
def _to_update(v: str) -> str:
    return v.upper()

CodeStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=30,
        pattern=r'^[A-Z0-9_]+$'
    ),
    AfterValidator(_to_update)
]

NameStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100,
    ),
    AfterValidator(_check_not_empty),
]

VersionStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,      # quita espacios al inicio y final
        min_length=1,               # debe tener al menos 1 caracter
        max_length=20,              # igual que en tu DDL
        pattern=r'^[0-9]+(\.[0-9]+)*$',  # formato 1.0, 2.1, 3.0.4, etc.
    ),
]

PhoneE164Str = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=7,   # al menos + y 6 dígitos
        max_length=16,  # + y hasta 15 dígitos
        pattern=r'^\+[1-9][0-9]{6,14}$',
    ),
]

EmailStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=6,    # ej: a@b.co es el mínimo válido
        max_length=100,  # como en tu DDL
        pattern=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
    ),
]

HashedStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=255,
    ),
]

MacAddressStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=17,
        max_length=17,
        pattern=r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    )
]

MqttTopicStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=255
    )
]

# ---------------------------------------------------------------------------
# 36. 📝 Validaciones relacionadas con el bot de telegram
# ---------------------------------------------------------------------------

InlineButtonText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=64
    )
]



from .models import *

models = {
    "PersonData": PersonData,
    "Role": Role,
    "User": User,
    "UserRoleLink": UserRoleLink,
}

__all__ = ["models", "metadata"]


from .models import (
    UserAuthJobPosition,
    UserAuthAccessRole,
    UserAuthEmployee,
    UserAuthCrudUser,
    UserAuthBotUser
)

from .models import metadata

models = {
    "JobPosition": UserAuthJobPosition,
    "AccessRole": UserAuthAccessRole,
    "Employee": UserAuthEmployee,
    "CrudUser": UserAuthCrudUser,
    "BotUser": UserAuthBotUser,
}

__all__ = ["models", "metadata"]


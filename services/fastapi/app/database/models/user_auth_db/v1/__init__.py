from .models import *

models = {
    "JobPosition": JobPosition,
    "AccessRole": AccessRole,
    "Employee": Employee,
    "CrudUser": CrudUser,
    "BotUser": BotUser,
}

__all__ = ["models", "metadata"]


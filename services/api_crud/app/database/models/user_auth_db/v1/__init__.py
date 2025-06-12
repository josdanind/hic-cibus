from .models import (
    UserAuthJobPosition,
    UserAuthAccessRole,
    UserAuthEmployee,
    UserAuthCrudUser,
    UserAuthBotUser
)

from .models import metadata

class CrudModelTypes:
    JopPosition: type = UserAuthJobPosition
    AccessRole: type = UserAuthAccessRole
    Employee: type = UserAuthEmployee
    CrudUser: type = UserAuthCrudUser
    BotUser: type = UserAuthBotUser


# __all__ = ["metadata", "CrudModelTypes"]


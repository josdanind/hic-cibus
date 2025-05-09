from .models import (
    Role,
    BotAccessRole,
    BotModelStatus,
    BotStatus,
    BotEnvironment,
    BotCategory,
    SubscriptionStatus,
    SubscriptionPeriod,
    PaymentStatus
)

from .models import (
    Employee, 
    Company,
    CompanyContact,
    BotModel,
    Bot,
    BotCredential,
    BotUser
)

from .models import (
    BotCategoryLink,
    UserBotLink,
    Subscription,
    SubscriptionPayment
)

from .models import metadata 

models = {
    # 📚 Catálogos base (sin dependencias o usadas por otras)
    "Role": Role,
    "BotAccessRole": BotAccessRole,
    "BotModelStatus": BotModelStatus,
    "BotStatus": BotStatus,
    "BotEnvironment": BotEnvironment,
    "BotCategory": BotCategory,
    "SubscriptionStatus": SubscriptionStatus,
    "SubscriptionPeriod": SubscriptionPeriod,
    "PaymentStatus": PaymentStatus,

    # 🗄 Núcleo (con relaciones controladas por FKs previas)
    "Employee": Employee,                 # → Role
    "Company": Company,                   # independiente
    "CompanyContact": CompanyContact,     # → Employee
    "BotModel": BotModel,                 # → BotModelStatus
    "Bot": Bot,                           # → BotModel, BotStatus, BotEnvironment
    "BotCredential": BotCredential,       # → Bot
    "BotUser": BotUser,                   # → Employee, BotUserPermission

    # 🔗 Tablas de relación M:N (requieren entidades anteriores)
    "BotCategoryLink": BotCategoryLink,   # → Bot, BotCategory
    "UserBotLink": UserBotLink,           # → BotUser, Bot

    # 🔄 Entidades transaccionales
    "Subscription": Subscription,         # → Bot, Company, SubscriptionStatus, SubscriptionPeriod
    "SubscriptionPayment": SubscriptionPayment,  # → Subscription, PaymentStatus
}

__all__ = ["models", "metadata"]
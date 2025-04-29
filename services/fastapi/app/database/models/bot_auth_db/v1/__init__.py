from .models import *

models = {
    # 📚 Catálogos base (sin dependencias o usadas por otras)
    "Role": Role,
    "BotUserPermission": BotUserPermission,
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
# Modelos base (sin dependencias)
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

# Modelos del núcleo
from .models import (
    Employee,
    Company,
    CompanyContact,
    BotModel,
    Bot,
    BotCredential,
    BotUser
)

# Modelos de relación M:N
from .models import (
    BotCategoryLink,
    UserBotLink,
    Subscription,
    SubscriptionPayment
)

# Metadata
from .models import metadata

class BotModelTypes:
    """
    Namespace para acceder a los tipos de modelos de la aplicación.
    Permite el tipado estático y el acceso directo a las clases de los modelos.
    """
    # 📚 Catálogos base (sin dependencias o usadas por otras)
    Role: type = Role
    BotAccessRole: type = BotAccessRole
    BotModelStatus: type = BotModelStatus
    BotStatus: type = BotStatus
    BotEnvironment: type = BotEnvironment
    BotCategory: type = BotCategory
    SubscriptionStatus: type = SubscriptionStatus
    SubscriptionPeriod: type = SubscriptionPeriod
    PaymentStatus: type = PaymentStatus

    # 🗄 Núcleo (con relaciones controladas por FKs previas)
    Employee: type = Employee                 # → Role
    Company: type = Company                   # independiente
    CompanyContact: type = CompanyContact     # → Employee
    BotModel: type = BotModel                 # → BotModelStatus
    Bot: type = Bot                           # → BotModel, BotStatus, BotEnvironment
    BotCredential: type = BotCredential       # → Bot
    BotUser: type = BotUser                   # → Employee, BotAccessRole (asumo que BotUserPermission era un typo por BotAccessRole o similar)

    # 🔗 Tablas de relación M:N (requieren entidades anteriores)
    BotCategoryLink: type = BotCategoryLink   # → Bot, BotCategory
    UserBotLink: type = UserBotLink           # → BotUser, Bot

    # 🔄 Entidades transaccionales
    Subscription: type = Subscription         # → Bot, Company, SubscriptionStatus, SubscriptionPeriod
    SubscriptionPayment: type = SubscriptionPayment # → Subscription, PaymentStatus

# __all__ = ["metadata", "BotModelTypes"]
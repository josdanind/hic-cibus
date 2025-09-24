
#  ╭──────────────────────────────────────────────────────────────╮
#  │ 📝 1. METADATA                                               │
#  │    Importa el objeto 'metadata', que contiene la             │
#  │    metainformación de la base de datos, como definiciones de │
#  │    base de datos, como definiciones de tablas y relaciones.  │
#  ╰──────────────────────────────────────────────────────────────╯

from .models import metadata

#  ╭──────────────────────────────────────────────────────╮
#  │ 📚 1. TABLAS - Catálogos base                        │
#  ╰──────────────────────────────────────────────────────╯

from .models import (
    BotModelStatus,
    BotStatus,
    ProcessTemplate,
    BotEnvironment,
    BotCategory,
    Magnitude,
    Manufacturer,
    SubscriptionStatus,
    PeriodUnit,
    InvoiceStatus,
    PaymentStatus,
    PaymentMethod,
    UserProcessPermission,
    BotProcessPermission,
    Role,
    SubprocessType,
)

#  ╭───────────────────────────────────────────────────────╮
#  │ 🗂️ 2. TABLAS - Catálogos dependientes                 │
#  ╰───────────────────────────────────────────────────────╯

from .models import (
    Plan,
    BotModel,
    SensorModel,
    ActuatorModel,
    ControllerModel,
)

#  ╭──────────────────────────────────────────────────────╮
#  │ 🏢 3. TABLAS - Datos maestro                         │
#  ╰──────────────────────────────────────────────────────╯

from .models import (
    Company,
    Employee,
    CompanyContact,
    EmployeeRoleLink,
    Bot,
    BotCredential,
    Subscription,
    BotCategoryLink,
)

#  ╭──────────────────────────────────────────────────────╮
#  │ 🌐 4. TABLAS - Componentes IoT y hardware físico     │
#  ╰──────────────────────────────────────────────────────╯

from .models import (
    OperationalUnit,
    Process,
    SubprocessGroup,
    Subprocess,
    ControllerDevice,
    Sensor,
    Actuator,
    SensorModelMagnitudeLink,
    ActuatorModelMagnitudeLink
)

# ╭──────────────────────────────────────────────────────╮
# │ ⚙️ 5. TABLAS - Uso y operación                       │
# ╰──────────────────────────────────────────────────────╯

from .models import (
    BotUser,
    BotUserSubscriptionLink,
    BotProcess,
    UserProcess
)

# ╭──────────────────────────────────────────────────────╮
# │ 💰 6. TABLAS - Facturación y pagos                   │
# ╰──────────────────────────────────────────────────────╯

from .models import (
    SubscriptionPeriod,
    Invoice,
    Payment,
    PaymentAttempt
)

# ╭──────────────────────────────────────────────────────╮
# │ 🛡️ 7. TABLAS - Permisos                              │
# ╰──────────────────────────────────────────────────────╯

from .models import (
    BotProcessPermissionLink,
    UserProcessPermissionLink,
)

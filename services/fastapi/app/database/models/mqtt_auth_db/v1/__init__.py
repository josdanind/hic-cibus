from .models import MqttUser
from .models import metadata

class MqttModelTypes:
    User: type = MqttUser

__all__ = ["metadata", "MqttModelTypes"]

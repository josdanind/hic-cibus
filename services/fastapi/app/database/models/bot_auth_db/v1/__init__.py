from .models import (
    BotModelStatus,
    BotStatus,
    BotEnvironment,
    BotCategory,
    BotModel,
    Bot,
    BotCredential,
    BotCategoryLink
)

models = {
    "BotModelStatus": BotModelStatus,       # base para BotModel
    "BotStatus": BotStatus,                 # base para Bot
    "BotEnvironment": BotEnvironment,       # base para Bot
    "BotCategory": BotCategory,             # base para BotCategoryLink
    "BotModel": BotModel,                   # depende de BotModelStatus
    "Bot": Bot,                             # depende de BotModel, BotStatus, BotEnvironment
    "BotCredential": BotCredential,         # depende de Bot
    "BotCategoryLink": BotCategoryLink      # depende de Bot y BotCategory
}

__all__ = ["models"]
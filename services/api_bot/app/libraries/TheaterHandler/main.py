# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería estándar
import re
from dataclasses import dataclass
from functools import wraps
from typing import Callable, Awaitable, Any

# 🧩 Terceros
import redis.asyncio as aioredis
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from telebot.types import Update


# 🏗️  Módulos internos de la librería
from .utils.http_client import HttpClient


@dataclass
class UserCtx:
    chat_id: int
    message_id: int
    first_name: str
    username: str
    user_id: int | None = None


def build_user_ctx(message: types.Message) -> UserCtx:
    # Asegúrate de que sea un chat privado 1:1 con el bot
    if message.chat.type != "private":
        raise ValueError("build_user_ctx está pensado solo para DM (private).")

    return UserCtx(
        chat_id=message.chat.id,
        message_id=message.message_id,
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )


class TheaterHandler:
    def __init__(
        self,
        *,
        bot_name: str,
        bot_token: str,
        api_client: HttpClient,
        valkey_client: aioredis.Redis,
        parse_mode: str = "HTML",
    ) -> None:
        self.bot_name = bot_name
        self.bot = AsyncTeleBot(token=bot_token, parse_mode=parse_mode)
        self.http = api_client
        self.valkey_client = valkey_client
        self.parse_mode = parse_mode

    # ──────────────────────────────
    # Delegación de atributos
    # ──────────────────────────────
    def __getattr__(self, name):
        return getattr(self.bot, name)

    # ──────────────────────────────
    # Handler para comandos
    # ──────────────────────────────
    def cmd(self, *names: str):
        return self.bot.message_handler(commands=list(names))

    # ────────────────────────────────────────────────────────────
    # Handler para comandos con contexto de usuario
    # ────────────────────────────────────────────────────────────
    def cmd_with_ctx(self, *names: str) -> Callable:
        """
        Decorador para comandos que inyecta un contexto de usuario.
        """
        def _decorator(func: Callable[[types.Message, UserCtx], Awaitable[Any]]):
            @self.bot.message_handler(commands=list(names))
            @wraps(func)
            async def _wrapper(message: types.Message):
                ctx = build_user_ctx(message)
                return await func(message, ctx)
            return _wrapper

        return _decorator

    # ──────────────────────────────
    # Handler para callbacks inline
    # ──────────────────────────────
    def callback(self, *callback_data: str, regex: str | None = None):
        if callback_data and regex:
            raise ValueError("No se puede usar 'callback_data' y 'regex' al mismo tiempo.")

        # 1️⃣  FILTRA los callbacks según los datos proporcionados
        if callback_data:
            allowed = set(callback_data)

            def flt(c):
                data = getattr(c, 'data', None)
                return data in allowed

        elif regex:
            try:
                rp = re.compile(regex)
            except re.error as exc:
                raise ValueError(f"Regex inválido: {exc}") from exc

            def flt(c, _rp=rp):
                data = getattr(c, "data", "")
                return bool(_rp.search(data))

        else:
            flt = lambda c: True

        # 2️⃣  DEVUELVE el decorador original del TeleBot
        return self.bot.callback_query_handler(func=flt)


    # ──────────────────────────────
    # Caché (Valkey)
    # ──────────────────────────────
    async def _cache_get_value(self, key: str):
        pass

    # ──────────────────────────────
    # HELPERS DE WEBHOOK
    # ──────────────────────────────
    async def set_webhook(
        self,
        url: str,
        *,
        secret_token: str | None = None,
        drop_updates: bool = True,
        allowed_updates: list[str] | None = None,
    ):
        await self.bot.delete_webhook()
        await self.bot.set_webhook(
            url=url,
            secret_token=secret_token,
            drop_pending_updates=drop_updates,
            allowed_updates=allowed_updates,
        )

    async def delete_webhook(self):
        await self.bot.delete_webhook()

    # ──────────────────────────────
    # UPDATE
    # ──────────────────────────────
    async def process_update(self, update_json: dict):
        upd: Update = Update.de_json(update_json)
        await self.bot.process_new_updates([upd])

    # ──────────────────────────────
    # Peticiones HTTP
    # ──────────────────────────────
    async def load_companies(self):
        data: dict = await self.http.get(
            "companies_info",
            params={"bot_name": self.bot_name }
        )

        for company, data in data.items():
            sub_is_active = data["subscription_active"]
            await self.valkey_client.set(f"sub:{company}:is_active", int(sub_is_active))


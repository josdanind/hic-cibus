# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería estándar
import re

# 🧩 Terceros
import redis.asyncio as aioredis
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Update

# 🏗️  Módulos internos de la librería

class TheaterHandler:
    def __init__(
        self,
        *,
        bot_token: str,
        api_crud_url: str,
        valkey_client: aioredis.Redis,
        parse_mode: str = "HTML",
    ) -> None:
        self.bot = AsyncTeleBot(token=bot_token, parse_mode=parse_mode)
        self.api_crud_url = api_crud_url,
        self.walkey_client = valkey_client,
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

    # ──────────────────────────────
    # Handler para callbacks inline
    # ──────────────────────────────
    def callback(self, *callback_data: str, regex: str | None = None):
        if callback_data and regex:
            raise ValueError("No se puede usar 'callback_data' y 'regex' al mismo tiempo.")

        # 1️⃣  FILTRA los callbacks según los datos proporcionados
        if callback_data:
            allowed = set(callback_data)
            flt = lambda c: c.data in allowed

        elif regex:
            try:
                rp = re.compile(regex)
            except re.error as exc:
                raise ValueError(f"Regex inválido: {exc}") from exc

            flt = lambda c, _rp=rp: bool(_rp.match(c.data or ""))

        else:
            flt = lambda c: True

        # 2️⃣  DEVUELVE el decorador original del TeleBot
        return self.bot.callback_query_handler(func=flt)


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
        upd: Update = self.bot.types.Update.de_json(update_json)
        await self.bot.process_new_updates([upd])
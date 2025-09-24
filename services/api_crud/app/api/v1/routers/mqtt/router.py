# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Terceros
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession

# 🏗️  Módulos internos de la aplicación
from app.database import get_mqtt_crud, DATABASES
from app.core.config import settings

# 🧱 Modelos y esquemas
from app.database.models.mqtt_users_db import MqttUser as MqttUserModel

# 🔐 Autenticación para Usuarios CRUD
from ..crud.auth import decode_token as user_crud_decode_token

router = APIRouter()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="crud_user/auth")


@router.get(
    "",
    response_model=list[tuple] | tuple,
    summary="Obtiene uno o todos los usuarios MQTT"
)
async def get_mqtt_user(
    token: str = Depends(oauth2_schema),
    crud_manager: AsyncSession = Depends(get_mqtt_crud),
    username: str | None = None
):
    # Verifica Token de usuario CRUD
    await user_crud_decode_token(token=token)

    if username:
        mqtt_user = await crud_manager.get(
            MqttUserModel,
            {"username": username},
            single_result=True
        )

        return (
            mqtt_user.id, mqtt_user.username, mqtt_user.is_superuser
        ) if mqtt_user else ()

    mqtt_users = await crud_manager.get(MqttUserModel)

    return [(user.id, user.username, user.is_superuser) for user in mqtt_users]
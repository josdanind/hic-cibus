# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🧩 Terceros
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import aiohttp

# 🏗️  Módulos internos de la aplicación
from app.schemas.auth import Token
from app.schemas.bot import BotCredential as BotCredentialSchema
from app.libraries.CRUDManager import CRUDManager
from app.database import get_tlaloc_crud
from app.database import DATABASES
from app.utils.rich_format import print_panel
from app.utils.http_exceptions import not_found

# 🧱 Modelos y esquemas
from app.database.models.tlaloc_db.V2 import (
    Bot,
    BotCredential
)

# 🚦 Utilidades del router
from .auth import generate_access_token
from .auth import decode_token as user_crud_decode_token

router = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="crud_user/auth")

@router.post("/auth", response_model=Token)
async def login_for_access_token(
    form_data:OAuth2PasswordRequestForm = Depends()
):
    """
    Autentica al usuario y genera un token de acceso.

    - **Requiere**: Nombre de usuario y contraseña.
    - **Retorna**: Un token JWT si las credenciales son correctas.
    - **Error**: Devuelve un error 401 si las credenciales son inválidas.
    """
    username, password = form_data.username, form_data.password

    access_token = await generate_access_token(username, password)

    return Token(access_token=access_token)

@router.post(
    "/create_bot_credential",
    status_code=status.HTTP_200_OK
)
async def create_bot_credential(
    register_credential: BotCredentialSchema,
    token: str = Depends(oauth2_schema),
    crud_manager: CRUDManager  = Depends(get_tlaloc_crud)
):
    """
    Crea o actualiza las credenciales para un bot existente.
    - Si el bot no existe → 404
    - Si no tiene credenciales → crea
    - Si ya tiene → actualiza
    """
    await user_crud_decode_token(token=token)

    bot = await crud_manager.get(
        Bot,
        {"name": register_credential.name},
        single_result=True,
        load_options = [selectinload(Bot.credentials)]
    )

    if bot is None:
        raise not_found(f"El bot '{register_credential.name}' no existe")

    creating = bot.credentials is None

    if creating:
        bot_credential = await crud_manager.add(
            BotCredential(
                bot_id=bot.id,
                hashed_password=register_credential.password
            )
        )
        action = "creadas"
    else:
        bot_credential = await crud_manager.update(
            model=BotCredential,
            filters={"bot_id": bot.id},
            data={"hashed_password": register_credential.password}
        )
        action = f"actualizadas"

    print_panel(
        title=f"Credenciales del bot {bot.name} {action}",
        messages=[
            (
                BotCredential.__tablename__,
                f"id: {bot_credential.id}, bot_id: {bot_credential.bot_id}"
            ),
        ],
        style="check arrow",
    )


    return {"message": f"Las credenciales del bot '{bot.name}' han sido {action} exitosamente."}

# @router.post("/register_bot")
# async def register_bot(
#     register_bot: RegisterBot,
#     token: str = Depends(oauth2_schema),
#     # crud_manager: CRUDManager  = Depends(get_bot_crud),
# ):
#     """
#     Registra un bot en el sistema.

#     - **Requiere**: Token de acceso válido.
#     - **Retorna**: Información del bot registrado.
#     - **Error**: Devuelve un error 401 si el token es inválido.
#     """
#     await user_crud_decode_token(token=token)

#     bot_data = await crud_manager.get(
#         BotModel,
#         {"name": register_bot.name},
#         single_result=True,
#         load_options = [selectinload(BotModel.credentials)]
#     )

#     if not bot_data:
#         bot_model = BotModel(
#             name=register_bot.name,
#             api_url=register_bot.api_url,
#             bot_model_id=register_bot.bot_model_id,
#         )

#         bot = await crud_manager.add(bot_model)

#         bot_credentials_model = BotCredentialModel(
#             hashed_password=register_bot.password,
#             bot_id=bot.id,
#         )

#         bot_credentials = await crud_manager.add(bot_credentials_model)

#         print_panel(
#             title="Registros creados en bot_auth_db",
#             messages=[
#                 (
#                     BotModel.__tablename__,
#                     f"id: {bot.id}, name: {bot.name} "
#                 ),
#                 (
#                     BotCredentialModel.__tablename__,
#                     f"id: {bot_credentials.id}, bot_id: {bot_credentials.bot_id}"
#                 ),
#             ],
#             style="check arrow",
#         )
#         message = f"El Bot {bot.name} ha sido registrado exitosamente."

#     else:
#         message = f"El Bot {bot_data.name} ya está registrado."

#     return {"message": message}

# @router.post("/ping_bot/")
# async def ping_bot(
#     bot_name:str,
#     token: str = Depends(oauth2_schema),
#     crud_manager: CRUDManager  = Depends(get_bot_crud)
# ):
#     await user_crud_decode_token(token=token)

#     bot_data = await crud_manager.get(
#         BotModel,
#         {"name": bot_name},
#         single_result=True,
#         load_options = [selectinload(BotModel.credentials)]
#     )

#     if not bot_data:
#         raise not_found(f"El bot '{bot_name}' no existe")

#     bot_url = bot_data.api_url + "/ping"
#     credential = bot_data.credentials

#     headers = {
#         "Hashed-Token": credential.hashed_api_access_token
#     }

#     async with aiohttp.ClientSession() as session:
#         async with session.get(bot_url, headers=headers) as response:
#             if response.status >= 400:
#                 # 🔴 Token inválido u otro error
#                 try:
#                     error_data = await response.json()
#                     detail = error_data.get("detail", "Error desconocido")
#                 except Exception:
#                     detail = await response.text()

#                 raise HTTPException(status_code=response.status, detail=detail)

#             # ✅ Token válido
#             return await response.json()
# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería Estándar
from typing import Annotated

# 🧩 Terceros
from fastapi import APIRouter, Depends, Query
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from sqlalchemy.ext.asyncio import AsyncSession

# 🏗️  Módulos internos de la aplicación
from app.schemas.auth import Token
from app.schemas.bot import BotTokenPayload
from app.libraries.CRUDManager import CRUDManager
from app.database import get_tlaloc_crud
from .sql import get_companies_sql

# 🛠️ Utilidades del router
from .auth import (
    generate_access_token,
    get_current_subject
)

router = APIRouter()

@router.post("/auth", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    crud_manager: CRUDManager = Depends(get_tlaloc_crud)
):
    bot_name, password = form_data.username, form_data.password

    access_token = await generate_access_token(
        bot_name,
        password,
        crud_manager
    )

    return Token(access_token=access_token)


@router.get("/companies_info")
async def get_companies_info(
    payload: Annotated[BotTokenPayload, Depends(get_current_subject)] ,
    bot_name:str = Query(..., description="Nombre del bot"),
    crud_manager: CRUDManager = Depends(get_tlaloc_crud),
):
    session: AsyncSession = crud_manager.session

    companies = (await session.execute(
        get_companies_sql,
        {"bot_name": bot_name}
    )).scalar_one_or_none()

    return companies


# @router.get("/test")
# async def test(
#     bot_name:str = Query(..., description="Nombre del bot"),
#     crud_manager: CRUDManager = Depends(get_tlaloc_crud)
# ):
#     session: AsyncSession = crud_manager.session

#     conditions = [
#         (Bot.name == bot_name),
#         (Subscription.bot_id == Bot.id),
#         (Subscription.company_id == Company.id),
#         Subscription.is_active.is_(True),
#     ]

#     stmt = (
#         select(Company)
#         .select_from(Company)
#         .where(*conditions)
#     )

#     rows = (await session.execute(stmt)).mappings().all()

#     print(rows)


# @router.get("/test_sql")
# async def test_sql(
#     container_label:str = Query(..., description="Etiqueta del contenedor"),
#     crud_manager: CRUDManager = Depends(get_tlaloc_crud)
# ):
#     session: AsyncSession = crud_manager.session

#     result = await crud_manager.get(
#         QueryModel,
#         {"name": "all_container_items"},
#         single_result=True
#     )

#     print(result.sql_template)
#     print(container_label)
#     sql_template = text(result.sql_template)

#     rows: list[str] = (
#         await session.execute(sql_template, {"label": container_label})
#     ).scalars().all()

#     print(rows)

#     return {"message": "SQL works!"}

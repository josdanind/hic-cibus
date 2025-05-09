# ────────────────
# 📦 Importaciones
# ────────────────
# Librería estándar
from typing import Type

# Librerías de terceros
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession

# ────────────────────────────────────────────────
# 📚 Gestor CRUD genérico para modelos SQLModel
# ────────────────────────────────────────────────
class CRUDManager:
    """
    Gestor CRUD que opera sobre cualquier modelo usando una sesión específica.
    """
    single_result_keys = {"id", "telegram_username", "telegram_id"}

    def __init__(self, session: AsyncSession):
        self.session = session # Sesión de la base de datos

    async def get(
        self,
        model: Type[SQLModel],
        filters: dict | None = None
    ) -> SQLModel | list[SQLModel] | None:
        """
        Obtiene un registro o una lista de registros según la condición dada.
        """
        async with self.session() as session:
            stmt = select(model)

            if filters:
                for key, value in filters.items():
                    column = getattr(model, key, None)
                    if column is None:
                        raise ValueError(
                            f"El campo '{key}' no existe en el modelo '{model.__name__}'"
                        )
                    stmt = stmt.where(column == value)

            result = await session.execute(stmt)

            if filters and (self.single_result_keys & filters.keys()):
                return result.scalar_one_or_none()

            return result.scalars().all()

    async def create(
        self,
        model: Type[SQLModel],
        data: dict
    ) -> SQLModel:
        """
        Crea un nuevo registro en la base de datos.
        """
        async with self.session() as session:
            db_model = model(**data)
            session.add(db_model)
            await session.commit()
            await session.refresh(db_model)

            return db_model

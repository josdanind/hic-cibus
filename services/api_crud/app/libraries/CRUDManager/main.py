# ────────────────
# 📦 Importaciones
# ────────────────
# Librería estándar
from typing import Type, Any, Sequence

# Librerías de terceros
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import strategy_options
from sqlalchemy.sql.selectable import Select

# ────────────────────────────────────────────────
# 📚 Gestor CRUD genérico para modelos SQLModel
# ────────────────────────────────────────────────
class CRUDManager:
    """
    Gestor CRUD que opera sobre cualquier modelo usando una sesión específica.
    """
    single_result_keys = {"id", "telegram_username", "telegram_id", "username"}

    def __init__(self, session: AsyncSession):
        self.session = session # Sesión de la base de datos

    async def get(
        self,
        model: Type[SQLModel],
        filters: dict | None = None,
        load_options: Sequence[strategy_options.LoaderOption] | None = None
    ) -> SQLModel | list[SQLModel] | None:
        """
        Obtiene un registro o una lista de registros según la condición dada.
        """
        stmt: Select = select(model)

        if filters:
            for key, value in filters.items():
                column = getattr(model, key, None)
                if column is None:
                    raise ValueError(
                        f"El campo '{key}' no existe en el modelo '{model.__name__}'"
                    )
                stmt = stmt.where(column == value)

        if load_options:
            stmt = stmt.options(*load_options)

        result = await self.session.execute(stmt)

        if filters and (self.single_result_keys & filters.keys()):
            return result.scalar_one_or_none()

        return result.scalars().all()

    async def add(
        self,
        model: SQLModel,
    ) -> SQLModel:
        """
        Crea un nuevo registro en la base de datos.
        """
        self.session.add(model)

        try:
            await self.session.commit()
            await self.session.refresh(model)
            return model
        except:
            await self.session.rollback()
            raise

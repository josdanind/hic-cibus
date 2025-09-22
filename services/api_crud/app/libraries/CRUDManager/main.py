# ────────────────
# 📦 Importaciones
# ────────────────
# Librería estándar
from typing import Type, Sequence

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
    def __init__(self, session: AsyncSession):
        self.session = session # Sesión de la base de datos

    async def get(
        self,
        model: Type[SQLModel],
        filters: dict | None = None,
        single_result: bool = False,
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

        if filters and single_result:
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

    async def update(
        self,
        model: SQLModel,
        filters: dict,
        data:dict,
        load_options: Sequence[strategy_options.LoaderOption] | None = None
    ):
        """
        Actualiza un registro existente en la base de datos.

        - **Parámetros**:
            - `model` (SQLModel): Modelo a actualizar.
            - `filters` (dict): Condiciones para identificar el registro a actualizar.
            - `data` (dict): Datos a actualizar.
        """
        if not filters:
            raise ValueError("Debes proporcionar al menos un filtro para evitar updates masivos.")

        valid_cols = set(model.model_fields.keys())
        invalid = (data.keys() - valid_cols) | (filters.keys() - valid_cols)

        if invalid:
            raise ValueError(f"Campos no válidos para {model.__name__}: {', '.join(invalid)}")

        to_update: list[SQLModel]

        to_update = await self.get(
            model=model,
            filters=filters,
            load_options=load_options,
        )

        if not to_update:
            return None

        for obj in to_update:
            for attr, value in data.items():
                setattr(obj, attr, value)

        try:
            await self.session.commit()
            for obj in to_update:
                await self.session.refresh(obj)
        except Exception:
            await self.session.rollback()
            raise

        return to_update[0] if len(to_update) == 1 else to_update
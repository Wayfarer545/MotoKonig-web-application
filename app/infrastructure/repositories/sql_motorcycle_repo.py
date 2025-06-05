# app/infrastructure/repositories/sql_motorcycle_repo.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.motorcycle import EngineType, Motorcycle, MotorcycleType
from app.domain.ports.motorcycle_repository import IMotorcycleRepository
from app.domain.ports.motorcycle_specification import MotorcycleSpecificationPort
from app.infrastructure.models.motorcycle_model import Motorcycle as MotorcycleModel


class SqlMotorcycleRepository(IMotorcycleRepository):
    """SQLAlchemy реализация репозитория мотоциклов"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, motorcycle: Motorcycle) -> Motorcycle:
        """Добавить новый мотоцикл"""
        db_motorcycle = MotorcycleModel(
            owner_id=motorcycle.owner_id,
            brand=motorcycle.brand,
            model=motorcycle.model,
            year=motorcycle.year,
            engine_volume=motorcycle.engine_volume,
            engine_type=motorcycle.engine_type,
            motorcycle_type=motorcycle.motorcycle_type,
            power=motorcycle.power,
            mileage=motorcycle.mileage,
            color=motorcycle.color,
            description=motorcycle.description,
            is_active=motorcycle.is_active
        )

        self.session.add(db_motorcycle)
        await self.session.flush()
        await self.session.refresh(db_motorcycle)

        # Обновляем доменную сущность
        motorcycle.id = db_motorcycle.id
        motorcycle.created_at = db_motorcycle.created_at
        motorcycle.updated_at = db_motorcycle.updated_at

        return motorcycle

    async def get(self, spec: MotorcycleSpecificationPort) -> Motorcycle | None:
        """Получить мотоцикл по спецификации"""
        statement = spec.to_query(select(MotorcycleModel))
        result = await self.session.execute(statement)
        db_motorcycle = result.scalar_one_or_none()

        if db_motorcycle:
            return self._to_domain_entity(db_motorcycle)
        return None

    async def get_list(self, spec: MotorcycleSpecificationPort | None = None) -> list[Motorcycle]:
        """Получить список мотоциклов по спецификации"""
        statement = select(MotorcycleModel)

        if spec:
            statement = spec.to_query(statement)

        result = await self.session.execute(statement)
        motorcycles = result.scalars().all()

        return [self._to_domain_entity(m) for m in motorcycles]

    async def update(self, motorcycle: Motorcycle) -> Motorcycle:
        """Обновить мотоцикл"""
        db_motorcycle = await self.session.get(MotorcycleModel, motorcycle.id)

        if db_motorcycle:
            # Обновляем поля
            db_motorcycle.brand = motorcycle.brand
            db_motorcycle.model = motorcycle.model
            db_motorcycle.year = motorcycle.year
            db_motorcycle.engine_volume = motorcycle.engine_volume
            db_motorcycle.engine_type = motorcycle.engine_type
            db_motorcycle.motorcycle_type = motorcycle.motorcycle_type
            db_motorcycle.power = motorcycle.power
            db_motorcycle.mileage = motorcycle.mileage
            db_motorcycle.color = motorcycle.color
            db_motorcycle.description = motorcycle.description
            db_motorcycle.is_active = motorcycle.is_active

            await self.session.flush()
            await self.session.refresh(db_motorcycle)

            # Обновляем timestamp в доменной сущности
            motorcycle.updated_at = db_motorcycle.updated_at

        return motorcycle

    async def delete(self, motorcycle_id: UUID) -> bool:
        """Удалить мотоцикл"""
        db_motorcycle = await self.session.get(MotorcycleModel, motorcycle_id)

        if db_motorcycle:
            await self.session.delete(db_motorcycle)
            await self.session.flush()
            return True

        return False

    def _to_domain_entity(self, db_motorcycle: MotorcycleModel) -> Motorcycle:
        """Преобразовать модель БД в доменную сущность"""
        return Motorcycle(
            motorcycle_id=db_motorcycle.id,
            owner_id=db_motorcycle.owner_id,
            brand=db_motorcycle.brand,
            model=db_motorcycle.model,
            year=db_motorcycle.year,
            engine_volume=db_motorcycle.engine_volume,
            engine_type=EngineType(db_motorcycle.engine_type.value),
            motorcycle_type=MotorcycleType(db_motorcycle.motorcycle_type.value),
            power=db_motorcycle.power,
            mileage=db_motorcycle.mileage,
            color=db_motorcycle.color,
            description=db_motorcycle.description,
            is_active=db_motorcycle.is_active,
            created_at=db_motorcycle.created_at,
            updated_at=db_motorcycle.updated_at
        )

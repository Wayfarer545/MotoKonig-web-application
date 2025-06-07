# app/application/use_cases/motorcycle/update_motorcycle.py

from uuid import UUID

from app.domain.entities.motorcycle import EngineType, Motorcycle, MotorcycleType
from app.domain.ports.epositories.motorcycle_repository import IMotorcycleRepository
from app.infrastructure.specs.moto.moto_by_id import (
    MotorcycleById,
)


class UpdateMotorcycleUseCase:
    """Use case для обновления мотоцикла"""

    def __init__(self, repo: IMotorcycleRepository):
        self.repo = repo

    async def execute(
            self,
            motorcycle_id: UUID,
            brand: str | None = None,
            model: str | None = None,
            year: int | None = None,
            engine_volume: int | None = None,
            engine_type: EngineType | None = None,
            motorcycle_type: MotorcycleType | None = None,
            power: int | None = None,
            mileage: int | None = None,
            color: str | None = None,
            description: str | None = None,
            is_active: bool | None = None,
    ) -> Motorcycle | None:
        """Обновить данные мотоцикла"""
        existing = await self.repo.get(MotorcycleById(motorcycle_id))

        if not existing:
            return None

        # Обновляем только переданные поля
        if brand is not None:
            existing.brand = brand.strip().title()
        if model is not None:
            existing.model = model.strip()
        if year is not None:
            existing._validate_year(year)
            existing.year = year
        if engine_volume is not None:
            existing._validate_engine_volume(engine_volume)
            existing.engine_volume = engine_volume
        if engine_type is not None:
            existing.engine_type = engine_type
        if motorcycle_type is not None:
            existing.motorcycle_type = motorcycle_type
        if power is not None:
            existing._validate_power(power)
            existing.power = power
        if mileage is not None:
            existing.update_mileage(mileage)
        if color is not None:
            existing.color = color.strip().title() if color else None
        if description is not None:
            existing.update_description(description)
        if is_active is not None:
            if is_active:
                existing.activate()
            else:
                existing.deactivate()

        return await self.repo.update(existing)

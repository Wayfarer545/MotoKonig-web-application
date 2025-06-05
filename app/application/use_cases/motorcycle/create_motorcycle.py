# app/application/use_cases/motorcycle/create_motorcycle.py

from uuid import UUID

from app.domain.entities.motorcycle import EngineType, Motorcycle, MotorcycleType
from app.domain.ports.motorcycle_repository import IMotorcycleRepository


class CreateMotorcycleUseCase:
    """Use case для создания нового мотоцикла"""

    def __init__(self, repo: IMotorcycleRepository):
        self.repo = repo

    async def execute(
            self,
            owner_id: UUID,
            brand: str,
            model: str,
            year: int,
            engine_volume: int,
            engine_type: EngineType,
            motorcycle_type: MotorcycleType,
            power: int | None = None,
            mileage: int | None = None,
            color: str | None = None,
            description: str | None = None,
    ) -> Motorcycle:
        """Создать новый мотоцикл"""
        motorcycle = Motorcycle(
            owner_id=owner_id,
            brand=brand,
            model=model,
            year=year,
            engine_volume=engine_volume,
            engine_type=engine_type,
            motorcycle_type=motorcycle_type,
            power=power,
            mileage=mileage,
            color=color,
            description=description
        )

        return await self.repo.add(motorcycle)

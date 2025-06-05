# app/application/use_cases/motorcycle/list_motorcycles.py

from app.domain.entities.motorcycle import Motorcycle
from app.domain.ports.motorcycle_repository import IMotorcycleRepository
from app.domain.ports.motorcycle_specification import MotorcycleSpecificationPort


class ListMotorcyclesUseCase:
    """Use case для получения списка мотоциклов"""

    def __init__(self, repo: IMotorcycleRepository):
        self.repo = repo

    async def execute(self, spec: MotorcycleSpecificationPort | None = None) -> list[Motorcycle]:
        """Получить список мотоциклов"""
        return await self.repo.get_list(spec)

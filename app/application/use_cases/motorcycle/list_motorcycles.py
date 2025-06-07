# app/application/use_cases/motorcycle/list_motorcycles.py

from app.domain.entities.motorcycle import Motorcycle
from domain.ports.repositories.motorcycle_repository import IMotorcycleRepository
from domain.ports.specs.motorcycle import MotorcycleSpecificationPort


class ListMotorcyclesUseCase:
    """Use case для получения списка мотоциклов"""

    def __init__(self, repo: IMotorcycleRepository):
        self.repo = repo

    async def execute(self, spec: MotorcycleSpecificationPort | None = None) -> list[Motorcycle]:
        """Получить список мотоциклов"""
        return await self.repo.get_list(spec)

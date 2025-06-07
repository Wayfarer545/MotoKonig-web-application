# app/application/use_cases/motorcycle/get_motorcycle.py

from app.domain.entities.motorcycle import Motorcycle
from app.domain.ports.repositories.motorcycle import IMotorcycleRepository
from app.domain.ports.specs.motorcycle import MotorcycleSpecificationPort


class GetMotorcycleUseCase:
    """Use case для получения мотоцикла"""

    def __init__(self, repo: IMotorcycleRepository):
        self.repo = repo

    async def execute(self, spec: MotorcycleSpecificationPort) -> Motorcycle | None:
        """Получить мотоцикл по спецификации"""
        return await self.repo.get(spec)

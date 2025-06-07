# app/application/use_cases/motorcycle/delete_motorcycle.py

from uuid import UUID

from app.domain.ports.repositories.motorcycle import IMotorcycleRepository


class DeleteMotorcycleUseCase:
    """Use case для удаления мотоцикла"""

    def __init__(self, repo: IMotorcycleRepository):
        self.repo = repo

    async def execute(self, motorcycle_id: UUID) -> bool:
        """Удалить мотоцикл"""
        return await self.repo.delete(motorcycle_id)

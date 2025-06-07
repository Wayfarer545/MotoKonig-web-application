# app/application/use_cases/moto_club/list_clubs.py

from app.domain.entities.moto_club import MotoClub
from domain.ports.repositories.moto_club_repository import IMotoClubRepository
from domain.ports.specs.moto_club import MotoClubSpecificationPort


class ListMotoClubsUseCase:
    """Use case для получения списка мотоклубов"""

    def __init__(self, repo: IMotoClubRepository):
        self.repo = repo

    async def execute(self, spec: MotoClubSpecificationPort | None = None) -> list[MotoClub]:
        """Получить список мотоклубов"""
        return await self.repo.get_list(spec)

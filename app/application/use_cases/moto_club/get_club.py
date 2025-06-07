# app/application/use_cases/moto_club/get_club.py

from app.domain.entities.moto_club import MotoClub
from app.domain.ports.epositories.moto_club_repository import IMotoClubRepository
from app.domain.ports.specs.moto_club import MotoClubSpecificationPort


class GetMotoClubUseCase:
    """Use case для получения мотоклуба"""

    def __init__(self, repo: IMotoClubRepository):
        self.repo = repo

    async def execute(self, spec: MotoClubSpecificationPort) -> MotoClub | None:
        """Получить мотоклуб по спецификации"""
        return await self.repo.get(spec)

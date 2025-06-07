# app/application/use_cases/moto_club/delete_club.py

from uuid import UUID

from app.domain.ports.epositories.moto_club_repository import IMotoClubRepository


class DeleteMotoClubUseCase:
    """Use case для удаления мотоклуба"""

    def __init__(self, repo: IMotoClubRepository):
        self.repo = repo

    async def execute(self, club_id: UUID) -> bool:
        """Удалить мотоклуб"""
        return await self.repo.delete(club_id)

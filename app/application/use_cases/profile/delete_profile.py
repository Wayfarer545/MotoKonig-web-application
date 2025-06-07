# app/application/use_cases/profile/delete_profile.py

from uuid import UUID

from app.domain.ports.repositories.profile import IProfileRepository


class DeleteProfileUseCase:
    """Use case для удаления профиля"""

    def __init__(self, repo: IProfileRepository):
        self.repo = repo

    async def execute(self, profile_id: UUID) -> bool:
        """Удалить профиль"""
        return await self.repo.delete(profile_id)

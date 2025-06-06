# app/application/use_cases/profile/get_profile.py

from app.domain.entities.profile import Profile
from app.domain.ports.profile_repository import IProfileRepository
from app.domain.ports.profile_specification import ProfileSpecificationPort


class GetProfileUseCase:
    """Use case для получения профиля"""

    def __init__(self, repo: IProfileRepository):
        self.repo = repo

    async def execute(self, spec: ProfileSpecificationPort) -> Profile | None:
        """Получить профиль по спецификации"""
        return await self.repo.get(spec)

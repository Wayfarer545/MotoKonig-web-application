# app/application/use_cases/social_link/remove_social_link.py

from uuid import UUID

from app.domain.entities.social_link import SocialPlatform
from app.domain.ports.repositories.social_link import ISocialLinkRepository


class RemoveSocialLinkUseCase:
    """Use case для удаления социальной ссылки"""

    def __init__(self, repo: ISocialLinkRepository):
        self.repo = repo

    async def execute(self, profile_id: UUID, platform: SocialPlatform) -> bool:
        """Удалить социальную ссылку"""
        return await self.repo.delete_by_profile_and_platform(profile_id, platform)

# app/application/use_cases/social_link/get_profile_social_links.py

from uuid import UUID

from app.domain.entities.social_link import SocialLink
from app.domain.ports.epositories.social_link_repository import ISocialLinkRepository
from app.infrastructure.specs.social_link.social_links_by_profile import (
    SocialLinksByProfile,
)


class GetProfileSocialLinksUseCase:
    """Use case для получения социальных ссылок профиля"""

    def __init__(self, repo: ISocialLinkRepository):
        self.repo = repo

    async def execute(self, profile_id: UUID) -> list[SocialLink]:
        """Получить все социальные ссылки профиля"""
        return await self.repo.get_list(SocialLinksByProfile(profile_id))

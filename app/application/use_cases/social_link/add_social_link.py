# app/application/use_cases/social_link/add_social_link.py

from uuid import UUID

from app.domain.entities.social_link import PrivacyLevel, SocialLink, SocialPlatform
from app.domain.ports.social_link_repository import ISocialLinkRepository
from app.infrastructure.specs.social_link.social_link_by_profile_and_platform import (
    SocialLinkByProfileAndPlatform,
)


class AddSocialLinkUseCase:
    """Use case для добавления социальной ссылки"""

    def __init__(self, repo: ISocialLinkRepository):
        self.repo = repo

    async def execute(
            self,
            profile_id: UUID,
            platform: SocialPlatform,
            url: str,
            privacy_level: PrivacyLevel = PrivacyLevel.FRIENDS_ONLY,
    ) -> SocialLink:
        """Добавить новую социальную ссылку"""

        # Проверяем, нет ли уже ссылки для этой платформы
        existing = await self.repo.get(
            SocialLinkByProfileAndPlatform(profile_id, platform)
        )

        if existing:
            # Обновляем существующую ссылку
            existing.update_url(url)
            existing.set_privacy(privacy_level)
            return await self.repo.update(existing)
        else:
            # Создаем новую ссылку
            social_link = SocialLink(
                profile_id=profile_id,
                platform=platform,
                url=url,
                privacy_level=privacy_level,
            )
            return await self.repo.add(social_link)

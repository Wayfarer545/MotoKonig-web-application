# app/domain/ports/social_link_repository.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.social_link import SocialLink, SocialPlatform
from app.domain.ports.specs.social_link import SocialLinkSpecificationPort


class ISocialLinkRepository(Protocol):
    """Порт репозитория социальных ссылок"""

    async def add(self, social_link: SocialLink) -> SocialLink:
        """Добавить новую социальную ссылку"""
        ...

    async def get(self, spec: SocialLinkSpecificationPort) -> SocialLink | None:
        """Получить социальную ссылку по спецификации"""
        ...

    async def get_list(self, spec: SocialLinkSpecificationPort | None = None) -> list[SocialLink]:
        """Получить список социальных ссылок по спецификации"""
        ...

    async def update(self, social_link: SocialLink) -> SocialLink:
        """Обновить социальную ссылку"""
        ...

    async def delete(self, link_id: UUID) -> bool:
        """Удалить социальную ссылку"""
        ...

    async def delete_by_profile_and_platform(self, profile_id: UUID, platform: SocialPlatform) -> bool:
        """Удалить ссылку по профилю и платформе"""
        ...

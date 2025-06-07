# app/infrastructure/specifications/social_link_specs/social_link_by_profile_and_platform.py

from typing import Any
from uuid import UUID

from app.domain.entities.social_link import SocialPlatform
from app.domain.ports.specs.social_link import SocialLinkSpecificationPort
from app.infrastructure.models.social_link_model import SocialLink as SocialLinkModel


class SocialLinkByProfileAndPlatform(SocialLinkSpecificationPort):
    """Спецификация для поиска социальной ссылки по профилю и платформе"""

    def __init__(self, profile_id: UUID, platform: SocialPlatform):
        self.profile_id = profile_id
        self.platform = platform

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(
            SocialLinkModel.profile_id == self.profile_id,
            SocialLinkModel.platform == self.platform
        )

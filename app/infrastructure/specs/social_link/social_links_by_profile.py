# app/infrastructure/specs/social_link/social_links_by_profile.py

from typing import Any
from uuid import UUID

from app.domain.ports.specs.social_link import SocialLinkSpecificationPort
from app.infrastructure.models.social_link_model import SocialLink as SocialLinkModel


class SocialLinksByProfile(SocialLinkSpecificationPort):
    """Спецификация для поиска социальных ссылок по профилю"""

    def __init__(self, profile_id: UUID):
        self.profile_id = profile_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(SocialLinkModel.profile_id == self.profile_id)

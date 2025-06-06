# app/infrastructure/specs/social_link/social_link_by_id.py

from typing import Any
from uuid import UUID

from app.domain.ports.social_link_specification import SocialLinkSpecificationPort
from app.infrastructure.models.social_link_model import SocialLink as SocialLinkModel


class SocialLinkById(SocialLinkSpecificationPort):
    """Спецификация для поиска социальной ссылки по ID"""

    def __init__(self, link_id: UUID):
        self.link_id = link_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(SocialLinkModel.id == self.link_id)
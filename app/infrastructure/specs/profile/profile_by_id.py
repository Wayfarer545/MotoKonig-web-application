# app/infrastructure/specs/profile/profile_by_id.py

from typing import Any
from uuid import UUID

from app.domain.ports.profile_specification import ProfileSpecificationPort
from app.infrastructure.models.profile_model import Profile as ProfileModel


class ProfileById(ProfileSpecificationPort):
    """Спецификация для поиска профиля по ID"""

    def __init__(self, profile_id: UUID):
        self.profile_id = profile_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(ProfileModel.id == self.profile_id)

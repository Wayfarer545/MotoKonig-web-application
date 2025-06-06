# app/infrastructure/specs/profile/profile_by_user_id.py

from typing import Any
from uuid import UUID

from app.domain.ports.profile_specification import ProfileSpecificationPort
from app.infrastructure.models.profile_model import Profile as ProfileModel


class ProfileByUserId(ProfileSpecificationPort):
    """Спецификация для поиска профиля по ID пользователя"""

    def __init__(self, user_id: UUID):
        self.user_id = user_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(ProfileModel.user_id == self.user_id)

# app/infrastructure/specs/user/user_by_id.py

from typing import Any
from uuid import UUID

from app.domain.ports.epositories.user_repository import UserSpecificationPort
from app.infrastructure.models.user_model import User as UserModel


class UserById(UserSpecificationPort):
    def __init__(self, user_id: UUID):
        self.user_id = user_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(UserModel.id == self.user_id)

# app/infrastructure/specs/user/user_by_id.py

from typing import Any
from uuid import UUID

from app.domain.ports.repositories.user import UserSpecificationPort
from app.infrastructure.models.user import User as UserModel


class UserById(UserSpecificationPort):
    def __init__(self, user_id: UUID):
        self.user_id = user_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(UserModel.id == self.user_id)

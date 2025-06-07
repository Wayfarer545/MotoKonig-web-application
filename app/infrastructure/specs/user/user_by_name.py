# app/infrastructure/specs/user/user_by_name.py

from typing import Any

from app.domain.ports.repositories.user import UserSpecificationPort
from app.infrastructure.models.user import User as UserModel


class UserByName(UserSpecificationPort):
    def __init__(self, username: str):
        self.username = username.lower()

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(UserModel.username == self.username)

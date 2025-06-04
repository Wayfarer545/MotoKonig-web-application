# app/adapters/specifications/user_by_name.py

from typing import Any

from app.domain.ports.user_repository import UserSpecificationPort
from app.infrastructure.models.user_model import User as UserModel


class UserByName(UserSpecificationPort):
    def __init__(self, username: str):
        self.username = username.lower()

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(UserModel.username == self.username)

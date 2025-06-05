from __future__ import annotations

from uuid import UUID

from app.adapters.specifications.user_specs.user_by_id import UserById
from app.adapters.specifications.user_specs.user_by_name import UserByName
from app.domain.entities.user import User
from app.domain.ports.user_repository import IUserRepository
from app.domain.ports.user_specification import UserSpecificationPort


class FakeUserRepository(IUserRepository):
    def __init__(self):
        self.store: dict[UUID, User] = {}

    async def add(self, user: User) -> User:
        self.store[user.id] = user
        return user

    async def get(self, spec: UserSpecificationPort) -> User | None:
        if isinstance(spec, UserByName):
            for u in self.store.values():
                if u.username == spec.username:
                    return u
        if isinstance(spec, UserById):
            return self.store.get(spec.user_id)
        return None

    async def get_list(self) -> list[User]:
        return list(self.store.values())

    async def update(self, user: User) -> User:
        self.store[user.id] = user
        return user

    async def delete(self, user_id: UUID) -> bool:
        return self.store.pop(user_id, None) is not None

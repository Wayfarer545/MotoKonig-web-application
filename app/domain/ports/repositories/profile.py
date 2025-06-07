# app/domain/ports/profile.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.profile import Profile
from app.domain.ports.specs.profile import ProfileSpecificationPort


class IProfileRepository(Protocol):
    """Порт репозитория профилей"""

    async def add(self, profile: Profile) -> Profile:
        """Добавить новый профиль"""
        ...

    async def get(self, spec: ProfileSpecificationPort) -> Profile | None:
        """Получить профиль по спецификации"""
        ...

    async def get_list(self, spec: ProfileSpecificationPort | None = None) -> list[Profile]:
        """Получить список профилей по спецификации"""
        ...

    async def update(self, profile: Profile) -> Profile:
        """Обновить профиль"""
        ...

    async def delete(self, profile_id: UUID) -> bool:
        """Удалить профиль"""
        ...

# app/domain/ports/club_membership.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.club_membership import ClubMembership
from app.domain.ports.specs.club_membership import (
    ClubMembershipSpecificationPort,
)


class IClubMembershipRepository(Protocol):
    """Порт репозитория членства в мотоклубах"""

    async def add(self, membership: ClubMembership) -> ClubMembership:
        """Добавить новое членство"""
        ...

    async def get(self, spec: ClubMembershipSpecificationPort) -> ClubMembership | None:
        """Получить членство по спецификации"""
        ...

    async def get_list(self, spec: ClubMembershipSpecificationPort | None = None) -> list[ClubMembership]:
        """Получить список членств по спецификации"""
        ...

    async def update(self, membership: ClubMembership) -> ClubMembership:
        """Обновить членство"""
        ...

    async def delete(self, membership_id: UUID) -> bool:
        """Удалить членство"""
        ...

    async def get_user_membership_in_club(self, user_id: UUID, club_id: UUID) -> ClubMembership | None:
        """Получить членство пользователя в конкретном клубе"""
        ...

    async def count_club_members(self, club_id: UUID, active_only: bool = True) -> int:
        """Подсчитать количество участников клуба"""
        ...

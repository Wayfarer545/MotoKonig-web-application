# app/domain/ports/club_invitation_repository.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.club_invitation import ClubInvitation
from app.domain.ports.specs.club_invitation import (
    ClubInvitationSpecificationPort,
)


class IClubInvitationRepository(Protocol):
    """Порт репозитория приглашений в мотоклубы"""

    async def add(self, invitation: ClubInvitation) -> ClubInvitation:
        """Добавить новое приглашение"""
        ...

    async def get(self, spec: ClubInvitationSpecificationPort) -> ClubInvitation | None:
        """Получить приглашение по спецификации"""
        ...

    async def get_list(self, spec: ClubInvitationSpecificationPort | None = None) -> list[ClubInvitation]:
        """Получить список приглашений по спецификации"""
        ...

    async def update(self, invitation: ClubInvitation) -> ClubInvitation:
        """Обновить приглашение"""
        ...

    async def delete(self, invitation_id: UUID) -> bool:
        """Удалить приглашение"""
        ...

    async def get_pending_invitation(self, club_id: UUID, invitee_id: UUID) -> ClubInvitation | None:
        """Получить активное приглашение для пользователя в клуб"""
        ...

    async def expire_old_invitations(self) -> int:
        """Сделать просроченными старые приглашения"""
        ...

# app/domain/entities/club_invitation.py

from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.value_objects.club_role import ClubRole

if TYPE_CHECKING:
    pass


class ClubInvitation:
    """
    Доменная сущность приглашения в мотоклуб

    Инварианты:
    - Приглашение должно иметь срок действия
    - Нельзя приглашать уже существующих участников
    - Приглашение может быть принято/отклонено только один раз
    """

    def __init__(
            self,
            *,
            invitation_id: UUID | None = None,
            club_id: UUID,
            inviter_id: UUID,
            invitee_id: UUID,
            invited_role: ClubRole = ClubRole.MEMBER,
            status: str = "pending",  # pending, accepted, declined, expired
            message: str | None = None,
            expires_at: datetime | None = None,
            responded_at: datetime | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        # Валидация инвариантов
        self._validate_status(status)
        if message is not None:
            self._validate_message(message)

        self.id: UUID = invitation_id or uuid4()
        self.club_id: UUID = club_id
        self.inviter_id: UUID = inviter_id
        self.invitee_id: UUID = invitee_id
        self.invited_role: ClubRole = invited_role
        self.status: str = status
        self.message: str | None = message.strip() if message else None
        self.expires_at: datetime = expires_at or (datetime.utcnow() + timedelta(days=7))
        self.responded_at: datetime | None = responded_at
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def _validate_status(self, status: str) -> None:
        """Валидация статуса приглашения"""
        allowed_statuses = ["pending", "accepted", "declined", "expired"]
        if status not in allowed_statuses:
            raise ValueError(f"Invalid status. Allowed: {', '.join(allowed_statuses)}")

    def _validate_message(self, message: str) -> None:
        """Валидация сообщения приглашения"""
        if len(message.strip()) > 500:
            raise ValueError("Invitation message cannot be longer than 500 characters")

    def accept(self) -> None:
        """Принять приглашение"""
        if self.status != "pending":
            raise ValueError("Can only accept pending invitations")

        if self.is_expired():
            raise ValueError("Cannot accept expired invitation")

        self.status = "accepted"
        self.responded_at = datetime.utcnow()

    def decline(self) -> None:
        """Отклонить приглашение"""
        if self.status != "pending":
            raise ValueError("Can only decline pending invitations")

        self.status = "declined"
        self.responded_at = datetime.utcnow()

    def expire(self) -> None:
        """Сделать приглашение просроченным"""
        if self.status == "pending":
            self.status = "expired"
            self.responded_at = datetime.utcnow()

    def is_expired(self) -> bool:
        """Проверить, просрочено ли приглашение"""
        return datetime.utcnow() > self.expires_at

    def is_pending(self) -> bool:
        """Проверить, ожидает ли приглашение ответа"""
        return self.status == "pending" and not self.is_expired()

    def extend_expiry(self, days: int = 7) -> None:
        """Продлить срок действия приглашения"""
        if self.status != "pending":
            raise ValueError("Can only extend pending invitations")

        self.expires_at = datetime.utcnow() + timedelta(days=days)

    def update_message(self, message: str | None) -> None:
        """Обновить сообщение приглашения"""
        if message is not None:
            self._validate_message(message)
        self.message = message.strip() if message else None

    def to_dto(self) -> dict:
        """Конвертировать в DTO для API"""
        return {
            "id": self.id,
            "club_id": self.club_id,
            "inviter_id": self.inviter_id,
            "invitee_id": self.invitee_id,
            "invited_role": self.invited_role.value,
            "status": self.status,
            "message": self.message,
            "expires_at": self.expires_at,
            "responded_at": self.responded_at,
            "is_expired": self.is_expired(),
            "is_pending": self.is_pending(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

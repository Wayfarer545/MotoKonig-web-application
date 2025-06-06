# app/domain/entities/club_membership.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.value_objects.club_role import ClubRole

if TYPE_CHECKING:
    pass


class ClubMembership:
    """
    Доменная сущность членства в мотоклубе

    Инварианты:
    - Пользователь может быть участником клуба только один раз
    - Роль должна быть валидной
    - Статус должен быть валидным
    """

    def __init__(
            self,
            *,
            membership_id: UUID | None = None,
            club_id: UUID,
            user_id: UUID,
            role: ClubRole = ClubRole.MEMBER,
            status: str = "active",  # active, suspended, banned
            joined_at: datetime | None = None,
            invited_by: UUID | None = None,
            notes: str | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        # Валидация инвариантов
        self._validate_status(status)
        if notes is not None:
            self._validate_notes(notes)

        self.id: UUID = membership_id or uuid4()
        self.club_id: UUID = club_id
        self.user_id: UUID = user_id
        self.role: ClubRole = role
        self.status: str = status
        self.joined_at: datetime = joined_at or datetime.utcnow()
        self.invited_by: UUID | None = invited_by
        self.notes: str | None = notes.strip() if notes else None
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def _validate_status(self, status: str) -> None:
        """Валидация статуса участника"""
        allowed_statuses = ["active", "suspended", "banned"]
        if status not in allowed_statuses:
            raise ValueError(f"Invalid status. Allowed: {', '.join(allowed_statuses)}")

    def _validate_notes(self, notes: str) -> None:
        """Валидация заметок"""
        if len(notes.strip()) > 500:
            raise ValueError("Notes cannot be longer than 500 characters")

    def promote_to_role(self, new_role: ClubRole) -> None:
        """Повысить участника до новой роли"""
        if new_role.value < self.role.value:  # Чем меньше значение, тем выше роль
            self.role = new_role
        else:
            raise ValueError("Cannot promote to lower or same role")

    def demote_to_role(self, new_role: ClubRole) -> None:
        """Понизить участника до новой роли"""
        if new_role.value > self.role.value:  # Чем больше значение, тем ниже роль
            self.role = new_role
        else:
            raise ValueError("Cannot demote to higher or same role")

    def suspend(self, reason: str | None = None) -> None:
        """Временно отстранить участника"""
        self.status = "suspended"
        if reason:
            self.notes = reason

    def ban(self, reason: str | None = None) -> None:
        """Заблокировать участника"""
        self.status = "banned"
        if reason:
            self.notes = reason

    def reinstate(self) -> None:
        """Восстановить участника"""
        self.status = "active"

    def update_notes(self, notes: str | None) -> None:
        """Обновить заметки"""
        if notes is not None:
            self._validate_notes(notes)
        self.notes = notes.strip() if notes else None

    def is_active(self) -> bool:
        """Проверить, активен ли участник"""
        return self.status == "active"

    def can_manage_members(self) -> bool:
        """Может ли участник управлять другими участниками"""
        return self.role in [ClubRole.PRESIDENT, ClubRole.VICE_PRESIDENT, ClubRole.SECRETARY]

    def can_create_events(self) -> bool:
        """Может ли участник создавать события"""
        return self.role in [ClubRole.PRESIDENT, ClubRole.VICE_PRESIDENT, ClubRole.EVENT_ORGANIZER]

    def can_moderate(self) -> bool:
        """Может ли участник модерировать"""
        return self.role in [ClubRole.PRESIDENT, ClubRole.VICE_PRESIDENT, ClubRole.MODERATOR]

    def to_dto(self) -> dict:
        """Конвертировать в DTO для API"""
        return {
            "id": self.id,
            "club_id": self.club_id,
            "user_id": self.user_id,
            "role": self.role.value,
            "status": self.status,
            "joined_at": self.joined_at,
            "invited_by": self.invited_by,
            "notes": self.notes,
            "permissions": {
                "can_manage_members": self.can_manage_members(),
                "can_create_events": self.can_create_events(),
                "can_moderate": self.can_moderate(),
            },
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

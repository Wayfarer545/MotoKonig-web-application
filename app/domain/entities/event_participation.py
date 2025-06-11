# app/domain/entities/event_participation.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    pass


class EventParticipation:
    """Доменная сущность участия пользователя в мероприятии"""

    def __init__(
            self,
            *,
            participation_id: UUID | None = None,
            event_id: UUID,
            user_id: UUID,
            joined_at: datetime | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ) -> None:
        self.id: UUID = participation_id or uuid4()
        self.event_id: UUID = event_id
        self.user_id: UUID = user_id
        self.joined_at: datetime = joined_at or datetime.utcnow()
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def to_dto(self) -> dict:
        return {
            "id": self.id,
            "event_id": self.event_id,
            "user_id": self.user_id,
            "joined_at": self.joined_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

# app/domain/ports/repositories/event_participation.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.event_participation import EventParticipation


class IEventParticipationRepository(Protocol):
    """Порт репозитория участий в мероприятиях"""

    async def add(self, participation: EventParticipation) -> EventParticipation:
        """Добавить участие"""
        ...

    async def get(self, event_id: UUID, user_id: UUID) -> EventParticipation | None:
        """Получить участие пользователя в мероприятии"""
        ...

    async def list_for_event(self, event_id: UUID) -> list[EventParticipation]:
        """Получить список участников события"""
        ...

    async def delete(self, event_id: UUID, user_id: UUID) -> bool:
        """Удалить участие"""
        ...

    async def count_for_event(self, event_id: UUID) -> int:
        """Подсчитать количество участников"""
        ...
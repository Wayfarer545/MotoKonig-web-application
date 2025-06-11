# app/domain/ports/repositories/event.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.event import Event
from app.domain.ports.specs.event import EventSpecificationPort


class IEventRepository(Protocol):
    """Порт репозитория мероприятий"""

    async def add(self, event: Event) -> Event:
        """Добавить новое мероприятие"""
        ...

    async def get(self, spec: EventSpecificationPort) -> Event | None:
        """Получить мероприятие по спецификации"""
        ...

    async def get_list(self, spec: EventSpecificationPort | None = None) -> list[Event]:
        """Получить список мероприятий по спецификации"""
        ...

    async def update(self, event: Event) -> Event:
        """Обновить мероприятие"""
        ...

    async def delete(self, event_id: UUID) -> bool:
        """Удалить мероприятие"""
        ...

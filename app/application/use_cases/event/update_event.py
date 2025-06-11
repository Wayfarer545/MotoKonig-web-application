# app/application/use_cases/event/update_event.py
from uuid import UUID

from app.domain.entities.event import Event
from app.domain.ports.repositories.event import IEventRepository
from app.domain.value_objects.event_type import EventType
from app.domain.value_objects.location import Location
from app.infrastructure.specs.event.event_by_id import EventById


class UpdateEventUseCase:
    """Use case для обновления мероприятия"""

    def __init__(self, repo: IEventRepository):
        self.repo = repo

    async def execute(
            self,
            event_id: UUID,
            title: str | None = None,
            description: str | None = None,
            location: Location | None = None,
            start_time=None,
            end_time=None,
            event_type: EventType | None = None,
            max_participants: int | None = None,
            photo_urls: list[str] | None = None,
    ) -> Event | None:
        existing = await self.repo.get(EventById(event_id))
        if not existing:
            return None
        if title is not None:
            existing.update_title(title)
        if description is not None:
            existing.update_description(description)
        if location is not None:
            existing.update_location(location)
        if start_time is not None or end_time is not None:
            existing.update_time(start_time or existing.start_time, end_time)
        if event_type is not None:
            existing.event_type = event_type
        if max_participants is not None:
            existing.set_max_participants(max_participants)
        if photo_urls is not None:
            existing.photo_urls = photo_urls
        return await self.repo.update(existing)
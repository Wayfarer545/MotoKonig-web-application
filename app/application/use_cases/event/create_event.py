# app/application/use_cases/event/create_event.py
from uuid import UUID

from app.domain.entities.event import Event
from app.domain.ports.repositories.event import IEventRepository
from app.domain.value_objects.event_type import EventType
from app.domain.value_objects.location import Location


class CreateEventUseCase:
    """Use case для создания мероприятия"""

    def __init__(self, repo: IEventRepository):
        self.repo = repo

    async def execute(
            self,
            organizer_id: UUID,
            title: str,
            description: str,
            location: Location,
            start_time,
            end_time=None,
            event_type: EventType = EventType.PRIVATE,
            max_participants: int | None = None,
            photo_urls: list[str] | None = None,
    ) -> Event:
        event = Event(
            organizer_id=organizer_id,
            title=title,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
            event_type=event_type,
            max_participants=max_participants,
            photo_urls=photo_urls or [],
        )
        return await self.repo.add(event)
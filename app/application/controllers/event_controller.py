# app/application/controllers/event_controller.py
from uuid import UUID

from app.application.exceptions import BadRequestError, NotFoundError
from app.application.use_cases.event.create_event import CreateEventUseCase
from app.application.use_cases.event.delete_event import DeleteEventUseCase
from app.application.use_cases.event.get_event import GetEventUseCase
from app.application.use_cases.event.list_events import ListEventsUseCase
from app.application.use_cases.event.update_event import UpdateEventUseCase
from app.domain.value_objects.event_type import EventType
from app.domain.value_objects.location import Location
from app.infrastructure.specs.event.event_by_id import EventById
from app.infrastructure.specs.event.event_filter import EventFilter


class EventController:
    """Контроллер для управления мероприятиями"""

    def __init__(
            self,
            create_uc: CreateEventUseCase,
            get_uc: GetEventUseCase,
            list_uc: ListEventsUseCase,
            update_uc: UpdateEventUseCase,
            delete_uc: DeleteEventUseCase,
    ):
        self.create_uc = create_uc
        self.get_uc = get_uc
        self.list_uc = list_uc
        self.update_uc = update_uc
        self.delete_uc = delete_uc

    async def create_event(
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
    ) -> dict:
        try:
            event = await self.create_uc.execute(
                organizer_id=organizer_id,
                title=title,
                description=description,
                location=location,
                start_time=start_time,
                end_time=end_time,
                event_type=event_type,
                max_participants=max_participants,
                photo_urls=photo_urls,
            )
            return event.to_dto()
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def get_event_by_id(self, event_id: UUID) -> dict:
        spec = EventById(event_id)
        event = await self.get_uc.execute(spec)
        if not event:
            raise NotFoundError("Event not found")
        return event.to_dto()

    async def list_events(
            self,
            organizer_id: UUID | None = None,
            event_type: EventType | None = None,
            start_from=None,
            start_to=None,
            location_query: str | None = None,
    ) -> list[dict]:
        spec = EventFilter(
            organizer_id=organizer_id,
            event_type=event_type,
            start_from=start_from,
            start_to=start_to,
            location_query=location_query,
        )
        events = await self.list_uc.execute(spec)
        return [e.to_dto() for e in events]

    async def update_event(
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
    ) -> dict:
        try:
            updated = await self.update_uc.execute(
                event_id=event_id,
                title=title,
                description=description,
                location=location,
                start_time=start_time,
                end_time=end_time,
                event_type=event_type,
                max_participants=max_participants,
                photo_urls=photo_urls,
            )
            if not updated:
                raise NotFoundError("Event not found")
            return updated.to_dto()
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def delete_event(self, event_id: UUID) -> None:
        success = await self.delete_uc.execute(event_id)
        if not success:
            raise NotFoundError("Event not found")
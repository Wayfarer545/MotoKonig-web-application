# app/infrastructure/repositories/sql_event_repo.py
import json
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.event import Event
from app.domain.ports.repositories.event import IEventRepository
from app.domain.ports.specs.event import EventSpecificationPort
from app.domain.value_objects.event_type import EventType
from app.domain.value_objects.location import Location
from app.infrastructure.models.event import Event as EventModel


class SqlEventRepository(IEventRepository):
    """SQLAlchemy реализация репозитория мероприятий"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, event: Event) -> Event:
        db_event = EventModel(
            organizer_id=event.organizer_id,
            title=event.title,
            description=event.description,
            latitude=event.location.latitude,
            longitude=event.location.longitude,
            address=event.location.address,
            start_time=event.start_time,
            end_time=event.end_time,
            event_type=event.event_type,
            max_participants=event.max_participants,
            photo_urls=json.dumps(event.photo_urls) if event.photo_urls else None,
        )

        self.session.add(db_event)
        await self.session.flush()
        await self.session.refresh(db_event)

        event.id = db_event.id
        event.created_at = db_event.created_at
        event.updated_at = db_event.updated_at
        return event

    async def get(self, spec: EventSpecificationPort) -> Event | None:
        statement = spec.to_query(select(EventModel))
        result = await self.session.execute(statement)
        db_event = result.scalar_one_or_none()
        if db_event:
            return self._to_domain_entity(db_event)
        return None

    async def get_list(self, spec: EventSpecificationPort | None = None) -> list[Event]:
        statement = select(EventModel)
        if spec:
            statement = spec.to_query(statement)
        result = await self.session.execute(statement)
        events = result.scalars().all()
        return [self._to_domain_entity(e) for e in events]

    async def update(self, event: Event) -> Event:
        db_event = await self.session.get(EventModel, event.id)
        if db_event:
            db_event.title = event.title
            db_event.description = event.description
            db_event.latitude = event.location.latitude
            db_event.longitude = event.location.longitude
            db_event.address = event.location.address
            db_event.start_time = event.start_time
            db_event.end_time = event.end_time
            db_event.event_type = event.event_type
            db_event.max_participants = event.max_participants
            db_event.photo_urls = json.dumps(event.photo_urls) if event.photo_urls else None

            await self.session.flush()
            await self.session.refresh(db_event)
            event.updated_at = db_event.updated_at
        return event

    async def delete(self, event_id: UUID) -> bool:
        db_event = await self.session.get(EventModel, event_id)
        if db_event:
            await self.session.delete(db_event)
            await self.session.flush()
            return True
        return False

    def _to_domain_entity(self, db_event: EventModel) -> Event:
        photos = []
        if db_event.photo_urls:
            try:
                photos = json.loads(db_event.photo_urls)
            except (json.JSONDecodeError, TypeError):
                photos = []
        return Event(
            event_id=db_event.id,
            organizer_id=db_event.organizer_id,
            title=db_event.title,
            description=db_event.description,
            location=Location(
                latitude=db_event.latitude,
                longitude=db_event.longitude,
                address=db_event.address,
            ),
            start_time=db_event.start_time,
            end_time=db_event.end_time,
            event_type=EventType(db_event.event_type.value),
            max_participants=db_event.max_participants,
            photo_urls=photos,
            created_at=db_event.created_at,
            updated_at=db_event.updated_at,
        )

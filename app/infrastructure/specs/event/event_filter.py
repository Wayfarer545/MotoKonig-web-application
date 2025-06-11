# app/infrastructure/specs/event/event_filter.py
from datetime import datetime
from typing import Any
from uuid import UUID

from app.domain.ports.specs.event import EventSpecificationPort
from app.domain.value_objects.event_type import EventType
from app.infrastructure.models.event import Event as EventModel


class EventFilter(EventSpecificationPort):
    """Фильтр для поиска мероприятий"""

    def __init__(
            self,
            *,
            organizer_id: UUID | None = None,
            event_type: EventType | None = None,
            start_from: datetime | None = None,
            start_to: datetime | None = None,
            location_query: str | None = None,
    ):
        self.organizer_id = organizer_id
        self.event_type = event_type
        self.start_from = start_from
        self.start_to = start_to
        self.location_query = location_query.strip() if location_query else None

    def to_query(self, base_query: Any) -> Any:
        query = base_query
        if self.organizer_id:
            query = query.where(EventModel.organizer_id == self.organizer_id)
        if self.event_type:
            query = query.where(EventModel.event_type == self.event_type)
        if self.start_from:
            query = query.where(EventModel.start_time >= self.start_from)
        if self.start_to:
            query = query.where(EventModel.start_time <= self.start_to)
        if self.location_query:
            like = f"%{self.location_query}%"
            query = query.where(EventModel.address.ilike(like))
        query = query.order_by(EventModel.start_time.asc())
        return query

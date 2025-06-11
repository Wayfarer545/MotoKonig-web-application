# app/infrastructure/specs/event/event_by_id.py
from typing import Any
from uuid import UUID

from app.domain.ports.specs.event import EventSpecificationPort
from app.infrastructure.models.event import Event as EventModel


class EventById(EventSpecificationPort):
    """Спецификация поиска события по ID"""

    def __init__(self, event_id: UUID):
        self.event_id = event_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(EventModel.id == self.event_id)
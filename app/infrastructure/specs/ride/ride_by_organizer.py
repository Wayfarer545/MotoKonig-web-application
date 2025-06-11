# app/infrastructure/specs/ride/ride_by_organizer.py

from typing import Any
from uuid import UUID

from app.domain.ports.specs.ride import RideSpecificationPort
from app.infrastructure.models.ride import Ride as RideModel


class RideByOrganizerSpec(RideSpecificationPort):
    """Спецификация поиска по организатору"""

    def __init__(self, organizer_id: UUID):
        self.organizer_id = organizer_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(RideModel.organizer_id == self.organizer_id)

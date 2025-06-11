# app/infrastructure/specs/ride/ride_by_organizer.py

from typing import Any
from uuid import UUID

from app.domain.ports.specs.ride import RideSpecificationPort
from app.infrastructure.models.ride import Ride as RideModel


class RideByIdSpec(RideSpecificationPort):
    """Спецификация поиска по ID"""

    def __init__(self, ride_id: UUID):
        self.ride_id = ride_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(RideModel.id == self.ride_id)

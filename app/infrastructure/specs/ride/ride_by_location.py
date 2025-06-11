# app/infrastructure/specs/ride/ride_by_location.py

from typing import Any

from app.domain.ports.specs.ride import RideSpecificationPort
from app.infrastructure.models.ride import Ride as RideModel


class RideByLocationSpec(RideSpecificationPort):
    """Спецификация поиска по локации"""

    def __init__(self, location: str):
        self.location = location

    def to_query(self, base_query: Any) -> Any:
        from sqlalchemy import or_
        return base_query.where(
            or_(
                RideModel.start_location.ilike(f"%{self.location}%"),
                RideModel.end_location.ilike(f"%{self.location}%")
            )
        )

# app/infrastructure/specs/ride/ride_upcoming.py

from datetime import datetime
from typing import Any

from app.domain.ports.specs.ride import RideSpecificationPort
from app.infrastructure.models.ride import Ride as RideModel


class RideUpcomingSpec(RideSpecificationPort):
    """Спецификация для получения предстоящих поездок"""

    def to_query(self, base_query: Any) -> Any:
        now = datetime.utcnow()
        return base_query.where(
            (RideModel.planned_start > now) &
            (RideModel.is_completed.is_(False))
        )

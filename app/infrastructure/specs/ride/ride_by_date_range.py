# app/infrastructure/specs/ride/ride_by_date_range.py

from datetime import datetime
from typing import Any

from app.domain.ports.specs.ride import RideSpecificationPort
from app.infrastructure.models.ride import Ride as RideModel


class RideByDateRangeSpec(RideSpecificationPort):
    """Спецификация поиска по диапазону дат"""

    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(
            RideModel.planned_start >= self.start_date,
            RideModel.planned_start <= self.end_date
        )

# app/infrastructure/specs/ride/ride_by_difficulty.py

from typing import Any

from app.domain.ports.specs.ride import RideSpecificationPort
from app.domain.value_objects.ride_difficulty import RideDifficulty
from app.infrastructure.models.ride import Ride as RideModel


class RideByDifficultySpec(RideSpecificationPort):
    """Спецификация поиска по сложности"""

    def __init__(self, difficulty: RideDifficulty):
        self.difficulty = difficulty

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(RideModel.difficulty == self.difficulty)

# app/infrastructure/specs/moto/moto_by_type.py

from typing import Any

from domain.ports.specs.motorcycle import MotorcycleSpecificationPort

from app.domain.value_objects.motorcycle_type import MotorcycleType
from app.infrastructure.models.motorcycle import Motorcycle as MotorcycleModel


class MotorcyclesByType(MotorcycleSpecificationPort):
    """Спецификация для поиска мотоциклов по типу"""

    def __init__(self, motorcycle_type: MotorcycleType, active_only: bool = True):
        self.motorcycle_type = motorcycle_type
        self.active_only = active_only

    def to_query(self, base_query: Any) -> Any:
        query = base_query.where(MotorcycleModel.motorcycle_type == self.motorcycle_type)
        if self.active_only:
            query = query.where(MotorcycleModel.is_active)
        return query

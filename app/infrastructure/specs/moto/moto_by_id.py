# app/infrastructure/specs/moto/moto_by_id.py

from typing import Any
from uuid import UUID

from app.domain.ports.motorcycle_specification import MotorcycleSpecificationPort
from app.infrastructure.models.motorcycle_model import Motorcycle as MotorcycleModel


class MotorcycleById(MotorcycleSpecificationPort):
    """Спецификация для поиска мотоцикла по ID"""

    def __init__(self, motorcycle_id: UUID):
        self.motorcycle_id = motorcycle_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(MotorcycleModel.id == self.motorcycle_id)

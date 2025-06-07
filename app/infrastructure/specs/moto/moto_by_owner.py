# app/infrastructure/specs/moto/moto_by_owner.py

from typing import Any
from uuid import UUID

from app.domain.ports.specs.motorcycle import MotorcycleSpecificationPort
from app.infrastructure.models.motorcycle_model import Motorcycle as MotorcycleModel


class MotorcyclesByOwner(MotorcycleSpecificationPort):
    """Спецификация для поиска мотоциклов по владельцу"""

    def __init__(self, owner_id: UUID, active_only: bool = True):
        self.owner_id = owner_id
        self.active_only = active_only

    def to_query(self, base_query: Any) -> Any:
        query = base_query.where(MotorcycleModel.owner_id == self.owner_id)
        if self.active_only:
            query = query.where(MotorcycleModel.is_active)
        return query

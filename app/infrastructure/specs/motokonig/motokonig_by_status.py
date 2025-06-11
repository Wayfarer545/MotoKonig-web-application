# app/infrastructure/specs/motokonig/motokonig_by_status.py

from typing import Any

from app.domain.ports.specs.motokonig import MotoKonigSpecificationPort
from app.domain.value_objects.motokonig_status import MotoKonigStatus
from app.infrastructure.models.motokonig import MotoKonig as MotoKonigModel


class MotoKonigByStatus(MotoKonigSpecificationPort):
    """Спецификация поиска по статусу"""

    def __init__(self, status: MotoKonigStatus):
        self.status = status

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(MotoKonigModel.status == self.status)

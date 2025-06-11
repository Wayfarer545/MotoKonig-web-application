# app/infrastructure/specs/motokonig/motokonig_by_user_id.py

from typing import Any
from uuid import UUID

from app.domain.ports.specs.motokonig import MotoKonigSpecificationPort
from app.infrastructure.models.motokonig import MotoKonig as MotoKonigModel


class MotoKonigByUserId(MotoKonigSpecificationPort):
    """Спецификация поиска по ID пользователя"""

    def __init__(self, user_id: UUID):
        self.user_id = user_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(MotoKonigModel.user_id == self.user_id)

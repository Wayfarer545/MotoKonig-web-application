# app/infrastructure/specs/moto_club/club_by_id.py

from typing import Any
from uuid import UUID

from app.domain.ports.specs.moto_club import MotoClubSpecificationPort
from app.infrastructure.models.moto_club_model import MotoClub as MotoClubModel


class MotoClubById(MotoClubSpecificationPort):
    """Спецификация для поиска мотоклуба по ID"""

    def __init__(self, club_id: UUID):
        self.club_id = club_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(MotoClubModel.id == self.club_id)

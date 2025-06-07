# app/infrastructure/specs/moto_club/club_filter.py

from typing import Any
from uuid import UUID

from app.domain.ports.specs.moto_club import MotoClubSpecificationPort
from app.infrastructure.models.motoclub import MotoClub as MotoClubModel


class MotoClubFilter(MotoClubSpecificationPort):
    """Спецификация для фильтрации мотоклубов"""

    def __init__(
            self,
            *,
            name: str | None = None,
            location: str | None = None,
            president_id: UUID | None = None,
            is_public: bool | None = None,
            is_active: bool | None = None,
            has_max_members: bool | None = None,
    ):
        self.name = name.strip() if name else None
        self.location = location.strip() if location else None
        self.president_id = president_id
        self.is_public = is_public
        self.is_active = is_active
        self.has_max_members = has_max_members

    def to_query(self, base_query: Any) -> Any:
        query = base_query

        if self.is_active is not None:
            query = query.where(MotoClubModel.is_active == self.is_active)

        if self.is_public is not None:
            query = query.where(MotoClubModel.is_public == self.is_public)

        if self.name:
            query = query.where(MotoClubModel.name.ilike(f"%{self.name}%"))

        if self.location:
            query = query.where(MotoClubModel.location.ilike(f"%{self.location}%"))

        if self.president_id:
            query = query.where(MotoClubModel.president_id == self.president_id)

        if self.has_max_members is not None:
            if self.has_max_members:
                query = query.where(MotoClubModel.max_members.is_not(None))
            else:
                query = query.where(MotoClubModel.max_members.is_(None))

        return query

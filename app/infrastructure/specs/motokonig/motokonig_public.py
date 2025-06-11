# app/infrastructure/specs/motokonig/motokonig_public.py

from typing import Any

from app.domain.ports.specs.motokonig import MotoKonigSpecificationPort
from app.infrastructure.models.motokonig import MotoKonig as MotoKonigModel


class MotoKonigPublic(MotoKonigSpecificationPort):
    """Спецификация для публичных профилей"""

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(MotoKonigModel.is_public == True)  # noqa: E712

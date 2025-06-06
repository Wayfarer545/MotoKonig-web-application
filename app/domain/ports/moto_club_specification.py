# app/domain/ports/moto_club_specification.py

from typing import Any, Protocol


class MotoClubSpecificationPort(Protocol):
    """Порт для спецификаций поиска мотоклубов"""

    def to_query(self, base_query: Any) -> Any:
        """Преобразовать спецификацию в SQL запрос"""
        ...

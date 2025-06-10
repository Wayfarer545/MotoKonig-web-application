# app/domain/ports/specs/listing.py

from typing import Any, Protocol


class ListingSpecificationPort(Protocol):
    """Порт для спецификаций поиска объявлений"""

    def to_query(self, base_query: Any) -> Any:
        """Преобразовать спецификацию в SQL запрос"""
        ...

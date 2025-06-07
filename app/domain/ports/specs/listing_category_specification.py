# app/domain/ports/specs/listing_category_specification.py

from typing import Any, Protocol


class ListingCategorySpecificationPort(Protocol):
    """Порт для спецификаций поиска категорий объявлений"""

    def to_query(self, base_query: Any) -> Any:
        """Преобразовать спецификацию в SQL запрос"""
        ...
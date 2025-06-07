# app/domain/ports/listing.py

from typing import Any, Protocol


class ListingSpecificationPort(Protocol):
    """Порт для спецификаций поиска объявлений"""

    def to_query(self, base_query: Any) -> Any:
        """Преобразовать спецификацию в SQL запрос"""
        ...


# app/domain/ports/listing_category_specification.py

from typing import Any, Protocol


class ListingCategorySpecificationPort(Protocol):
    """Порт для спецификаций поиска категорий"""

    def to_query(self, base_query: Any) -> Any:
        """Преобразовать спецификацию в SQL запрос"""
        ...
# app/domain/ports/listing_image_specification.py

from typing import Any, Protocol


class ListingImageSpecificationPort(Protocol):
    """Порт для спецификаций поиска изображений"""

    def to_query(self, base_query: Any) -> Any:
        """Преобразовать спецификацию в SQL запрос"""
        ...
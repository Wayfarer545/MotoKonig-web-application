# app/domain/ports/motorcycle_specification.py

from typing import Any, Protocol


class MotorcycleSpecificationPort(Protocol):
    """Порт для спецификаций поиска мотоциклов"""

    def to_query(self, base_query: Any) -> Any:
        """Преобразовать спецификацию в SQL запрос"""
        ...

# app/domain/ports/profile.py

from typing import Any, Protocol


class ProfileSpecificationPort(Protocol):
    """Порт для спецификаций поиска профилей"""

    def to_query(self, base_query: Any) -> Any:
        """Преобразовать спецификацию в SQL запрос"""
        ...

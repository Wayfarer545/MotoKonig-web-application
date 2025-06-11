# app/domain/ports/specs/event.py
from typing import Any, Protocol


class EventSpecificationPort(Protocol):
    """Порт для спецификаций поиска мероприятий"""

    def to_query(self, base_query: Any) -> Any:
        """Преобразовать спецификацию в SQL запрос"""
        ...

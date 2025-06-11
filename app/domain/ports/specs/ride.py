# app/domain/ports/specs/ride.py

from abc import ABC, abstractmethod
from typing import Any

__all__ = ["RideSpecificationPort"]


class RideSpecificationPort(ABC):
    """Базовая спецификация для поездок"""

    @abstractmethod
    def to_query(self, statement: Any) -> Any:
        """Преобразовать спецификацию в запрос"""
        ...

# app/domain/ports/specs/motokonig.py

from abc import ABC, abstractmethod
from typing import Any

__all__ = ["MotoKonigSpecificationPort"]


class MotoKonigSpecificationPort(ABC):
    """Базовая спецификация для MotoKonig"""

    @abstractmethod
    def to_query(self, statement: Any) -> Any:
        """Преобразовать спецификацию в запрос"""
        ...

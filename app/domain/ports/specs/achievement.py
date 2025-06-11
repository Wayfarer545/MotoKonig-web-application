# app/domain/ports/specs/achievement.py

from abc import ABC, abstractmethod
from typing import Any

__all__ = ["AchievementSpecificationPort"]


class AchievementSpecificationPort(ABC):
    """Базовая спецификация для достижений"""

    @abstractmethod
    def to_query(self, statement: Any) -> Any:
        """Преобразовать спецификацию в запрос"""
        ...
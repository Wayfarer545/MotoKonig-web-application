# app/domain/ports/repositories/achievement.py

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.achievement import Achievement
from app.domain.value_objects.achievement_type import AchievementType

__all__ = ["IAchievementRepository"]


class IAchievementRepository(ABC):
    """Порт репозитория для достижений"""

    @abstractmethod
    async def add(self, achievement: Achievement, motokonig_id: UUID) -> Achievement:
        """Добавить новое достижение"""
        ...

    @abstractmethod
    async def get_by_motokonig(self, motokonig_id: UUID) -> list[Achievement]:
        """Получить все достижения профиля"""
        ...

    @abstractmethod
    async def has_achievement(self, motokonig_id: UUID, achievement_type: AchievementType) -> bool:
        """Проверить наличие достижения у профиля"""
        ...

    @abstractmethod
    async def get_achievement_stats(self) -> dict[AchievementType, int]:
        """Получить статистику по достижениям"""
        ...

# app/domain/entities/achievement.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.value_objects.achievement_type import AchievementType

__all__ = ["Achievement"]

if TYPE_CHECKING:
    pass


class Achievement:
    """
    Доменная сущность достижения MotoKonig

    Инварианты:
    - Дата получения не может быть в будущем
    - Описание не может быть пустым, если указано
    """

    def __init__(
            self,
            *,
            achievement_id: UUID | None = None,
            achievement_type: AchievementType,
            earned_at: datetime | None = None,
            description: str | None = None,
            metadata: dict | None = None
    ):
        # Валидация
        now = datetime.utcnow()
        if earned_at and earned_at > now:
            raise ValueError("Achievement cannot be earned in the future")

        if description is not None and not description.strip():
            raise ValueError("Description cannot be empty if provided")

        self.achievement_id = achievement_id or uuid4()
        self.achievement_type = achievement_type
        self.earned_at = earned_at or now
        self.description = description.strip() if description else None
        self.metadata = metadata or {}

    def to_dto(self) -> dict:
        """Преобразовать в DTO"""
        return {
            "achievement_id": self.achievement_id,
            "achievement_type": self.achievement_type,
            "earned_at": self.earned_at,
            "description": self.description,
            "metadata": self.metadata
        }
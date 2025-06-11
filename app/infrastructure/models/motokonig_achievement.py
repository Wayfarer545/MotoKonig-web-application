# app/infrastructure/models/motokonig_achievement.py

from datetime import datetime
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.achievement_type import AchievementType

if TYPE_CHECKING:
    from .motokonig import MotoKonig

__all__ = ["MotoKonigAchievement"]


class MotoKonigAchievement(UUIDAuditBase):
    """Модель достижений MotoKonig"""

    __tablename__ = "motokonig_achievements"

    # Foreign keys
    motokonig_id: Mapped[str] = mapped_column(
        ForeignKey("motokonig_profiles.id"),
        nullable=False,
    )

    # Attributes
    achievement_type: Mapped[AchievementType] = mapped_column(
        String(50),
        nullable=False,
    )
    earned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    achievement_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    motokonig: Mapped["MotoKonig"] = relationship(back_populates="achievements")


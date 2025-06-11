# app/infrastructure/models/motokonig.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.motokonig_status import MotoKonigStatus

if TYPE_CHECKING:
    from .motokonig_achievement import MotoKonigAchievement
    from .ride import Ride
    from .ride_participant import RideParticipant
    from .user import User

__all__ = ["MotoKonig"]


class MotoKonig(UUIDAuditBase):
    """Модель профиля MotoKonig"""

    __tablename__ = "motokonig_profiles"

    # Foreign keys
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    # Attributes
    nickname: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    status: Mapped[MotoKonigStatus] = mapped_column(
        String(20),
        default=MotoKonigStatus.NOVICE,
        nullable=False,
    )
    experience_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_distance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_rides: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_speed: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_speed: Mapped[float | None] = mapped_column(Float, nullable=True)
    rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="motokonig_profile")
    achievements: Mapped[list["MotoKonigAchievement"]] = relationship(
        back_populates="motokonig",
        cascade="all, delete-orphan",
    )
    organized_rides: Mapped[list["Ride"]] = relationship(
        back_populates="organizer",
        foreign_keys="Ride.organizer_id",
    )
    ride_participations: Mapped[list["RideParticipant"]] = relationship(
        back_populates="motokonig",
    )

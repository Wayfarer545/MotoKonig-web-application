# app/infrastructure/models/ride.py

from datetime import datetime
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.ride_difficulty import RideDifficulty

if TYPE_CHECKING:
    from .motokonig import MotoKonig
    from .ride_checkpoint import RideCheckpoint
    from .ride_participant import RideParticipant

__all__ = ["Ride"]


class Ride(UUIDAuditBase):
    """Модель поездки"""

    __tablename__ = "rides"

    # Foreign keys
    organizer_id: Mapped[str] = mapped_column(
        ForeignKey("motokonig_profiles.id"),
        nullable=False,
    )

    # Attributes
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[RideDifficulty] = mapped_column(Integer, nullable=False)
    planned_distance: Mapped[int] = mapped_column(Integer, nullable=False)
    max_participants: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    start_location: Mapped[str] = mapped_column(String(200), nullable=False)
    end_location: Mapped[str] = mapped_column(String(200), nullable=False)
    planned_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    planned_duration: Mapped[int] = mapped_column(Integer, nullable=False)  # минуты

    # Actual data
    actual_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_distance: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Additional info
    route_gpx: Mapped[str | None] = mapped_column(Text, nullable=True)
    weather_conditions: Mapped[str | None] = mapped_column(String(200), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Relationships
    organizer: Mapped["MotoKonig"] = relationship(
        back_populates="organized_rides",
        foreign_keys=[organizer_id],
    )
    participants: Mapped[list["RideParticipant"]] = relationship(
        back_populates="ride",
        cascade="all, delete-orphan",
    )
    checkpoints: Mapped[list["RideCheckpoint"]] = relationship(
        back_populates="ride",
        cascade="all, delete-orphan",
    )

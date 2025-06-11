# app/infrastructure/models/ride_participant.py

from datetime import datetime
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .motokonig import MotoKonig
    from .ride import Ride

__all__ = ["RideParticipant"]


class RideParticipant(UUIDAuditBase):
    """Модель участника поездки"""

    __tablename__ = "ride_participants"

    # Foreign keys
    ride_id: Mapped[str] = mapped_column(
        ForeignKey("rides.id"),
        nullable=False,
    )
    motokonig_id: Mapped[str] = mapped_column(
        ForeignKey("motokonig_profiles.id"),
        nullable=False,
    )

    # Attributes
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    left_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    distance_covered: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_speed: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_speed: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_leader: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    ride: Mapped["Ride"] = relationship(back_populates="participants")
    motokonig: Mapped["MotoKonig"] = relationship(back_populates="ride_participations")


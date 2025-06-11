# app/infrastructure/models/ride_checkpoint.py

from datetime import datetime
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .ride import Ride

__all__ = ["RideCheckpoint"]


class RideCheckpoint(UUIDAuditBase):
    """Модель контрольной точки поездки"""

    __tablename__ = "ride_checkpoints"

    # Foreign keys
    ride_id: Mapped[str] = mapped_column(
        ForeignKey("rides.id"),
        nullable=False,
    )

    # Attributes
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    reached_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    ride: Mapped["Ride"] = relationship(back_populates="checkpoints")

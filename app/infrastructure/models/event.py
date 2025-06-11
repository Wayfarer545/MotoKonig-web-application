# app/infrastructure/models/event.py
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.event_type import EventType

__all__ = ["Event"]

if TYPE_CHECKING:
    from .event_participation import EventParticipation
    from .user import User


class Event(UUIDAuditBase):
    """SQLAlchemy модель мероприятия"""

    __tablename__ = "events"

    organizer_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    organizer: Mapped["User"] = relationship("User", lazy="selectin")

    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    address: Mapped[str | None] = mapped_column(String(200), nullable=True)

    start_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    end_time: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)

    event_type: Mapped[EventType] = mapped_column(
        SQLEnum(EventType, name="event_type", native_enum=False),
        default=EventType.PRIVATE,
        nullable=False,
        index=True,
    )
    max_participants: Mapped[int | None] = mapped_column(Integer, nullable=True)
    photo_urls: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON

    participants: Mapped[list["EventParticipation"]] = relationship(
        "EventParticipation",
        back_populates="event",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
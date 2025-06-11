# app/infrastructure/models/event_participation.py
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

__all__ = ["EventParticipation"]

if TYPE_CHECKING:
    from .event import Event
    from .user import User


class EventParticipation(UUIDAuditBase):
    """SQLAlchemy модель участия пользователя в мероприятии"""

    __tablename__ = "event_participations"

    event_id: Mapped[str] = mapped_column(ForeignKey("events.id"), nullable=False, index=True)
    event: Mapped["Event"] = relationship("Event", back_populates="participants")

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    user: Mapped["User"] = relationship("User", lazy="selectin")

    joined_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

# app/infrastructure/models/motoclub.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

__all__ = ["MotoClub"]

if TYPE_CHECKING:
    from .club_invitation import ClubInvitation
    from .club_membership import ClubMembership
    from .user import User


class MotoClub(UUIDAuditBase):
    """SQLAlchemy модель мотоклуба"""

    __tablename__ = "moto_clubs"

    # Основная информация
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Связь с президентом
    president_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    president: Mapped["User"] = relationship("User", lazy="selectin")

    # Настройки клуба
    is_public: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)
    max_members: Mapped[int | None] = mapped_column(Integer, nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Медиа
    avatar_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # Статус
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)

    # Даты
    founded_date: Mapped[str | None] = mapped_column(String(50), nullable=True)  # ISO формат

    # Связи
    memberships: Mapped[list["ClubMembership"]] = relationship(
        "ClubMembership",
        back_populates="club",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    invitations: Mapped[list["ClubInvitation"]] = relationship(
        "ClubInvitation",
        back_populates="club",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

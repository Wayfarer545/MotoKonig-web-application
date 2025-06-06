# app/infrastructure/models/club_invitation_model.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.club_role import ClubRole

__all__ = ["ClubInvitation"]

if TYPE_CHECKING:
    from .moto_club_model import MotoClub
    from .user_model import User


class ClubInvitation(UUIDAuditBase):
    """SQLAlchemy модель приглашения в мотоклуб"""

    __tablename__ = "club_invitations"

    # Связи
    club_id: Mapped[str] = mapped_column(
        ForeignKey("moto_clubs.id"),
        nullable=False,
        index=True
    )
    club: Mapped["MotoClub"] = relationship("MotoClub", back_populates="invitations")

    inviter_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    inviter: Mapped["User"] = relationship("User", foreign_keys=[inviter_id], lazy="selectin")

    invitee_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    invitee: Mapped["User"] = relationship("User", foreign_keys=[invitee_id], lazy="selectin")

    # Информация о приглашении
    invited_role: Mapped[ClubRole] = mapped_column(
        SQLEnum(ClubRole, name="invited_club_role", native_enum=False),
        nullable=False,
        default=ClubRole.MEMBER
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        index=True
    )  # pending, accepted, declined, expired

    message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Временные рамки
    expires_at: Mapped[str] = mapped_column(String(50), nullable=False)  # ISO формат
    responded_at: Mapped[str | None] = mapped_column(String(50), nullable=True)  # ISO формат
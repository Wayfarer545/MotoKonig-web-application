# app/infrastructure/models/club_membership_model.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.club_role import ClubRole

__all__ = ["ClubMembership"]

if TYPE_CHECKING:
    from .moto_club_model import MotoClub
    from .user_model import User


class ClubMembership(UUIDAuditBase):
    """SQLAlchemy модель членства в мотоклубе"""

    __tablename__ = "club_memberships"
    __table_args__ = (
        # Один пользователь может быть участником клуба только один раз
        UniqueConstraint('club_id', 'user_id', name='uq_club_user_membership'),
    )

    # Связи
    club_id: Mapped[str] = mapped_column(
        ForeignKey("moto_clubs.id"),
        nullable=False,
        index=True
    )
    club: Mapped["MotoClub"] = relationship("MotoClub", back_populates="memberships")

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], lazy="selectin")

    # Информация о членстве
    role: Mapped[ClubRole] = mapped_column(
        SQLEnum(ClubRole, name="club_role", native_enum=False),
        nullable=False,
        default=ClubRole.MEMBER,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
        index=True
    )  # active, suspended, banned

    # Дополнительная информация
    joined_at: Mapped[str] = mapped_column(String(50), nullable=False)  # ISO формат
    invited_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )
    inviter: Mapped["User"] = relationship("User", foreign_keys=[invited_by], lazy="selectin")

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

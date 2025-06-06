# app/infrastructure/models/profile_model.py

from datetime import date
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

__all__ = ["Profile"]

from app.domain.value_objects.privacy_level import PrivacyLevel

if TYPE_CHECKING:

    from .social_link_model import SocialLink
    from .user_model import User


class Profile(UUIDAuditBase):
    """SQLAlchemy модель профиля пользователя"""

    __tablename__ = "profiles"

    # Связь с пользователем (One-to-One)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,  # Гарантируем One-to-One
        index=True
    )
    user: Mapped["User"] = relationship("User", back_populates="profile")

    # Основная информация
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    riding_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)  # в годах

    # Аватар и медиа
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Настройки приватности
    privacy_level: Mapped[PrivacyLevel] = mapped_column(
        SQLEnum(PrivacyLevel, name="privacy_level", native_enum=False),
        nullable=False,
        default=PrivacyLevel.PUBLIC
    )
    phone_privacy: Mapped[PrivacyLevel] = mapped_column(
        SQLEnum(PrivacyLevel, name="phone_privacy_level", native_enum=False),
        nullable=False,
        default=PrivacyLevel.FRIENDS_ONLY
    )
    location_privacy: Mapped[PrivacyLevel] = mapped_column(
        SQLEnum(PrivacyLevel, name="location_privacy_level", native_enum=False),
        nullable=False,
        default=PrivacyLevel.PUBLIC
    )

    # Связь с социальными ссылками
    social_links: Mapped[list["SocialLink"]] = relationship(
        "SocialLink",
        back_populates="profile",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

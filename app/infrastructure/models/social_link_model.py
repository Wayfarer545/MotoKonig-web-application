# app/infrastructure/models/social_link_model.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Enum as SQLEnum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.value_objects.privacy_level import PrivacyLevel
from domain.value_objects.social_link import SocialPlatform

__all__ = ["SocialLink"]

if TYPE_CHECKING:
    from .profile_model import Profile


class SocialLink(UUIDAuditBase):
    """SQLAlchemy модель социальной ссылки"""

    __tablename__ = "social_links"
    __table_args__ = (
        # Уникальная комбинация профиль + платформа
        UniqueConstraint('profile_id', 'platform', name='uq_profile_platform'),
    )

    # Связь с профилем
    profile_id: Mapped[str] = mapped_column(
        ForeignKey("profiles.id"),
        nullable=False,
        index=True
    )
    profile: Mapped["Profile"] = relationship("Profile", back_populates="social_links")

    # Информация о ссылке
    platform: Mapped[SocialPlatform] = mapped_column(
        SQLEnum(SocialPlatform, name="social_platform", native_enum=False),
        nullable=False,
        index=True
    )
    url: Mapped[str] = mapped_column(String(500), nullable=False)

    # Настройки и статус
    privacy_level: Mapped[PrivacyLevel] = mapped_column(
        SQLEnum(PrivacyLevel, name="social_privacy_level", native_enum=False),
        nullable=False,
        default=PrivacyLevel.FRIENDS_ONLY
    )
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
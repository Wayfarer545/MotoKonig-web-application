# app/infrastructure/models/user.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.user_role import UserRole

if TYPE_CHECKING:
    from .listing import Listing
    from .listing_favorite import ListingFavorite
    from .motokonig import MotoKonig
    from .motorcycle import Motorcycle
    from .profile import Profile


class User(UUIDAuditBase):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="userrole", native_enum=False), nullable=False, )
    is_active: Mapped[bool] = mapped_column(default=True)

    # Связь с мотоциклами
    motorcycles: Mapped[list["Motorcycle"]] = relationship(
        "Motorcycle",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # Связь с профилем (One-to-One)
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,  # One-to-One отношение
        lazy="selectin"
    )

    # Связь с MotoKonig профилем (One-to-One)
    motokonig_profile: Mapped["MotoKonig"] = relationship(
        "MotoKonig",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,  # One-to-One отношение
        lazy="selectin"
    )

    listings: Mapped[list["Listing"]] = relationship(
        "Listing",
        back_populates="seller",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # Связь с избранными объявлениями
    favorite_listings: Mapped[list["ListingFavorite"]] = relationship(
        "ListingFavorite",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

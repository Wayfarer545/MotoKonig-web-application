# app/infrastructure/models/user.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.user_role import UserRole

if TYPE_CHECKING:
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

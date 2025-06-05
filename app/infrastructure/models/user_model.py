# app/infrastructure/models/user_model.py

from enum import IntEnum
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .motorcycle_model import Motorcycle


class UserRole(IntEnum):
    ADMIN = 0
    OPERATOR = 1
    USER = 2


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
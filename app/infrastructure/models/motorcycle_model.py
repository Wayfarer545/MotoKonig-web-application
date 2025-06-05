# app/infrastructure/models/motorcycle_model.py

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Enum as SQLEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.value_objects.engine_type import EngineType
from domain.value_objects.motorcycle_type import MotorcycleType


class Motorcycle(UUIDAuditBase):
    """SQLAlchemy модель мотоцикла"""

    __tablename__ = "motorcycles"

    # Связь с владельцем
    owner_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    owner: Mapped["User"] = relationship("User", back_populates="motorcycles")

    # Основная информация
    brand: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    # Технические характеристики
    engine_volume: Mapped[int] = mapped_column(Integer, nullable=False)  # в см³
    engine_type: Mapped[EngineType] = mapped_column(
        SQLEnum(EngineType, name="engine_type", native_enum=False),
        nullable=False
    )
    motorcycle_type: Mapped[MotorcycleType] = mapped_column(
        SQLEnum(MotorcycleType, name="motorcycle_type", native_enum=False),
        nullable=False,
        index=True
    )
    power: Mapped[int | None] = mapped_column(Integer, nullable=True)  # в л.с.
    mileage: Mapped[int | None] = mapped_column(Integer, nullable=True)  # в км

    # Дополнительная информация
    color: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Статус
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)
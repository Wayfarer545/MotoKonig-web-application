# app/infrastructure/models/motorcycle_model.py

from enum import Enum

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Enum as SQLEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class EngineType(Enum):
    """Типы двигателей мотоциклов"""
    INLINE_2 = "inline_2"
    INLINE_3 = "inline_3"
    INLINE_4 = "inline_4"
    V_TWIN = "v_twin"
    V4 = "v4"
    SINGLE = "single"
    BOXER = "boxer"
    ELECTRIC = "electric"


class MotorcycleType(Enum):
    """Типы мотоциклов"""
    SPORT = "sport"
    NAKED = "naked"
    TOURING = "touring"
    CRUISER = "cruiser"
    CHOPPER = "chopper"
    ADVENTURE = "adventure"
    DIRT_BIKE = "dirt_bike"
    SUPERMOTO = "supermoto"
    CAFE_RACER = "cafe_racer"
    SCRAMBLER = "scrambler"
    SCOOTER = "scooter"
    TRIKE = "trike"
    ELECTRIC = "electric"


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
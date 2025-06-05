# app/domain/entities/motorcycle.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from domain.value_objects.engine_type import EngineType
from domain.value_objects.motorcycle_type import MotorcycleType

__all__ = ["Motorcycle"]

if TYPE_CHECKING:
    pass


class Motorcycle:
    """
    Доменная сущность мотоцикла

    Инварианты:
    - Год выпуска не может быть в будущем
    - Объем двигателя должен быть положительным числом
    - Мощность должна быть положительным числом
    - Пробег не может быть отрицательным
    """

    def __init__(
            self,
            *,
            motorcycle_id: UUID | None = None,
            owner_id: UUID,
            brand: str,
            model: str,
            year: int,
            engine_volume: int,  # в см³
            engine_type: EngineType,
            motorcycle_type: MotorcycleType,
            power: int | None = None,  # в л.с.
            mileage: int | None = None,  # в км
            color: str | None = None,
            description: str | None = None,
            is_active: bool = True,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        # Валидация инвариантов
        self._validate_year(year)
        self._validate_engine_volume(engine_volume)
        if power is not None:
            self._validate_power(power)
        if mileage is not None:
            self._validate_mileage(mileage)
        self._validate_brand_model(brand, model)

        self.id: UUID = motorcycle_id or uuid4()
        self.owner_id: UUID = owner_id
        self.brand: str = brand.strip().title()
        self.model: str = model.strip()
        self.year: int = year
        self.engine_volume: int = engine_volume
        self.engine_type: EngineType = engine_type
        self.motorcycle_type: MotorcycleType = motorcycle_type
        self.power: int | None = power
        self.mileage: int | None = mileage
        self.color: str | None = color.strip().title() if color else None
        self.description: str | None = description.strip() if description else None
        self.is_active: bool = is_active
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def _validate_year(self, year: int) -> None:
        """Валидация года выпуска"""
        current_year = datetime.now().year
        if year < 1885:  # Первый мотоцикл был создан в 1885 году
            raise ValueError("Year cannot be before 1885")
        if year > current_year + 1:  # Позволяем следующий год для новых моделей
            raise ValueError(f"Year cannot be in the future (max: {current_year + 1})")

    def _validate_engine_volume(self, volume: int) -> None:
        """Валидация объема двигателя"""
        if volume <= 0:
            raise ValueError("Engine volume must be positive")
        if volume > 3000:  # 3000cc - разумный максимум для мотоцикла
            raise ValueError("Engine volume seems too large for a motorcycle")

    def _validate_power(self, power: int) -> None:
        """Валидация мощности"""
        if power <= 0:
            raise ValueError("Power must be positive")
        if power > 500:  # 500 л.с. - разумный максимум
            raise ValueError("Power seems too high for a motorcycle")

    def _validate_mileage(self, mileage: int) -> None:
        """Валидация пробега"""
        if mileage < 0:
            raise ValueError("Mileage cannot be negative")

    def _validate_brand_model(self, brand: str, model: str) -> None:
        """Валидация бренда и модели"""
        if not brand or not brand.strip():
            raise ValueError("Brand cannot be empty")
        if not model or not model.strip():
            raise ValueError("Model cannot be empty")
        if len(brand.strip()) < 2:
            raise ValueError("Brand must be at least 2 characters")
        if len(model.strip()) < 1:
            raise ValueError("Model must be at least 1 character")

    def update_mileage(self, new_mileage: int) -> None:
        """Обновить пробег мотоцикла"""
        if new_mileage < (self.mileage or 0):
            raise ValueError("New mileage cannot be less than current mileage")
        self._validate_mileage(new_mileage)
        self.mileage = new_mileage

    def update_description(self, description: str | None) -> None:
        """Обновить описание мотоцикла"""
        self.description = description.strip() if description else None

    def deactivate(self) -> None:
        """Деактивировать мотоцикл (скрыть из гаража)"""
        self.is_active = False

    def activate(self) -> None:
        """Активировать мотоцикл"""
        self.is_active = True

    def get_display_name(self) -> str:
        """Получить отображаемое имя мотоцикла"""
        return f"{self.brand} {self.model} ({self.year})"

    def get_engine_info(self) -> str:
        """Получить информацию о двигателе"""
        engine_str = f"{self.engine_volume}cc {self.engine_type.value.replace('_', ' ').title()}"
        if self.power:
            engine_str += f", {self.power} hp"
        return engine_str

    def to_dto(self) -> dict:
        """Конвертировать в DTO для API"""
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "engine_volume": self.engine_volume,
            "engine_type": self.engine_type.value,
            "motorcycle_type": self.motorcycle_type.value,
            "power": self.power,
            "mileage": self.mileage,
            "color": self.color,
            "description": self.description,
            "is_active": self.is_active,
            "display_name": self.get_display_name(),
            "engine_info": self.get_engine_info(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

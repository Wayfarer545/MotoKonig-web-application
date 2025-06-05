# app/presentation/schemas/motorcycle.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field, field_validator

from app.domain.value_objects.engine_type import EngineType
from app.domain.value_objects.motorcycle_type import MotorcycleType


class BaseModel(_BaseModel):
    """Базовая модель Pydantic с поддержкой атрибутов SQLAlchemy."""
    model_config = ConfigDict(from_attributes=True)


class CreateMotorcycleSchema(_BaseModel):
    """Схема для создания мотоцикла"""
    brand: str = Field(..., min_length=2, max_length=100, description="Марка мотоцикла")
    model: str = Field(..., min_length=1, max_length=100, description="Модель мотоцикла")
    year: int = Field(..., ge=1885, le=2026, description="Год выпуска")
    engine_volume: int = Field(..., gt=0, le=3000, description="Объем двигателя в см³")
    engine_type: EngineType = Field(EngineType, description="Тип двигателя")
    motorcycle_type: MotorcycleType = Field(MotorcycleType, description="Тип мотоцикла")
    power: int | None = Field(None, gt=0, le=500, description="Мощность в л.с.")
    mileage: int | None = Field(None, ge=0, description="Пробег в км")
    color: str | None = Field(None, max_length=50, description="Цвет")
    description: str | None = Field(None, max_length=2000, description="Описание")

    @field_validator('brand', 'model', 'color')
    @classmethod
    def strip_and_validate_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            return None
        return stripped


class UpdateMotorcycleSchema(_BaseModel):
    """Схема для обновления мотоцикла"""
    brand: str | None = Field(None, min_length=2, max_length=100, description="Марка мотоцикла")
    model: str | None = Field(None, min_length=1, max_length=100, description="Модель мотоцикла")
    year: int | None = Field(None, ge=1885, le=2026, description="Год выпуска")
    engine_volume: int | None = Field(None, gt=0, le=3000, description="Объем двигателя в см³")
    engine_type: EngineType | None = Field(None, description="Тип двигателя")
    motorcycle_type: MotorcycleType | None = Field(None, description="Тип мотоцикла")
    power: int | None = Field(None, gt=0, le=500, description="Мощность в л.с.")
    mileage: int | None = Field(None, ge=0, description="Пробег в км")
    color: str | None = Field(None, max_length=50, description="Цвет")
    description: str | None = Field(None, max_length=2000, description="Описание")
    is_active: bool | None = Field(None, description="Активность мотоцикла")

    @field_validator('brand', 'model', 'color')
    @classmethod
    def strip_and_validate_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            return None
        return stripped


class MotorcycleResponseSchema(BaseModel):
    """Схема ответа с данными мотоцикла"""
    id: UUID
    owner_id: UUID
    brand: str
    model: str
    year: int
    engine_volume: int
    engine_type: str
    motorcycle_type: str
    power: int | None
    mileage: int | None
    color: str | None
    description: str | None
    is_active: bool
    display_name: str
    engine_info: str
    created_at: datetime
    updated_at: datetime


class MotorcycleSearchSchema(_BaseModel):
    """Схема для поиска мотоциклов"""
    brand: str | None = Field(None, description="Марка для поиска")
    model: str | None = Field(None, description="Модель для поиска")
    year_from: int | None = Field(None, ge=1885, description="Год выпуска от")
    year_to: int | None = Field(None, le=2026, description="Год выпуска до")
    motorcycle_type: MotorcycleType | None = Field(None, description="Тип мотоцикла")
    engine_type: EngineType | None = Field(None, description="Тип двигателя")
    engine_volume_from: int | None = Field(None, gt=0, description="Объем двигателя от")
    engine_volume_to: int | None = Field(None, le=3000, description="Объем двигателя до")
    power_from: int | None = Field(None, gt=0, description="Мощность от")
    power_to: int | None = Field(None, le=500, description="Мощность до")
    active_only: bool = Field(True, description="Только активные мотоциклы")

    @field_validator('year_from', 'year_to')
    @classmethod
    def validate_year_range(cls, v, info):
        if info.field_name == 'year_to' and 'year_from' in info.data:
            year_from = info.data['year_from']
            if year_from and v and v < year_from:
                raise ValueError('year_to must be greater than or equal to year_from')
        return v

    @field_validator('engine_volume_to', 'power_to')
    @classmethod
    def validate_ranges(cls, v, info):
        field_name = info.field_name
        if field_name == 'engine_volume_to' and 'engine_volume_from' in info.data:
            from_val = info.data['engine_volume_from']
            if from_val and v and v < from_val:
                raise ValueError('engine_volume_to must be greater than or equal to engine_volume_from')
        elif field_name == 'power_to' and 'power_from' in info.data:
            from_val = info.data['power_from']
            if from_val and v and v < from_val:
                raise ValueError('power_to must be greater than or equal to power_from')
        return v

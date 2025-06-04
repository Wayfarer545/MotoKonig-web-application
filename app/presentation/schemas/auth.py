# app/presentation/schemas/auth.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field, field_validator


class BaseModel(_BaseModel):
    """Базовая модель Pydantic с поддержкой атрибутов SQLAlchemy."""
    model_config = ConfigDict(from_attributes=True)


class LoginRequest(_BaseModel):
    """Схема запроса на вход"""
    username: str = Field(..., min_length=3, description="Имя пользователя")
    password: str = Field(..., min_length=6, description="Пароль")


class TokenResponse(BaseModel):
    """Схема ответа с токенами"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Тип токена")


class RefreshRequest(_BaseModel):
    """Схема запроса на обновление токенов"""
    refresh_token: str = Field(..., description="Refresh token")


class MessageResponse(BaseModel):
    """Схема ответа с сообщением"""
    message: str = Field(..., description="Сообщение")


class CurrentUser(BaseModel):
    """Схема текущего пользователя"""
    user_id: str = Field(..., description="ID пользователя")
    username: str = Field(..., description="Имя пользователя")
    role: str = Field(..., description="Роль пользователя")


# app/presentation/schemas/auth.py
# Добавляем к существующим схемам:

class RegisterRequest(_BaseModel):
    """Схема запроса на регистрацию"""
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    password: str = Field(..., min_length=6, description="Пароль")
    password_confirm: str = Field(..., description="Подтверждение пароля")

    @field_validator('password_confirm')
    def passwords_match(cls, v, values):
        if 'password' in values.data and v != values.data['password']:
            raise ValueError('Passwords do not match')
        return v


class RegisterResponse(BaseModel):
    """Схема ответа после регистрации"""
    id: UUID
    username: str
    role: str
    message: str = "Registration successful"


class SetupPinRequest(_BaseModel):
    """Установка PIN-кода"""
    pin_code: str = Field(..., min_length=4, max_length=6, pattern="^[0-9]+$")
    device_id: str = Field(..., description="Уникальный ID устройства")
    device_name: str = Field(..., description="Название устройства")


class PinLoginRequest(_BaseModel):
    """Вход по PIN-коду"""
    pin_code: str = Field(..., min_length=4, max_length=6)
    device_id: str
    refresh_token: str = Field(..., description="Сохранённый refresh token")


class MobileTokenResponse(TokenResponse):
    """Расширенный ответ для мобильных"""
    device_token: str = Field(..., description="Токен устройства")
    pin_expires_at: datetime = Field(..., description="Когда истекает PIN")


class DeviceInfo(BaseModel):
    """Информация об устройстве"""
    device_id: str
    device_name: str
    created_at: datetime
    last_login: datetime | None = None

class RevokeDeviceRequest(BaseModel):
    """Запрос на отзыв устройства"""
    device_id: str

# app/presentation/schemas/auth.py

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Схема запроса на вход"""
    username: str = Field(..., min_length=3, description="Имя пользователя")
    password: str = Field(..., min_length=6, description="Пароль")


class TokenResponse(BaseModel):
    """Схема ответа с токенами"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Тип токена")


class RefreshRequest(BaseModel):
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
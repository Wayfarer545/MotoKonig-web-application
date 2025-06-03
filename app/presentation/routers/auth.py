# app/presentation/routers/auth.py

from typing import Dict, Any
from fastapi import APIRouter, Depends

from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.application.controllers.auth_controller import AuthController
from app.presentation.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    MessageResponse,
    CurrentUser
)
from app.presentation.middleware.auth import (
    JWTBearer,
    get_current_user,
    require_authenticated
)


router = APIRouter(route_class=DishkaRoute)


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    controller: FromDishka[AuthController]
):
    """Вход в систему"""
    return await controller.login(
        username=credentials.username,
        password=credentials.password
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    token: str = Depends(JWTBearer()),
    controller: FromDishka[AuthController] = None
):
    """Выход из системы"""
    return await controller.logout(token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshRequest,
    controller: FromDishka[AuthController]
):
    """Обновить access token"""
    return await controller.refresh(request.refresh_token)


@router.get("/me", response_model=CurrentUser)
async def get_me(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Получить информацию о текущем пользователе"""
    return CurrentUser(
        user_id=str(current_user["user_id"]),
        username=current_user["username"],
        role=current_user["role"].name
    )
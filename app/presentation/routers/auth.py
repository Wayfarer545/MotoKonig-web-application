# app/presentation/routers/auth.py

from typing import Dict, Any, Annotated
from fastapi import APIRouter, Request, Depends

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from app.domain.ports.token_service import TokenServicePort
from app.application.controllers.auth_controller import AuthController
from app.presentation.schemas.auth import (
    TokenResponse,
    RefreshRequest,
    MessageResponse,
    CurrentUser, RegisterResponse, RegisterRequest
)
from app.presentation.middleware.auth import get_current_user_dishka, get_token_from_header

router = APIRouter(route_class=DishkaRoute)

security = HTTPBasic()

@router.post("/login", response_model=TokenResponse)
async def login(
        controller: FromDishka[AuthController],
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    """Вход в систему"""
    return await controller.login(
        username=credentials.username,
        password=credentials.password
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
        request: Request,
        controller: FromDishka[AuthController]
):
    """Выход из системы"""
    token = await get_token_from_header(request)
    if not token:
        return {"message": "No token provided"}

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
        request: Request,
        token_service: FromDishka[TokenServicePort]
):
    """Получить информацию о текущем пользователе"""
    current_user = await get_current_user_dishka(request, token_service)

    return CurrentUser(
        user_id=str(current_user["user_id"]),
        username=current_user["username"],
        role=current_user["role"].name
    )

@router.post("/register", response_model=RegisterResponse)
async def register(
    request: RegisterRequest,
    controller: FromDishka[AuthController]
):
    """Регистрация нового пользователя"""
    return await controller.register(
        username=request.username,
        password=request.password
    )
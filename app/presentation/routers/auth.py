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
    CurrentUser, RegisterResponse, RegisterRequest, SetupPinRequest, PinLoginRequest, DeviceInfo
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


@router.post("/setup-pin", response_model=Dict[str, Any])
async def setup_pin(
        request: Request,
        pin_request: SetupPinRequest,
        controller: FromDishka[AuthController],
        token_service: FromDishka[TokenServicePort]
):
    """Установить PIN для мобильного устройства"""
    current_user = await get_current_user_dishka(request, token_service)

    return await controller.setup_pin(
        user_id=current_user["user_id"],
        pin_code=pin_request.pin_code,
        device_id=pin_request.device_id,
        device_name=pin_request.device_name
    )


@router.post("/pin-login", response_model=TokenResponse)
async def pin_login(
        request: PinLoginRequest,
        controller: FromDishka[AuthController]
):
    """Вход по PIN-коду"""
    return await controller.pin_login(
        pin_code=request.pin_code,
        device_id=request.device_id,
        refresh_token=request.refresh_token
    )

# app/presentation/routers/auth.py

@router.get("/devices", response_model=list[DeviceInfo])
async def list_devices(
    request: Request,
    controller: FromDishka[AuthController],
    token_service: FromDishka[TokenServicePort]
):
    """Получить список устройств пользователя"""
    current_user = await get_current_user_dishka(request, token_service)
    return await controller.list_devices(current_user["user_id"])

@router.delete("/devices/{device_id}")
async def revoke_device(
    device_id: str,
    request: Request,
    controller: FromDishka[AuthController],
    token_service: FromDishka[TokenServicePort]
):
    """Отозвать доступ устройства"""
    current_user = await get_current_user_dishka(request, token_service)
    await controller.revoke_device(current_user["user_id"], device_id)
    return {"message": "Device revoked successfully"}
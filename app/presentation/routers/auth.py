# app/presentation/routers/auth.py

from typing import Annotated, Any

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.application.controllers.auth_controller import AuthController
from app.application.exceptions import (
    BadRequestError,
    InternalError,
    TooManyRequestsError,
    UnauthorizedError,
)
from app.domain.ports.token_service import TokenServicePort
from presentation.dependencies.auth import (
    get_current_user_dishka,
    get_token_from_header,
)
from app.presentation.schemas.auth import (
    CurrentUser,
    DeviceInfo,
    MessageResponse,
    PinLoginRequest,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
    SetupPinRequest,
    TokenResponse,
)

router = APIRouter(route_class=DishkaRoute)

security = HTTPBasic()

@router.post("/login", response_model=TokenResponse)
async def login(
        controller: FromDishka[AuthController],
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    """Вход в систему"""
    try:
        return await controller.login(
            username=credentials.username,
            password=credentials.password,
        )
    except UnauthorizedError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ex),
            headers={"WWW-Authenticate": "Bearer"},
        ) from ex


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
    try:
        return await controller.refresh(request.refresh_token)
    except UnauthorizedError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ex),
            headers={"WWW-Authenticate": "Bearer"},
        ) from ex


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
    try:
        return await controller.register(
            username=request.username,
            password=request.password,
        )
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex),
        ) from ex


@router.post("/setup-pin", response_model=dict[str, Any])
async def setup_pin(
        request: Request,
        pin_request: SetupPinRequest,
        controller: FromDishka[AuthController],
        token_service: FromDishka[TokenServicePort]
):
    """Установить PIN для мобильного устройства"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        return await controller.setup_pin(
            user_id=current_user["user_id"],
            pin_code=pin_request.pin_code,
            device_id=pin_request.device_id,
            device_name=pin_request.device_name,
        )
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex),
        ) from ex


@router.post("/pin-login", response_model=TokenResponse)
async def pin_login(
        request: PinLoginRequest,
        controller: FromDishka[AuthController]
):
    """Вход по PIN-коду"""
    try:
        return await controller.pin_login(
            pin_code=request.pin_code,
            device_id=request.device_id,
            refresh_token=request.refresh_token,
        )
    except UnauthorizedError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ex),
        ) from ex
    except TooManyRequestsError as ex:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(ex),
        ) from ex

# app/presentation/routers/auth.py

@router.get("/devices", response_model=list[DeviceInfo])
async def list_devices(
    request: Request,
    controller: FromDishka[AuthController],
    token_service: FromDishka[TokenServicePort]
):
    """Получить список устройств пользователя"""
    current_user = await get_current_user_dishka(request, token_service)
    try:
        return await controller.list_devices(current_user["user_id"])
    except InternalError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex),
        ) from ex

@router.delete("/devices/{device_id}")
async def revoke_device(
    device_id: str,
    request: Request,
    controller: FromDishka[AuthController],
    token_service: FromDishka[TokenServicePort]
):
    """Отозвать доступ устройства"""
    current_user = await get_current_user_dishka(request, token_service)
    try:
        await controller.revoke_device(current_user["user_id"], device_id)
    except InternalError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex),
        ) from ex
    return {"message": "Device revoked successfully"}

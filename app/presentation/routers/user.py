# app/presentation/routers/user.py

from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Request, status

from app.application.controllers.user_controller import UserController
from app.application.exceptions import NotFoundError
from app.domain.ports.services.token import TokenServicePort
from app.domain.value_objects.user_role import UserRole
from app.presentation.dependencies.auth import check_role, get_current_user_dishka
from app.presentation.schemas.user import (
    CreateUserSchema,
    UpdateUserSchema,
    UserResponseSchema,
)

router = APIRouter(route_class=DishkaRoute)


@router.post("/", response_model=UserResponseSchema, status_code=201)
async def create_user(
        request: Request,
        dto: CreateUserSchema,
        controller: FromDishka[UserController],
        token_service: FromDishka[TokenServicePort]
):
    """Создать нового пользователя (только для админов)"""
    current_user = await get_current_user_dishka(request, token_service)
    check_role(current_user, [UserRole.ADMIN])

    return await controller.create(dto.username, dto.password, dto.role)


@router.get("/", response_model=list[UserResponseSchema])
async def list_users(
        request: Request,
        controller: FromDishka[UserController],
        token_service: FromDishka[TokenServicePort]
):
    """Получить список всех пользователей"""
    current_user = await get_current_user_dishka(request, token_service)
    check_role(current_user, [UserRole.ADMIN, UserRole.OPERATOR])

    return await controller.list_users()


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(
        request: Request,
        user_id: UUID,
        controller: FromDishka[UserController],
        token_service: FromDishka[TokenServicePort]
):
    """Получить пользователя по ID"""
    current_user = await get_current_user_dishka(request, token_service)

    # Пользователь может просматривать только свой профиль
    # Операторы и админы могут просматривать всех
    if (current_user["role"].value > 1 and
            current_user["user_id"] != user_id):
        raise HTTPException(status_code=403, detail="Access denied")

    user_data = await controller.get_user_by_id(user_id)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data


@router.put("/{user_id}", response_model=UserResponseSchema)
async def update_user(
        request: Request,
        user_id: UUID,
        dto: UpdateUserSchema,
        controller: FromDishka[UserController],
        token_service: FromDishka[TokenServicePort]
):
    """Обновить данные пользователя"""
    current_user = await get_current_user_dishka(request, token_service)

    # Пользователь может изменять только свои данные (кроме роли)
    # Операторы и админы могут изменять всё
    if current_user["role"].value > 1:
        if current_user["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        # Обычные пользователи не могут менять роль
        if dto.role is not None:
            raise HTTPException(status_code=403, detail="Cannot change role")
    try:
        return await controller.update_user(
            user_id,
            username=dto.username,
            password=dto.password,
            role=dto.role,
            deactivate=dto.deactivate,
        )
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex),
        ) from ex


@router.delete("/{user_id}", status_code=204)
async def delete_user(
        request: Request,
        user_id: UUID,
        controller: FromDishka[UserController],
        token_service: FromDishka[TokenServicePort]
):
    """Удалить пользователя (только для админов)"""
    current_user = await get_current_user_dishka(request, token_service)
    check_role(current_user, [UserRole.ADMIN])
    try:
        await controller.delete_user(user_id)
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex),
        ) from ex

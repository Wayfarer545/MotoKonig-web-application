# app/presentation/routers/user.py

from fastapi import APIRouter, Depends
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from app.application.controllers.user_controller import UserController
from app.presentation.schemas.user import (
    CreateUserSchema,
    UpdateUserSchema,
    UserResponseSchema
)

router = APIRouter(route_class=DishkaRoute)

@router.get("/", response_model=list[UserResponseSchema])
async def list_users(controller: FromDishka[UserController]):
    return await controller.list_users()

@router.post("/", response_model=UserResponseSchema, status_code=201)
async def create_user(
    dto: CreateUserSchema,
    controller: FromDishka[UserController],
):
    return await controller.create(dto.username, dto.password, dto.role)

@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(user_id: UUID, controller: FromDishka[UserController]):
    return await controller.get_user_by_id(user_id)

@router.put("/{user_id}", response_model=UserResponseSchema)
async def update_user(
    user_id: UUID,
    dto: UpdateUserSchema,
    controller: FromDishka[UserController],
):
    return await controller.update_user(
        user_id,
        username=dto.username,
        password=dto.password,
        role=dto.role,
        deactivate=dto.deactivate,
    )

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: UUID, controller: FromDishka[UserController]):
    await controller.delete_user(user_id)

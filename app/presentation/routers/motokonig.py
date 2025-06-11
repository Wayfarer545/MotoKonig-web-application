# app/presentation/routers/motokonig.py

from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Request

from app.application.controllers.motokonig_controller import MotoKonigController
from app.domain.ports.services.token import TokenServicePort
from app.presentation.dependencies.auth import get_current_user_dishka
from app.presentation.schemas.motokonig import (
    CreateMotoKonigProfileSchema,
    MotoKonigListItemSchema,
    MotoKonigResponseSchema,
    UpdateMotoKonigProfileSchema,
)

router = APIRouter(route_class=DishkaRoute)


@router.post("/", response_model=MotoKonigResponseSchema, status_code=201)
async def create_profile(
        request: Request,
        dto: CreateMotoKonigProfileSchema,
        controller: FromDishka[MotoKonigController],
        token_service: FromDishka[TokenServicePort]
):
    """Создать профиль MotoKonig"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        profile = await controller.create_profile(
            user_id=current_user["user_id"],
            nickname=dto.nickname,
            bio=dto.bio,
            avatar_url=dto.avatar_url,
            is_public=dto.is_public,
        )
        return profile.to_dto()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/me", response_model=MotoKonigResponseSchema)
async def get_my_profile(
        request: Request,
        controller: FromDishka[MotoKonigController],
        token_service: FromDishka[TokenServicePort]
):
    """Получить свой профиль MotoKonig"""
    current_user = await get_current_user_dishka(request, token_service)

    profile = await controller.get_profile_by_user_id(current_user["user_id"])
    if not profile:
        raise HTTPException(status_code=404, detail="MotoKonig profile not found")

    return profile.to_dto()


@router.get("/top", response_model=list[MotoKonigListItemSchema])
async def get_top_riders(
        controller: FromDishka[MotoKonigController],
        limit: int = 10
):
    """Получить топ райдеров"""
    profiles = await controller.get_top_riders(limit)

    return [
        MotoKonigListItemSchema(
            motokonig_id=p.motokonig_id,
            nickname=p.nickname,
            status=p.status,
            rating=p.rating,
            total_distance=p.total_distance,
            avatar_url=p.avatar_url,
        )
        for p in profiles
    ]


@router.get("/{motokonig_id}", response_model=MotoKonigResponseSchema)
async def get_profile(
        motokonig_id: UUID,
        controller: FromDishka[MotoKonigController]
):
    """Получить профиль MotoKonig по ID"""
    profile = await controller.get_profile_by_id(motokonig_id)
    if not profile:
        raise HTTPException(status_code=404, detail="MotoKonig profile not found")

    # Проверяем публичность профиля
    if not profile.is_public:
        raise HTTPException(status_code=403, detail="Profile is private")

    return profile.to_dto()


@router.patch("/{motokonig_id}", response_model=MotoKonigResponseSchema)
async def update_profile(
        request: Request,
        motokonig_id: UUID,
        dto: UpdateMotoKonigProfileSchema,
        controller: FromDishka[MotoKonigController],
        token_service: FromDishka[TokenServicePort]
):
    """Обновить профиль MotoKonig"""
    current_user = await get_current_user_dishka(request, token_service)

    # Проверяем, что пользователь обновляет свой профиль
    profile = await controller.get_profile_by_id(motokonig_id)
    if not profile or profile.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Cannot update other user's profile")

    try:
        updated = await controller.update_profile(
            motokonig_id=motokonig_id,
            nickname=dto.nickname,
            bio=dto.bio,
            avatar_url=dto.avatar_url,
            is_public=dto.is_public,
        )
        return updated.to_dto()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/{motokonig_id}", status_code=204)
async def delete_profile(
        request: Request,
        motokonig_id: UUID,
        controller: FromDishka[MotoKonigController],
        token_service: FromDishka[TokenServicePort]
):
    """Удалить профиль MotoKonig"""
    current_user = await get_current_user_dishka(request, token_service)

    # Проверяем права
    profile = await controller.get_profile_by_id(motokonig_id)
    if not profile or profile.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Cannot delete other user's profile")

    await controller.delete_profile(motokonig_id)

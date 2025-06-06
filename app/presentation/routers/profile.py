# app/presentation/routers/profile.py

from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Request, status

from app.application.controllers.profile_controller import ProfileController
from app.application.exceptions import NotFoundError
from app.domain.value_objects.privacy_level import PrivacyLevel as DomainPrivacyLevel
from app.domain.value_objects.social_link import SocialPlatform as DomainSocialPlatform


from app.domain.ports.token_service import TokenServicePort
from app.presentation.middleware.auth import get_current_user_dishka
from app.presentation.schemas.profile import (
    AddSocialLinkSchema,
    CreateProfileSchema,
    ProfileResponseSchema,
    SocialLinkResponseSchema,
    UpdateProfileSchema,
)

router = APIRouter(route_class=DishkaRoute)


def convert_enum_to_domain_privacy(schema_enum):
    """Конвертировать схему privacy enum в доменный enum"""
    if schema_enum is None:
        return None
    return DomainPrivacyLevel(schema_enum.value)


def convert_enum_to_domain_platform(schema_enum):
    """Конвертировать схему platform enum в доменный enum"""
    if schema_enum is None:
        return None
    return DomainSocialPlatform(schema_enum.value)


@router.post("/", response_model=ProfileResponseSchema, status_code=201)
async def create_profile(
        request: Request,
        dto: CreateProfileSchema,
        controller: FromDishka[ProfileController],
        token_service: FromDishka[TokenServicePort]
):
    """Создать профиль текущего пользователя"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        profile = await controller.create_profile(
            user_id=current_user["user_id"],
            bio=dto.bio,
            location=dto.location,
            phone=dto.phone,
            date_of_birth=dto.date_of_birth,
            riding_experience=dto.riding_experience,
            privacy_level=convert_enum_to_domain_privacy(dto.privacy_level),
            phone_privacy=convert_enum_to_domain_privacy(dto.phone_privacy),
            location_privacy=convert_enum_to_domain_privacy(dto.location_privacy),
        )
        return profile.to_dto()
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex


@router.get("/my", response_model=ProfileResponseSchema)
async def get_my_profile(
        request: Request,
        controller: FromDishka[ProfileController],
        token_service: FromDishka[TokenServicePort]
):
    """Получить профиль текущего пользователя"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Для собственного профиля показываем всё
        profile_dto = await controller.get_profile_by_user_id(
            user_id=current_user["user_id"],
            viewer_role=current_user["role"].name,
            is_friend=True,  # Для себя всегда true
            is_club_member=True
        )
        return profile_dto
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


@router.get("/user/{user_id}", response_model=ProfileResponseSchema)
async def get_user_profile(
        request: Request,
        user_id: UUID,
        controller: FromDishka[ProfileController],
        token_service: FromDishka[TokenServicePort]
):
    """Получить профиль пользователя"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # TODO: Здесь нужно будет проверять дружбу и членство в клубах
        is_friend = False  # Заглушка
        is_club_member = False  # Заглушка

        profile_dto = await controller.get_profile_by_user_id(
            user_id=user_id,
            viewer_role=current_user["role"].name,
            is_friend=is_friend,
            is_club_member=is_club_member
        )
        return profile_dto
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


@router.get("/{profile_id}", response_model=ProfileResponseSchema)
async def get_profile(
        request: Request,
        profile_id: UUID,
        controller: FromDishka[ProfileController],
        token_service: FromDishka[TokenServicePort]
):
    """Получить профиль по ID"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # TODO: Здесь нужно будет проверять дружбу и членство в клубах
        is_friend = False  # Заглушка
        is_club_member = False  # Заглушка

        profile_dto = await controller.get_profile_by_id(
            profile_id=profile_id,
            viewer_role=current_user["role"].name,
            is_friend=is_friend,
            is_club_member=is_club_member
        )
        return profile_dto
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


@router.put("/my", response_model=ProfileResponseSchema)
async def update_my_profile(
        request: Request,
        dto: UpdateProfileSchema,
        controller: FromDishka[ProfileController],
        token_service: FromDishka[TokenServicePort]
):
    """Обновить профиль текущего пользователя"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Сначала получаем профиль пользователя
        existing_profile = await controller.get_profile_by_user_id(
            user_id=current_user["user_id"],
            viewer_role=current_user["role"].name,
            is_friend=True,
            is_club_member=True
        )

        profile_dto = await controller.update_profile(
            profile_id=UUID(existing_profile["id"]),
            bio=dto.bio,
            location=dto.location,
            phone=dto.phone,
            date_of_birth=dto.date_of_birth,
            riding_experience=dto.riding_experience,
            privacy_level=convert_enum_to_domain_privacy(dto.privacy_level),
            phone_privacy=convert_enum_to_domain_privacy(dto.phone_privacy),
            location_privacy=convert_enum_to_domain_privacy(dto.location_privacy),
            viewer_role=current_user["role"].name,
            is_friend=True,
            is_club_member=True
        )
        return profile_dto
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex


@router.delete("/my", status_code=204)
async def delete_my_profile(
        request: Request,
        controller: FromDishka[ProfileController],
        token_service: FromDishka[TokenServicePort]
):
    """Удалить профиль текущего пользователя"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Сначала получаем профиль пользователя
        existing_profile = await controller.get_profile_by_user_id(
            user_id=current_user["user_id"],
            viewer_role=current_user["role"].name,
            is_friend=True,
            is_club_member=True
        )

        await controller.delete_profile(UUID(existing_profile["id"]))
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


# Социальные ссылки
@router.post("/my/social-links", response_model=SocialLinkResponseSchema, status_code=201)
async def add_social_link(
        request: Request,
        dto: AddSocialLinkSchema,
        controller: FromDishka[ProfileController],
        token_service: FromDishka[TokenServicePort]
):
    """Добавить социальную ссылку к профилю"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Получаем профиль пользователя
        existing_profile = await controller.get_profile_by_user_id(
            user_id=current_user["user_id"],
            viewer_role=current_user["role"].name,
            is_friend=True,
            is_club_member=True
        )

        link_dto = await controller.add_social_link(
            profile_id=UUID(existing_profile["id"]),
            platform=convert_enum_to_domain_platform(dto.platform),
            url=dto.url,
            privacy_level=convert_enum_to_domain_privacy(dto.privacy_level),
            viewer_role=current_user["role"].name,
            is_friend=True,
            is_club_member=True
        )
        return link_dto
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex


@router.get("/my/social-links", response_model=list[SocialLinkResponseSchema])
async def get_my_social_links(
        request: Request,
        controller: FromDishka[ProfileController],
        token_service: FromDishka[TokenServicePort]
):
    """Получить социальные ссылки профиля"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Получаем профиль пользователя
        existing_profile = await controller.get_profile_by_user_id(
            user_id=current_user["user_id"],
            viewer_role=current_user["role"].name,
            is_friend=True,
            is_club_member=True
        )

        links = await controller.get_profile_social_links(
            profile_id=UUID(existing_profile["id"]),
            viewer_role=current_user["role"].name,
            is_friend=True,
            is_club_member=True
        )
        return links
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


@router.delete("/my/social-links/{platform}", status_code=204)
async def remove_social_link(
        request: Request,
        platform: str,
        controller: FromDishka[ProfileController],
        token_service: FromDishka[TokenServicePort]
):
    """Удалить социальную ссылку"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Получаем профиль пользователя
        existing_profile = await controller.get_profile_by_user_id(
            user_id=current_user["user_id"],
            viewer_role=current_user["role"].name,
            is_friend=True,
            is_club_member=True
        )

        # Конвертируем платформу
        social_platform = DomainSocialPlatform(platform)

        await controller.remove_social_link(
            profile_id=UUID(existing_profile["id"]),
            platform=social_platform
        )
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid platform: {platform}"
        ) from ex


@router.get("/{profile_id}/social-links", response_model=list[SocialLinkResponseSchema])
async def get_profile_social_links(
        request: Request,
        profile_id: UUID,
        controller: FromDishka[ProfileController],
        token_service: FromDishka[TokenServicePort]
):
    """Получить социальные ссылки профиля (с учетом приватности)"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # TODO: Здесь нужно будет проверять дружбу и членство в клубах
        is_friend = False  # Заглушка
        is_club_member = False  # Заглушка

        links = await controller.get_profile_social_links(
            profile_id=profile_id,
            viewer_role=current_user["role"].name,
            is_friend=is_friend,
            is_club_member=is_club_member
        )
        return links
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex
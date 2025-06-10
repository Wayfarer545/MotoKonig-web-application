# app/presentation/routers/listing.py

from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.application.controllers.listing_controller import ListingController
from app.application.exceptions import BadRequestError, NotFoundError
from app.domain.entities.user import UserRole
from app.domain.ports.services.token import TokenServicePort
from app.domain.value_objects.listing_category import ListingCategory as DomainListingCategory
from app.presentation.dependencies.auth import get_current_user_dishka
from app.presentation.schemas.listing import (
    CreateListingSchema,
    FavoriteResponseSchema,
    ListingDetailResponseSchema,
    ListingResponseSchema,
    ListingSearchSchema,
    MessageResponseSchema,
    UpdateListingSchema,
)

router = APIRouter(route_class=DishkaRoute)


def convert_enum_to_domain_category(schema_enum):
    """Конвертировать схему category enum в доменный enum"""
    if schema_enum is None:
        return None
    return DomainListingCategory(schema_enum.value)


@router.post("/", response_model=ListingResponseSchema, status_code=201)
async def create_listing(
        request: Request,
        dto: CreateListingSchema,
        controller: FromDishka[ListingController],
        token_service: FromDishka[TokenServicePort]
):
    """Создать новое объявление"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        listing = await controller.create_listing(
            seller_id=current_user["user_id"],
            title=dto.title,
            description=dto.description,
            category=dto.category,
            price=dto.price,
            location=dto.location,
            is_negotiable=dto.is_negotiable,
            contact_phone=dto.contact_phone,
            contact_email=dto.contact_email,
            photo_urls=dto.photo_urls,
        )
        return listing.to_dto()
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex


@router.get("/search", response_model=list[ListingResponseSchema])
async def search_listings(
        request: Request,
        controller: FromDishka[ListingController],
        token_service: FromDishka[TokenServicePort],
        search_params: ListingSearchSchema = Depends(),
):
    """Поиск объявлений с фильтрами"""
    await get_current_user_dishka(request, token_service)

    listings = await controller.search_listings(
        category=convert_enum_to_domain_category(search_params.category),
        location=search_params.location,
        price_min=search_params.price_min,
        price_max=search_params.price_max,
        search_query=search_params.search_query,
        seller_id=search_params.seller_id,
        featured_first=search_params.featured_first,
    )
    return listings


@router.get("/my", response_model=list[ListingDetailResponseSchema])
async def get_my_listings(
        request: Request,
        controller: FromDishka[ListingController],
        token_service: FromDishka[TokenServicePort],
):
    """Получить объявления текущего пользователя"""
    current_user = await get_current_user_dishka(request, token_service)

    listings = await controller.search_listings(
        seller_id=current_user["user_id"],
        active_only=False,  # Показываем все статусы для владельца
    )
    # Конвертируем в расширенный формат с приватной информацией
    return [
        {**listing, "contact_phone": None, "contact_email": None, "moderation_notes": None}
        for listing in listings
    ]


@router.get("/{listing_id}", response_model=ListingResponseSchema)
async def get_listing(
        request: Request,
        listing_id: UUID,
        controller: FromDishka[ListingController],
        token_service: FromDishka[TokenServicePort]
):
    """Получить объявление по ID"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        listing = await controller.get_listing_by_id(listing_id)

        # Если это владелец или админ/оператор, показываем приватную информацию
        if (current_user["role"] in [UserRole.ADMIN, UserRole.OPERATOR] or
                str(current_user["user_id"]) == str(listing["seller_id"])):
            listing_with_private = await controller.get_listing_with_private_info(listing_id)
            return listing_with_private

        return listing
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


@router.put("/{listing_id}", response_model=ListingDetailResponseSchema)
async def update_listing(
        request: Request,
        listing_id: UUID,
        dto: UpdateListingSchema,
        controller: FromDishka[ListingController],
        token_service: FromDishka[TokenServicePort]
):
    """Обновить объявление"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Сначала проверяем существование и права
        existing = await controller.get_listing_by_id(listing_id)

        # Проверяем права доступа
        if (current_user["role"] not in [UserRole.ADMIN, UserRole.OPERATOR] and
                str(current_user["user_id"]) != str(existing["seller_id"])):
            raise HTTPException(status_code=403, detail="Access denied")

        # Обновляем
        listing = await controller.update_listing(
            listing_id=listing_id,
            title=dto.title,
            description=dto.description,
            category=convert_enum_to_domain_category(dto.category),
            price=dto.price,
            location=dto.location,
            is_negotiable=dto.is_negotiable,
            contact_phone=dto.contact_phone,
            contact_email=dto.contact_email,
        )
        return listing
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex


@router.delete("/{listing_id}", status_code=204)
async def delete_listing(
        request: Request,
        listing_id: UUID,
        controller: FromDishka[ListingController],
        token_service: FromDishka[TokenServicePort]
):
    """Удалить объявление"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Сначала проверяем существование и права
        existing = await controller.get_listing_by_id(listing_id)

        # Проверяем права доступа (только владелец или админ)
        if (current_user["role"] != UserRole.ADMIN and
                str(current_user["user_id"]) != str(existing["seller_id"])):
            raise HTTPException(status_code=403, detail="Access denied")

        await controller.delete_listing(listing_id)
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


# Избранное
@router.post("/{listing_id}/favorite", response_model=FavoriteResponseSchema)
async def add_to_favorites(
        request: Request,
        listing_id: UUID,
        controller: FromDishka[ListingController],
        token_service: FromDishka[TokenServicePort]
):
    """Добавить объявление в избранное"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        favorite = await controller.add_to_favorites(
            user_id=current_user["user_id"],
            listing_id=listing_id
        )
        return favorite
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex


@router.delete("/{listing_id}/favorite", response_model=MessageResponseSchema)
async def remove_from_favorites(
        request: Request,
        listing_id: UUID,
        controller: FromDishka[ListingController],
        token_service: FromDishka[TokenServicePort]
):
    """Удалить объявление из избранного"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        await controller.remove_from_favorites(
            user_id=current_user["user_id"],
            listing_id=listing_id
        )
        return {"message": "Removed from favorites successfully"}
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex

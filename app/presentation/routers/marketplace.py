# app/presentation/routers/marketplace.py

from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.application.controllers.marketplace_controller import MarketplaceController
from app.application.exceptions import BadRequestError, NotFoundError
from domain.ports.services.token_service import TokenServicePort
from app.domain.value_objects.user_role import UserRole
from app.presentation.middleware.auth import check_role, get_current_user_dishka
from app.presentation.schemas.marketplace import (
    CategoryResponseSchema,
    CreateCategorySchema,
    CreateListingSchema,
    ListingResponseSchema,
    ListingSearchSchema,
    UpdateListingSchema,
)

router = APIRouter(route_class=DishkaRoute)


# Роуты для объявлений
@router.post("/listings", response_model=ListingResponseSchema, status_code=201)
async def create_listing(
        request: Request,
        dto: CreateListingSchema,
        controller: FromDishka[MarketplaceController],
        token_service: FromDishka[TokenServicePort]
):
    """Создать новое объявление"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        listing = await controller.create_listing(
            seller_id=current_user["user_id"],
            category_id=dto.category_id,
            title=dto.title,
            description=dto.description,
            price=dto.price,
            listing_type=dto.listing_type,
            location=dto.location,
            latitude=dto.latitude,
            longitude=dto.longitude,
            contact_phone=dto.contact_phone,
            contact_email=dto.contact_email,
            is_negotiable=dto.is_negotiable,
            condition=dto.condition,
            brand=dto.brand,
            model=dto.model,
            year=dto.year,
            mileage=dto.mileage,
        )
        return listing
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex


@router.get("/listings/search", response_model=list[ListingResponseSchema])
async def search_listings(
        request: Request,
        controller: FromDishka[MarketplaceController],
        token_service: FromDishka[TokenServicePort],
        search_params: ListingSearchSchema = Depends(),
):
    """Поиск объявлений с фильтрами"""
    await get_current_user_dishka(request, token_service)

    listings = await controller.search_listings(
        query=search_params.query,
        category_id=search_params.category_id,
        min_price=search_params.min_price,
        max_price=search_params.max_price,
        location=search_params.location,
        brand=search_params.brand,
        model=search_params.model,
        year_from=search_params.year_from,
        year_to=search_params.year_to,
        condition=search_params.condition,
        listing_type=search_params.listing_type.value if search_params.listing_type else None,
        active_only=search_params.active_only,
    )
    return listings


@router.get("/listings/my", response_model=list[ListingResponseSchema])
async def get_my_listings(
        request: Request,
        controller: FromDishka[MarketplaceController],
        token_service: FromDishka[TokenServicePort],
        active_only: bool = True,
):
    """Получить объявления текущего пользователя"""
    current_user = await get_current_user_dishka(request, token_service)

    listings = await controller.get_seller_listings(
        seller_id=current_user["user_id"],
        active_only=active_only
    )
    return listings


@router.get("/listings/seller/{seller_id}", response_model=list[ListingResponseSchema])
async def get_seller_listings(
        request: Request,
        seller_id: UUID,
        controller: FromDishka[MarketplaceController],
        token_service: FromDishka[TokenServicePort],
        active_only: bool = True
):
    """Получить объявления продавца"""
    current_user = await get_current_user_dishka(request, token_service)

    # Проверяем права доступа
    if (current_user["role"].value > 1 and
            current_user["user_id"] != seller_id):
        # Обычные пользователи могут видеть только активные объявления других
        active_only = True

    listings = await controller.get_seller_listings(
        seller_id=seller_id,
        active_only=active_only
    )
    return listings


@router.get("/listings/{listing_id}", response_model=ListingResponseSchema)
async def get_listing(
        request: Request,
        listing_id: UUID,
        controller: FromDishka[MarketplaceController],
        token_service: FromDishka[TokenServicePort],
        increment_views: bool = True
):
    """Получить объявление по ID"""
    await get_current_user_dishka(request, token_service)

    try:
        listing = await controller.get_listing_by_id(
            listing_id=listing_id,
            increment_views=increment_views
        )
        return listing
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


@router.put("/listings/{listing_id}", response_model=ListingResponseSchema)
async def update_listing(
        request: Request,
        listing_id: UUID,
        dto: UpdateListingSchema,
        controller: FromDishka[MarketplaceController],
        token_service: FromDishka[TokenServicePort]
):
    """Обновить объявление"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Сначала проверяем существование и права
        existing = await controller.get_listing_by_id(listing_id, increment_views=False)

        # Проверяем права доступа
        if (current_user["role"] not in [UserRole.ADMIN, UserRole.OPERATOR] and
                str(current_user["user_id"]) != str(existing["seller_id"])):
            raise HTTPException(status_code=403, detail="Access denied")

        # Обновляем
        listing = await controller.update_listing(
            listing_id=listing_id,
            title=dto.title,
            description=dto.description,
            price=dto.price,
            listing_type=dto.listing_type,
            location=dto.location,
            latitude=dto.latitude,
            longitude=dto.longitude,
            contact_phone=dto.contact_phone,
            contact_email=dto.contact_email,
            is_negotiable=dto.is_negotiable,
            condition=dto.condition,
            brand=dto.brand,
            model=dto.model,
            year=dto.year,
            mileage=dto.mileage,
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


@router.post("/listings/{listing_id}/publish", response_model=ListingResponseSchema)
async def publish_listing(
        request: Request,
        listing_id: UUID,
        controller: FromDishka[MarketplaceController],
        token_service: FromDishka[TokenServicePort]
):
    """Опубликовать объявление"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Проверяем права доступа
        existing = await controller.get_listing_by_id(listing_id, increment_views=False)

        if (current_user["role"] not in [UserRole.ADMIN, UserRole.OPERATOR] and
                str(current_user["user_id"]) != str(existing["seller_id"])):
            raise HTTPException(status_code=403, detail="Access denied")

        listing = await controller.publish_listing(listing_id)
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


@router.delete("/listings/{listing_id}", status_code=204)
async def delete_listing(
        request: Request,
        listing_id: UUID,
        controller: FromDishka[MarketplaceController],
        token_service: FromDishka[TokenServicePort]
):
    """Удалить объявление"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Проверяем права доступа
        existing = await controller.get_listing_by_id(listing_id, increment_views=False)

        if (current_user["role"] != UserRole.ADMIN and
                str(current_user["user_id"]) != str(existing["seller_id"])):
            raise HTTPException(status_code=403, detail="Access denied")

        await controller.delete_listing(listing_id)
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


# Роуты для категорий
@router.post("/categories", response_model=CategoryResponseSchema, status_code=201)
async def create_category(
        request: Request,
        dto: CreateCategorySchema,
        controller: FromDishka[MarketplaceController],
        token_service: FromDishka[TokenServicePort]
):
    """Создать новую категорию (только для админов)"""
    current_user = await get_current_user_dishka(request, token_service)
    check_role(current_user, [UserRole.ADMIN])

    try:
        category = await controller.create_category(
            name=dto.name,
            slug=dto.slug,
            description=dto.description,
            parent_id=dto.parent_id,
            icon=dto.icon,
            sort_order=dto.sort_order,
        )
        return category
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex
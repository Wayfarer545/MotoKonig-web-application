# app/presentation/routers/motorcycle.py

from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.application.controllers.motorcycle_controller import MotorcycleController
from app.application.exceptions import NotFoundError
from app.domain.entities.user import UserRole
from app.domain.ports.token_service import TokenServicePort
from app.domain.value_objects.engine_type import EngineType as DomainEngineType
from app.domain.value_objects.motorcycle_type import (
    MotorcycleType as DomainMotorcycleType,
)
from presentation.dependencies.auth import get_current_user_dishka
from app.presentation.schemas.motorcycle import (
    CreateMotorcycleSchema,
    MotorcycleResponseSchema,
    MotorcycleSearchSchema,
    UpdateMotorcycleSchema,
)

router = APIRouter(route_class=DishkaRoute)


def convert_enum_to_domain(schema_enum, domain_enum_class):
    """Конвертировать схему enum в доменный enum"""
    if schema_enum is None:
        return None
    return domain_enum_class(schema_enum.value)


@router.post("/", response_model=MotorcycleResponseSchema, status_code=201)
async def create_motorcycle(
        request: Request,
        dto: CreateMotorcycleSchema,
        controller: FromDishka[MotorcycleController],
        token_service: FromDishka[TokenServicePort]
):
    """Создать новый мотоцикл"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        motorcycle = await controller.create_motorcycle(
            owner_id=current_user["user_id"],
            brand=dto.brand,
            model=dto.model,
            year=dto.year,
            engine_volume=dto.engine_volume,
            engine_type=dto.engine_type,
            motorcycle_type=dto.motorcycle_type.value,
            power=dto.power,
            mileage=dto.mileage,
            color=dto.color,
            description=dto.description,
        )
        return motorcycle.to_dto()
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex


@router.get("/my", response_model=list[MotorcycleResponseSchema])
async def get_my_motorcycles(
        request: Request,
        controller: FromDishka[MotorcycleController],
        token_service: FromDishka[TokenServicePort],
        active_only: bool = True,
):
    """Получить мотоциклы текущего пользователя"""
    current_user = await get_current_user_dishka(request, token_service)
    motorcycles = await controller.get_user_motorcycles(
        owner_id=current_user["user_id"],
        active_only=active_only
    )
    return motorcycles


@router.get("/user/{user_id}", response_model=list[MotorcycleResponseSchema])
async def get_user_motorcycles(
        request: Request,
        user_id: UUID,
        controller: FromDishka[MotorcycleController],
        token_service: FromDishka[TokenServicePort],
        active_only: bool = True
):
    """Получить мотоциклы пользователя (для админов/операторов или владельца)"""
    current_user = await get_current_user_dishka(request, token_service)

    # Проверяем права доступа
    if (current_user["role"].value > 1 and
            current_user["user_id"] != user_id):
        raise HTTPException(status_code=403, detail="Access denied")

    motorcycles = await controller.get_user_motorcycles(
        owner_id=user_id,
        active_only=active_only
    )
    return motorcycles


@router.get("/search", response_model=list[MotorcycleResponseSchema])
async def search_motorcycles(
        request: Request,
        controller: FromDishka[MotorcycleController],
        token_service: FromDishka[TokenServicePort],
        search_params: MotorcycleSearchSchema = Depends(),
):
    """Поиск мотоциклов с фильтрами"""
    await get_current_user_dishka(request, token_service)

    motorcycles = await controller.search_motorcycles(
        brand=search_params.brand,
        model=search_params.model,
        year_from=search_params.year_from,
        year_to=search_params.year_to,
        motorcycle_type=convert_enum_to_domain(search_params.motorcycle_type, DomainMotorcycleType),
        engine_type=convert_enum_to_domain(search_params.engine_type, DomainEngineType),
        engine_volume_from=search_params.engine_volume_from,
        engine_volume_to=search_params.engine_volume_to,
        power_from=search_params.power_from,
        power_to=search_params.power_to,
        active_only=search_params.active_only
    )
    return motorcycles


@router.get("/{motorcycle_id}", response_model=MotorcycleResponseSchema)
async def get_motorcycle(
        request: Request,
        motorcycle_id: UUID,
        controller: FromDishka[MotorcycleController],
        token_service: FromDishka[TokenServicePort]
):
    """Получить мотоцикл по ID"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        motorcycle = await controller.get_motorcycle_by_id(motorcycle_id)

        # Проверяем права доступа (владелец или админ/оператор)
        if (current_user["role"].value > 1 and
                str(current_user["user_id"]) != str(motorcycle["owner_id"])):
            raise HTTPException(status_code=403, detail="Access denied")

        return motorcycle
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


@router.put("/{motorcycle_id}", response_model=MotorcycleResponseSchema)
async def update_motorcycle(
        request: Request,
        motorcycle_id: UUID,
        dto: UpdateMotorcycleSchema,
        controller: FromDishka[MotorcycleController],
        token_service: FromDishka[TokenServicePort]
):
    """Обновить мотоцикл"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Сначала проверяем существование и права
        existing = await controller.get_motorcycle_by_id(motorcycle_id)

        # Проверяем права доступа
        if (current_user["role"].value > 1 and
                str(current_user["user_id"]) != str(existing["owner_id"])):
            raise HTTPException(status_code=403, detail="Access denied")

        # Обновляем
        motorcycle = await controller.update_motorcycle(
            motorcycle_id=motorcycle_id,
            brand=dto.brand,
            model=dto.model,
            year=dto.year,
            engine_volume=dto.engine_volume,
            engine_type=convert_enum_to_domain(dto.engine_type, DomainEngineType),
            motorcycle_type=convert_enum_to_domain(dto.motorcycle_type, DomainMotorcycleType),
            power=dto.power,
            mileage=dto.mileage,
            color=dto.color,
            description=dto.description,
            is_active=dto.is_active,
        )
        return motorcycle
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


@router.delete("/{motorcycle_id}", status_code=204)
async def delete_motorcycle(
        request: Request,
        motorcycle_id: UUID,
        controller: FromDishka[MotorcycleController],
        token_service: FromDishka[TokenServicePort]
):
    """Удалить мотоцикл"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Сначала проверяем существование и права
        existing = await controller.get_motorcycle_by_id(motorcycle_id)

        # Проверяем права доступа (только владелец или админ)
        if (current_user["role"] not in [UserRole.ADMIN] and
                str(current_user["user_id"]) != str(existing["owner_id"])):
            raise HTTPException(status_code=403, detail="Access denied")

        await controller.delete_motorcycle(motorcycle_id)
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex

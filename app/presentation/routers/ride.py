# app/presentation/routers/ride.py

from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Request

from app.application.controllers.motokonig_controller import MotoKonigController
from app.application.controllers.ride_controller import RideController
from app.domain.ports.services.token import TokenServicePort
from app.presentation.dependencies.auth import get_current_user_dishka
from app.presentation.schemas.ride import (
    CompleteRideSchema,
    CreateRideSchema,
    RateRideSchema,
    RideListItemSchema,
    RideResponseSchema,
)

router = APIRouter(route_class=DishkaRoute)


async def _get_current_motokonig_id(
        request: Request,
        motokonig_controller: MotoKonigController,
        token_service: TokenServicePort
) -> UUID:
    """Получить MotoKonig ID текущего пользователя"""
    current_user = await get_current_user_dishka(request, token_service)
    profile = await motokonig_controller.get_profile_by_user_id(current_user["user_id"])

    if not profile:
        raise HTTPException(
            status_code=400,
            detail="You need to create a MotoKonig profile first"
        )

    return profile.motokonig_id


@router.post("/", response_model=RideResponseSchema, status_code=201)
async def create_ride(
        request: Request,
        dto: CreateRideSchema,
        ride_controller: FromDishka[RideController],
        motokonig_controller: FromDishka[MotoKonigController],
        token_service: FromDishka[TokenServicePort]
):
    """Создать новую поездку"""
    motokonig_id = await _get_current_motokonig_id(request, motokonig_controller, token_service)

    try:
        ride = await ride_controller.create_ride(
            organizer_id=motokonig_id,
            title=dto.title,
            description=dto.description,
            difficulty=dto.difficulty,
            planned_distance=dto.planned_distance,
            max_participants=dto.max_participants,
            start_location=dto.start_location,
            end_location=dto.end_location,
            planned_start=dto.planned_start,
            planned_duration=dto.planned_duration,
            route_gpx=dto.route_gpx,
            is_public=dto.is_public,
        )

        # Добавляем nickname организатора
        organizer = await motokonig_controller.get_profile_by_id(ride.organizer_id)
        response = ride.to_dto()
        response["organizer_nickname"] = organizer.nickname if organizer else None
        response["current_participants"] = len(ride.participants)

        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/upcoming", response_model=list[RideListItemSchema])
async def get_upcoming_rides(
        ride_controller: FromDishka[RideController],
        motokonig_controller: FromDishka[MotoKonigController],
        limit: int = 10
):
    """Получить предстоящие поездки"""
    rides = await ride_controller.get_upcoming_rides(limit)

    result = []
    for ride in rides:
        organizer = await motokonig_controller.get_profile_by_id(ride.organizer_id)
        result.append(
            RideListItemSchema(
                ride_id=ride.ride_id,
                title=ride.title,
                difficulty=ride.difficulty,
                planned_distance=ride.planned_distance,
                start_location=ride.start_location,
                planned_start=ride.planned_start,
                current_participants=len(ride.participants),
                max_participants=ride.max_participants,
                is_completed=ride.is_completed,
                organizer_nickname=organizer.nickname if organizer else None,
            )
        )

    return result


@router.get("/{ride_id}", response_model=RideResponseSchema)
async def get_ride(
        ride_id: UUID,
        ride_controller: FromDishka[RideController],
        motokonig_controller: FromDishka[MotoKonigController]
):
    """Получить информацию о поездке"""
    ride = await ride_controller.get_ride_by_id(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    # Добавляем информацию об участниках
    response = ride.to_dto()
    organizer = await motokonig_controller.get_profile_by_id(ride.organizer_id)
    response["organizer_nickname"] = organizer.nickname if organizer else None
    response["current_participants"] = len(ride.participants)

    # Добавляем информацию о каждом участнике
    participants = []
    for p in ride.participants:
        profile = await motokonig_controller.get_profile_by_id(p.motokonig_id)
        if profile:
            participants.append({
                "motokonig_id": p.motokonig_id,
                "nickname": profile.nickname,
                "avatar_url": profile.avatar_url,
                "joined_at": p.joined_at,
                "is_leader": p.is_leader,
                "distance_covered": p.distance_covered,
                "average_speed": p.average_speed,
                "max_speed": p.max_speed,
            })
    response["participants"] = participants

    return response


@router.post("/{ride_id}/join", response_model=RideResponseSchema)
async def join_ride(
        request: Request,
        ride_id: UUID,
        ride_controller: FromDishka[RideController],
        motokonig_controller: FromDishka[MotoKonigController],
        token_service: FromDishka[TokenServicePort]
):
    """Присоединиться к поездке"""
    motokonig_id = await _get_current_motokonig_id(request, motokonig_controller, token_service)

    try:
        ride = await ride_controller.join_ride(ride_id, motokonig_id)

        response = ride.to_dto()
        response["current_participants"] = len(ride.participants)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/{ride_id}/leave", response_model=RideResponseSchema)
async def leave_ride(
        request: Request,
        ride_id: UUID,
        ride_controller: FromDishka[RideController],
        motokonig_controller: FromDishka[MotoKonigController],
        token_service: FromDishka[TokenServicePort]
):
    """Покинуть поездку"""
    motokonig_id = await _get_current_motokonig_id(request, motokonig_controller, token_service)

    try:
        ride = await ride_controller.leave_ride(ride_id, motokonig_id)

        response = ride.to_dto()
        response["current_participants"] = len(ride.participants)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/{ride_id}/start", response_model=RideResponseSchema)
async def start_ride(
        request: Request,
        ride_id: UUID,
        ride_controller: FromDishka[RideController],
        motokonig_controller: FromDishka[MotoKonigController],
        token_service: FromDishka[TokenServicePort]
):
    """Начать поездку (только для организатора)"""
    motokonig_id = await _get_current_motokonig_id(request, motokonig_controller, token_service)

    try:
        ride = await ride_controller.start_ride(ride_id, motokonig_id)
        return ride.to_dto()
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e


@router.post("/{ride_id}/complete", response_model=RideResponseSchema)
async def complete_ride(
        request: Request,
        ride_id: UUID,
        dto: CompleteRideSchema,
        ride_controller: FromDishka[RideController],
        motokonig_controller: FromDishka[MotoKonigController],
        token_service: FromDishka[TokenServicePort]
):
    """Завершить поездку (только для организатора)"""
    motokonig_id = await _get_current_motokonig_id(request, motokonig_controller, token_service)

    try:
        ride = await ride_controller.complete_ride(
            ride_id=ride_id,
            organizer_id=motokonig_id,
            actual_distance=dto.actual_distance,
            weather_conditions=dto.weather_conditions,
        )
        return ride.to_dto()
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e


@router.post("/{ride_id}/rate", response_model=RideResponseSchema)
async def rate_ride(
        request: Request,
        ride_id: UUID,
        dto: RateRideSchema,
        ride_controller: FromDishka[RideController],
        motokonig_controller: FromDishka[MotoKonigController],
        token_service: FromDishka[TokenServicePort]
):
    """Оценить поездку"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        ride = await ride_controller.rate_ride(
            ride_id=ride_id,
            user_id=current_user["user_id"],
            rating=dto.rating,
        )
        return ride.to_dto()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

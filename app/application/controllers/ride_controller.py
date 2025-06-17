# app/application/controllers/ride_controller.py

from datetime import datetime
from uuid import UUID

from app.application.use_cases.ride.complete_ride import CompleteRideUseCase
from app.application.use_cases.ride.create_ride import CreateRideUseCase
from app.application.use_cases.ride.join_ride import JoinRideUseCase
from app.domain.entities.ride import Ride
from app.domain.ports.repositories.ride import IRideRepository
from app.domain.value_objects.ride_difficulty import RideDifficulty
from app.infrastructure.specs.ride.ride_by_id import RideByIdSpec
from app.infrastructure.specs.ride.ride_by_organizer import RideByOrganizerSpec
from app.infrastructure.specs.ride.ride_upcoming import RideUpcomingSpec

__all__ = ["RideController"]


class RideController:
    """Контроллер для управления поездками"""

    def __init__(
            self,
            ride_repo: IRideRepository,
            create_ride_uc: CreateRideUseCase,
            join_ride_uc: JoinRideUseCase,
            complete_ride_uc: CompleteRideUseCase,
    ):
        self._ride_repo = ride_repo
        self._create_ride_uc = create_ride_uc
        self._join_ride_uc = join_ride_uc
        self._complete_ride_uc = complete_ride_uc

    async def create_ride(
            self,
            organizer_id: UUID,
            title: str,
            description: str | None,
            difficulty: RideDifficulty,
            planned_distance: int,
            max_participants: int,
            start_location: str,
            end_location: str | None,
            planned_start: datetime,
            planned_duration: int,
            route_gpx: str | None = None,
            is_public: bool = True,
    ) -> Ride:
        """Создать новую поездку"""
        return await self._create_ride_uc.execute(
            organizer_id=organizer_id,
            title=title,
            description=description,
            difficulty=difficulty,
            planned_distance=planned_distance,
            max_participants=max_participants,
            start_location=start_location,
            end_location=end_location,
            planned_start=planned_start,
            planned_duration=planned_duration,
            route_gpx=route_gpx,
            is_public=is_public,
        )

    async def get_ride_by_id(self, ride_id: UUID) -> Ride | None:
        """Получить поездку по ID"""
        return await self._ride_repo.get(RideByIdSpec(ride_id))

    async def get_upcoming_rides(self, limit: int = 10) -> list[Ride]:
        """Получить предстоящие поездки"""
        upcoming_rides =  await self._ride_repo.get_list(RideUpcomingSpec())
        return upcoming_rides[:limit]

    async def get_rides_by_organizer(self, organizer_id: UUID) -> list[Ride]:
        """Получить поездки организатора"""
        return await self._ride_repo.get_list(RideByOrganizerSpec(organizer_id))

    async def join_ride(
            self,
            ride_id: UUID,
            motokonig_id: UUID,
    ) -> Ride:
        """Присоединиться к поездке"""
        return await self._join_ride_uc.execute(
            ride_id=ride_id,
            motokonig_id=motokonig_id,
        )

    async def leave_ride(
            self,
            ride_id: UUID,
            motokonig_id: UUID,
    ) -> Ride:
        """Покинуть поездку"""
        ride = await self.get_ride_by_id(ride_id)
        if not ride:
            raise ValueError("Ride not found")

        ride.remove_participant(motokonig_id)
        return await self._ride_repo.update(ride)

    async def start_ride(
            self,
            ride_id: UUID,
            organizer_id: UUID,
    ) -> Ride:
        """Начать поездку"""
        ride = await self.get_ride_by_id(ride_id)
        if not ride:
            raise ValueError("Ride not found")

        if ride.organizer_id != organizer_id:
            raise ValueError("Only organizer can start the ride")

        ride.start_ride()
        return await self._ride_repo.update(ride)

    async def complete_ride(
            self,
            ride_id: UUID,
            organizer_id: UUID,
            actual_distance: int,
            weather_conditions: str | None = None,
    ) -> Ride:
        """Завершить поездку"""
        return await self._complete_ride_uc.execute(
            ride_id=ride_id,
            organizer_id=organizer_id,
            actual_distance=actual_distance,
            weather_conditions=weather_conditions,
        )

    async def rate_ride(
            self,
            ride_id: UUID,
            user_id: UUID,
            rating: float,
    ) -> Ride:
        """Оценить поездку"""
        ride = await self.get_ride_by_id(ride_id)
        if not ride:
            raise ValueError("Ride not found")

        # Проверяем, что пользователь был участником
        participant_ids = [p.motokonig_id for p in ride.participants]  # noqa: F841
        # TODO: получить motokonig_id по user_id

        ride.rate_ride(rating)
        return await self._ride_repo.update(ride)

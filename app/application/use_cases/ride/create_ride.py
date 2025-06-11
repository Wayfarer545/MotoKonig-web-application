# app/application/use_cases/ride/create_ride.py

from datetime import datetime
from uuid import UUID

from app.domain.entities.ride import Ride
from app.domain.ports.repositories.motokonig import IMotoKonigRepository
from app.domain.ports.repositories.ride import IRideRepository
from app.domain.value_objects.ride_difficulty import RideDifficulty

__all__ = ["CreateRideUseCase"]


class CreateRideUseCase:
    """Use case для создания поездки"""

    def __init__(
            self,
            ride_repo: IRideRepository,
            motokonig_repo: IMotoKonigRepository,
    ):
        self._ride_repo = ride_repo
        self._motokonig_repo = motokonig_repo

    async def execute(
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

        # Проверяем, что организатор существует
        organizer = await self._motokonig_repo.get_by_id(organizer_id)
        if not organizer:
            raise ValueError("Organizer profile not found")

        # Создаём поездку
        ride = Ride(
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

        # Автоматически добавляем организатора как участника
        ride.add_participant(organizer_id, is_leader=True)

        # Сохраняем
        return await self._ride_repo.add(ride)

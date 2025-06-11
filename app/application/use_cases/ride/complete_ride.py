# app/application/use_cases/ride/complete_ride.py

from uuid import UUID

from app.domain.entities.ride import Ride
from app.domain.ports.repositories.ride import IRideRepository
from app.application.use_cases.motokonig.update_ride_stats import UpdateRideStatsUseCase

__all__ = ["CompleteRideUseCase"]


class CompleteRideUseCase:
    """Use case для завершения поездки"""

    def __init__(
            self,
            ride_repo: IRideRepository,
            update_stats_uc: UpdateRideStatsUseCase,
    ):
        self._ride_repo = ride_repo
        self._update_stats_uc = update_stats_uc

    async def execute(
            self,
            ride_id: UUID,
            organizer_id: UUID,
            actual_distance: int,
            weather_conditions: str | None = None,
    ) -> Ride:
        """Завершить поездку и обновить статистику участников"""

        # Получаем поездку
        ride = await self._ride_repo.get_by_id(ride_id)
        if not ride:
            raise ValueError("Ride not found")

        # Проверяем, что завершает организатор
        if ride.organizer_id != organizer_id:
            raise ValueError("Only organizer can complete the ride")

        # Завершаем поездку
        ride.complete_ride(actual_distance, weather_conditions)

        # Обновляем статистику для всех участников
        if ride.actual_start and ride.actual_end:
            duration = int((ride.actual_end - ride.actual_start).total_seconds() / 60)

            for participant in ride.participants:
                if participant.left_at is None:  # Только для тех, кто доехал
                    # Рассчитываем индивидуальные показатели
                    participant_distance = participant.distance_covered or actual_distance
                    participant_max_speed = participant.max_speed or 100.0

                    await self._update_stats_uc.execute(
                        motokonig_id=participant.motokonig_id,
                        distance=participant_distance,
                        duration=duration,
                        max_speed=participant_max_speed,
                    )

        # Сохраняем поездку
        return await self._ride_repo.update(ride)
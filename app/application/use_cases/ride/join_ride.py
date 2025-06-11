# app/application/use_cases/ride/join_ride.py

from uuid import UUID

from app.domain.entities.ride import Ride
from app.domain.ports.repositories.motokonig import IMotoKonigRepository
from app.domain.ports.repositories.ride import IRideRepository

__all__ = ["JoinRideUseCase"]


class JoinRideUseCase:
    """Use case для присоединения к поездке"""

    def __init__(
            self,
            ride_repo: IRideRepository,
            motokonig_repo: IMotoKonigRepository,
    ):
        self._ride_repo = ride_repo
        self._motokonig_repo = motokonig_repo

    async def execute(
            self,
            ride_id: UUID,
            motokonig_id: UUID,
    ) -> Ride:
        """Присоединиться к поездке"""

        # Получаем поездку
        ride = await self._ride_repo.get_by_id(ride_id)
        if not ride:
            raise ValueError("Ride not found")

        # Проверяем профиль участника
        participant = await self._motokonig_repo.get_by_id(motokonig_id)
        if not participant:
            raise ValueError("MotoKonig profile not found")

        # Проверяем публичность поездки
        if not ride.is_public and not participant.is_public:
            raise ValueError("Cannot join private ride with private profile")

        # Добавляем участника
        ride.add_participant(motokonig_id)

        # Сохраняем
        return await self._ride_repo.update(ride)


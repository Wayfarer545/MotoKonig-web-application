# app/application/use_cases/motokonig/get_top_riders.py

from app.domain.entities.motokonig import MotoKonig
from app.domain.ports.repositories.motokonig import IMotoKonigRepository
from app.infrastructure.specs.motokonig.motokonig_public import MotoKonigPublic

__all__ = ["GetTopRidersUseCase"]


class GetTopRidersUseCase:
    """Use case для получения топ-райдеров"""

    def __init__(self, motokonig_repo: IMotoKonigRepository):
        self._motokonig_repo = motokonig_repo

    async def execute(self, limit: int = 10) -> list[MotoKonig]:
        """Получить топ публичных профилей по рейтингу"""

        # Получаем публичные профили
        public_profiles = await self._motokonig_repo.get_list(
            MotoKonigPublic()
        )

        # Сортируем по рейтингу и опыту
        sorted_profiles = sorted(
            public_profiles,
            key=lambda x: (x.rating, x.experience_points),
            reverse=True
        )

        return sorted_profiles[:limit]

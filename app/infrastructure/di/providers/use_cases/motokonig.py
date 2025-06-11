# app/infrastructure/di/providers/use_cases/motokonig.py

from dishka import Provider, Scope, provide

from app.application.use_cases.motokonig.create_profile import (
    CreateMotoKonigProfileUseCase,
)
from app.application.use_cases.motokonig.get_top_riders import GetTopRidersUseCase
from app.application.use_cases.motokonig.update_ride_stats import UpdateRideStatsUseCase
from app.domain.ports.repositories.motokonig import IMotoKonigRepository
from app.domain.ports.repositories.user import IUserRepository

__all__ = ["MotoKonigUseCaseProvider"]


class MotoKonigUseCaseProvider(Provider):
    """DI провайдер для MotoKonig use cases"""

    @provide(scope=Scope.REQUEST)
    def provide_create_profile_uc(
            self,
            motokonig_repo: IMotoKonigRepository,
            user_repo: IUserRepository,
    ) -> CreateMotoKonigProfileUseCase:
        return CreateMotoKonigProfileUseCase(motokonig_repo, user_repo)

    @provide(scope=Scope.REQUEST)
    def provide_update_stats_uc(
            self,
            motokonig_repo: IMotoKonigRepository,
    ) -> UpdateRideStatsUseCase:
        return UpdateRideStatsUseCase(motokonig_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_top_riders_uc(
            self,
            motokonig_repo: IMotoKonigRepository,
    ) -> GetTopRidersUseCase:
        return GetTopRidersUseCase(motokonig_repo)


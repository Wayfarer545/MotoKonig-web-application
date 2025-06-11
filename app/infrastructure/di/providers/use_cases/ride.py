# app/infrastructure/di/providers/use_cases/ride.py

from dishka import Provider, Scope, provide

__all__ = ["RideUseCaseProvider"]

from app.application.use_cases.motokonig.update_ride_stats import UpdateRideStatsUseCase

from app.application.use_cases.ride.complete_ride import CompleteRideUseCase
from app.application.use_cases.ride.create_ride import CreateRideUseCase
from app.application.use_cases.ride.join_ride import JoinRideUseCase
from app.domain.ports.repositories.motokonig import IMotoKonigRepository
from app.domain.ports.repositories.ride import IRideRepository


class RideUseCaseProvider(Provider):
    """DI провайдер для MotoKonig use cases"""

    @provide(scope=Scope.REQUEST)
    def provide_create_ride_uc(
            self,
            ride_repo: IRideRepository,
            motokonig_repo: IMotoKonigRepository,
    ) -> CreateRideUseCase:
        return CreateRideUseCase(ride_repo, motokonig_repo)

    @provide(scope=Scope.REQUEST)
    def provide_join_ride_uc(
            self,
            ride_repo: IRideRepository,
            motokonig_repo: IMotoKonigRepository,
    ) -> JoinRideUseCase:
        return JoinRideUseCase(ride_repo, motokonig_repo)

    @provide(scope=Scope.REQUEST)
    def provide_complete_ride_uc(
            self,
            ride_repo: IRideRepository,
            update_stats_uc: UpdateRideStatsUseCase,
    ) -> CompleteRideUseCase:
        return CompleteRideUseCase(ride_repo, update_stats_uc)

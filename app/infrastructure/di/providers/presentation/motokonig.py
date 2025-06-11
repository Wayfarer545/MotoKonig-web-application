# app/infrastructure/di/providers/presentation/motokonig.py

from dishka import Provider, Scope, provide

from app.application.controllers.motokonig_controller import MotoKonigController
from app.application.controllers.ride_controller import RideController
from app.application.use_cases.motokonig.create_profile import (
    CreateMotoKonigProfileUseCase,
)
from app.application.use_cases.motokonig.get_top_riders import GetTopRidersUseCase
from app.application.use_cases.motokonig.update_ride_stats import UpdateRideStatsUseCase
from app.application.use_cases.ride.complete_ride import CompleteRideUseCase
from app.application.use_cases.ride.create_ride import CreateRideUseCase
from app.application.use_cases.ride.join_ride import JoinRideUseCase
from app.domain.ports.repositories.motokonig import IMotoKonigRepository
from app.domain.ports.repositories.ride import IRideRepository

__all__ = ["MotoKonigControllerProvider"]


class MotoKonigControllerProvider(Provider):
    """DI провайдер для контроллеров MotoKonig"""

    @provide(scope=Scope.REQUEST)
    def provide_motokonig_controller(
            self,
            motokonig_repo: IMotoKonigRepository,
            create_profile_uc: CreateMotoKonigProfileUseCase,
            update_stats_uc: UpdateRideStatsUseCase,
            get_top_riders_uc: GetTopRidersUseCase,
    ) -> MotoKonigController:
        return MotoKonigController(
            motokonig_repo=motokonig_repo,
            create_profile_uc=create_profile_uc,
            update_stats_uc=update_stats_uc,
            get_top_riders_uc=get_top_riders_uc,
        )

    @provide(scope=Scope.REQUEST)
    def provide_ride_controller(
            self,
            ride_repo: IRideRepository,
            create_ride_uc: CreateRideUseCase,
            join_ride_uc: JoinRideUseCase,
            complete_ride_uc: CompleteRideUseCase,
    ) -> RideController:
        return RideController(
            ride_repo=ride_repo,
            create_ride_uc=create_ride_uc,
            join_ride_uc=join_ride_uc,
            complete_ride_uc=complete_ride_uc,
        )

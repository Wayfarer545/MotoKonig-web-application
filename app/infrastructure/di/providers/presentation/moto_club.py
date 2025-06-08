# app/infrastructure/di/providers/presentation/moto_club.py

from dishka import Provider, Scope, provide

from app.application.controllers.motoclub_controller import MotoClubController
from app.application.use_cases.club_invitation.invite_user import (
    InviteUserToClubUseCase,
)
from app.application.use_cases.club_membership.join_club import JoinClubUseCase
from app.application.use_cases.moto_club.create_club import CreateMotoClubUseCase
from app.application.use_cases.moto_club.delete_club import DeleteMotoClubUseCase
from app.application.use_cases.moto_club.get_club import GetMotoClubUseCase
from app.application.use_cases.moto_club.list_clubs import ListMotoClubsUseCase
from app.application.use_cases.moto_club.update_club import UpdateMotoClubUseCase


class MotoClubControllerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_moto_club_controller(
        self,
        create_uc: CreateMotoClubUseCase,
        get_uc: GetMotoClubUseCase,
        list_uc: ListMotoClubsUseCase,
        update_uc: UpdateMotoClubUseCase,
        delete_uc: DeleteMotoClubUseCase,
        join_uc: JoinClubUseCase,
        invite_uc: InviteUserToClubUseCase,
    ) -> MotoClubController:
        return MotoClubController(
            create_uc,
            get_uc,
            list_uc,
            update_uc,
            delete_uc,
            join_uc,
            invite_uc,
        )

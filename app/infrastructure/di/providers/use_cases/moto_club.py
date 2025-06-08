from dishka import Provider, Scope, provide

from app.application.use_cases.moto_club.create_club import CreateMotoClubUseCase
from app.application.use_cases.moto_club.delete_club import DeleteMotoClubUseCase
from app.application.use_cases.moto_club.get_club import GetMotoClubUseCase
from app.application.use_cases.moto_club.list_clubs import ListMotoClubsUseCase
from app.application.use_cases.moto_club.update_club import UpdateMotoClubUseCase
from app.domain.ports.repositories.club_membership import IClubMembershipRepository
from app.domain.ports.repositories.moto_club import IMotoClubRepository


class MotoClubUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_create_moto_club_uc(
        self,
        club_repo: IMotoClubRepository,
        membership_repo: IClubMembershipRepository,
    ) -> CreateMotoClubUseCase:
        return CreateMotoClubUseCase(club_repo, membership_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_moto_club_uc(self, repo: IMotoClubRepository) -> GetMotoClubUseCase:
        return GetMotoClubUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_list_moto_clubs_uc(self, repo: IMotoClubRepository) -> ListMotoClubsUseCase:
        return ListMotoClubsUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_update_moto_club_uc(self, repo: IMotoClubRepository) -> UpdateMotoClubUseCase:
        return UpdateMotoClubUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_delete_moto_club_uc(self, repo: IMotoClubRepository) -> DeleteMotoClubUseCase:
        return DeleteMotoClubUseCase(repo)

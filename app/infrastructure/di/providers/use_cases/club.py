from dishka import Provider, Scope, provide

from app.application.use_cases.club_invitation.invite_user import (
    InviteUserToClubUseCase,
)
from app.application.use_cases.club_membership.join_club import JoinClubUseCase
from app.domain.ports.repositories.club_invitation import IClubInvitationRepository
from app.domain.ports.repositories.club_membership import IClubMembershipRepository
from app.domain.ports.repositories.moto_club import IMotoClubRepository


class ClubUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_join_club_uc(
        self,
        club_repo: IMotoClubRepository,
        membership_repo: IClubMembershipRepository,
    ) -> JoinClubUseCase:
        return JoinClubUseCase(club_repo, membership_repo)

    @provide(scope=Scope.REQUEST)
    def provide_invite_user_uc(
        self,
        club_repo: IMotoClubRepository,
        membership_repo: IClubMembershipRepository,
        invitation_repo: IClubInvitationRepository,
    ) -> InviteUserToClubUseCase:
        return InviteUserToClubUseCase(club_repo, membership_repo, invitation_repo)

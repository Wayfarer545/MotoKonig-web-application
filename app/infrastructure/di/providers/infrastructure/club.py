# app/infrastructure/di/providers/infrastructure/club.py

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.repositories.club_invitation import IClubInvitationRepository
from app.domain.ports.repositories.club_membership import IClubMembershipRepository
from app.infrastructure.repositories.sql_club_invitation_repo import (
    SqlClubInvitationRepository,
)
from app.infrastructure.repositories.sql_club_membership_repo import (
    SqlClubMembershipRepository,
)


class ClubRepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_club_membership_repo(self, session: AsyncSession) -> IClubMembershipRepository:
        return SqlClubMembershipRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_club_invitation_repo(self, session: AsyncSession) -> IClubInvitationRepository:
        return SqlClubInvitationRepository(session)

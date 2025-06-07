# app/infrastructure/di/providers/use_cases.py

from dishka import Provider, Scope, provide

from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.logout import LogoutUseCase
from app.application.use_cases.auth.pin_auth import PinAuthUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.application.use_cases.auth.register import RegisterUseCase
from app.application.use_cases.club_invitation.invite_user import (
    InviteUserToClubUseCase,
)
from app.application.use_cases.club_membership.join_club import JoinClubUseCase
from app.application.use_cases.media.delete_file import DeleteFileUseCase
from app.application.use_cases.media.get_presigned_url import GetPresignedUrlUseCase
from app.application.use_cases.media.upload_file import UploadFileUseCase
from app.application.use_cases.moto_club.create_club import CreateMotoClubUseCase
from app.application.use_cases.moto_club.delete_club import DeleteMotoClubUseCase
from app.application.use_cases.moto_club.get_club import GetMotoClubUseCase
from app.application.use_cases.moto_club.list_clubs import ListMotoClubsUseCase
from app.application.use_cases.moto_club.update_club import UpdateMotoClubUseCase
from app.application.use_cases.motorcycle.create_motorcycle import (
    CreateMotorcycleUseCase,
)
from app.application.use_cases.motorcycle.delete_motorcycle import (
    DeleteMotorcycleUseCase,
)
from app.application.use_cases.motorcycle.get_motorcycle import GetMotorcycleUseCase
from app.application.use_cases.motorcycle.list_motorcycles import ListMotorcyclesUseCase
from app.application.use_cases.motorcycle.update_motorcycle import (
    UpdateMotorcycleUseCase,
)
from app.application.use_cases.profile.create_profile import CreateProfileUseCase
from app.application.use_cases.profile.delete_profile import DeleteProfileUseCase
from app.application.use_cases.profile.get_profile import GetProfileUseCase
from app.application.use_cases.profile.update_profile import UpdateProfileUseCase
from app.application.use_cases.social_link.add_social_link import AddSocialLinkUseCase
from app.application.use_cases.social_link.get_profile_social_links import (
    GetProfileSocialLinksUseCase,
)
from app.application.use_cases.social_link.remove_social_link import (
    RemoveSocialLinkUseCase,
)
from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.delete_user import DeleteUserUseCase
from app.application.use_cases.user.get_user import GetUserUseCase
from app.application.use_cases.user.list_users import ListUsersUseCase
from app.application.use_cases.user.update_user import UpdateUserUseCase
from app.domain.ports.epositories.club_invitation_repository import (
    IClubInvitationRepository,
)
from app.domain.ports.epositories.club_membership_repository import (
    IClubMembershipRepository,
)
from app.domain.ports.epositories.media_file_repository import IMediaFileRepository
from app.domain.ports.epositories.moto_club_repository import IMotoClubRepository
from app.domain.ports.epositories.motorcycle_repository import IMotorcycleRepository
from app.domain.ports.epositories.profile_repository import IProfileRepository
from app.domain.ports.epositories.social_link_repository import ISocialLinkRepository
from app.domain.ports.epositories.user_repository import IUserRepository
from app.domain.ports.file_storage import FileStoragePort
from app.domain.ports.pin_storage import PinStoragePort
from app.domain.ports.services.password_service import PasswordService
from app.domain.ports.services.token_service import TokenServicePort


class UseCaseProvider(Provider):
    # User Use Cases
    @provide(scope=Scope.REQUEST)
    def provide_list_users_uc(self, repo: IUserRepository) -> ListUsersUseCase:
        return ListUsersUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_user_uc(self, repo: IUserRepository) -> GetUserUseCase:
        return GetUserUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_create_user_uc(self, repo: IUserRepository, pwd_service: PasswordService) -> CreateUserUseCase:
        return CreateUserUseCase(repo, pwd_service)

    @provide(scope=Scope.REQUEST)
    def provide_update_user_uc(self, repo: IUserRepository, pwd_service: PasswordService) -> UpdateUserUseCase:
        return UpdateUserUseCase(repo, pwd_service)

    @provide(scope=Scope.REQUEST)
    def provide_delete_user_uc(self, repo: IUserRepository) -> DeleteUserUseCase:
        return DeleteUserUseCase(repo)

    # Motorcycle Use Cases
    @provide(scope=Scope.REQUEST)
    def provide_list_motorcycles_uc(self, repo: IMotorcycleRepository) -> ListMotorcyclesUseCase:
        return ListMotorcyclesUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_motorcycle_uc(self, repo: IMotorcycleRepository) -> GetMotorcycleUseCase:
        return GetMotorcycleUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_create_motorcycle_uc(self, repo: IMotorcycleRepository) -> CreateMotorcycleUseCase:
        return CreateMotorcycleUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_update_motorcycle_uc(self, repo: IMotorcycleRepository) -> UpdateMotorcycleUseCase:
        return UpdateMotorcycleUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_delete_motorcycle_uc(self, repo: IMotorcycleRepository) -> DeleteMotorcycleUseCase:
        return DeleteMotorcycleUseCase(repo)

    # Auth Use Cases
    @provide(scope=Scope.REQUEST)
    def provide_login_uc(self, repo: IUserRepository, pwd_service: PasswordService, token_service: TokenServicePort) -> LoginUseCase:
        return LoginUseCase(repo, pwd_service, token_service)

    @provide(scope=Scope.REQUEST)
    def provide_logout_uc(self, token_service: TokenServicePort) -> LogoutUseCase:
        return LogoutUseCase(token_service)

    @provide(scope=Scope.REQUEST)
    def provide_refresh_uc(self, token_service: TokenServicePort, repo: IUserRepository) -> RefreshTokenUseCase:
        return RefreshTokenUseCase(token_service, repo)

    @provide(scope=Scope.REQUEST)
    def provide_register_uc(self, repo: IUserRepository, pwd_service: PasswordService) -> RegisterUseCase:
        return RegisterUseCase(repo, pwd_service)

    @provide(scope=Scope.REQUEST)
    def provide_pin_auth_uc(self, user_repo: IUserRepository, token_service: TokenServicePort, pin_storage: PinStoragePort) -> PinAuthUseCase:
        return PinAuthUseCase(user_repo, token_service, pin_storage)

    # Profile Use Cases
    @provide(scope=Scope.REQUEST)
    def provide_create_profile_uc(self, repo: IProfileRepository) -> CreateProfileUseCase:
        return CreateProfileUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_profile_uc(self, repo: IProfileRepository) -> GetProfileUseCase:
        return GetProfileUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_update_profile_uc(self, repo: IProfileRepository) -> UpdateProfileUseCase:
        return UpdateProfileUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_delete_profile_uc(self, repo: IProfileRepository) -> DeleteProfileUseCase:
        return DeleteProfileUseCase(repo)

    # Social Link Use Cases
    @provide(scope=Scope.REQUEST)
    def provide_add_social_link_uc(self, repo: ISocialLinkRepository) -> AddSocialLinkUseCase:
        return AddSocialLinkUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_remove_social_link_uc(self, repo: ISocialLinkRepository) -> RemoveSocialLinkUseCase:
        return RemoveSocialLinkUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_social_links_uc(self, repo: ISocialLinkRepository) -> GetProfileSocialLinksUseCase:
        return GetProfileSocialLinksUseCase(repo)

    # Media Use Cases
    @provide(scope=Scope.REQUEST)
    def provide_upload_file_uc(self, file_storage: FileStoragePort, media_repo: IMediaFileRepository) -> UploadFileUseCase:
        return UploadFileUseCase(file_storage, media_repo)

    @provide(scope=Scope.REQUEST)
    def provide_delete_file_uc(self, file_storage: FileStoragePort, media_repo: IMediaFileRepository) -> DeleteFileUseCase:
        return DeleteFileUseCase(file_storage, media_repo)

    @provide(scope=Scope.REQUEST)
    def provide_presigned_url_uc(self, file_storage: FileStoragePort, media_repo: IMediaFileRepository) -> GetPresignedUrlUseCase:
        return GetPresignedUrlUseCase(file_storage, media_repo)

    # MotoClub Use Cases
    @provide(scope=Scope.REQUEST)
    def provide_create_moto_club_uc(
            self,
            club_repo: IMotoClubRepository,
            membership_repo: IClubMembershipRepository
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

    # Club Membership Use Cases
    @provide(scope=Scope.REQUEST)
    def provide_join_club_uc(
            self,
            club_repo: IMotoClubRepository,
            membership_repo: IClubMembershipRepository
    ) -> JoinClubUseCase:
        return JoinClubUseCase(club_repo, membership_repo)

    # Club Invitation Use Cases
    @provide(scope=Scope.REQUEST)
    def provide_invite_user_uc(
            self,
            club_repo: IMotoClubRepository,
            membership_repo: IClubMembershipRepository,
            invitation_repo: IClubInvitationRepository
    ) -> InviteUserToClubUseCase:
        return InviteUserToClubUseCase(club_repo, membership_repo, invitation_repo)

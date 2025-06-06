# app/infrastructure/di/providers/presentation.py

from dishka import Provider, Scope, provide

from app.application.controllers.auth_controller import AuthController
from app.application.controllers.media_controller import MediaController
from app.application.controllers.moto_club_controller import MotoClubController
from app.application.controllers.motorcycle_controller import MotorcycleController
from app.application.controllers.profile_controller import ProfileController
from app.application.controllers.user_controller import UserController
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


class PresentationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_user_controller(
        self,
        list_uc: ListUsersUseCase,
        get_uc: GetUserUseCase,
        create_uc: CreateUserUseCase,
        update_uc: UpdateUserUseCase,
        delete_uc: DeleteUserUseCase,
    ) -> UserController:
        return UserController(list_uc, get_uc, create_uc, update_uc, delete_uc)

    @provide(scope=Scope.REQUEST)
    def provide_motorcycle_controller(
        self,
        list_uc: ListMotorcyclesUseCase,
        get_uc: GetMotorcycleUseCase,
        create_uc: CreateMotorcycleUseCase,
        update_uc: UpdateMotorcycleUseCase,
        delete_uc: DeleteMotorcycleUseCase,
    ) -> MotorcycleController:
        return MotorcycleController(list_uc, get_uc, create_uc, update_uc, delete_uc)

    @provide(scope=Scope.REQUEST)
    def provide_auth_controller(
        self,
        login_uc: LoginUseCase,
        logout_uc: LogoutUseCase,
        refresh_uc: RefreshTokenUseCase,
        register_uc: RegisterUseCase,
        pin_auth_uc: PinAuthUseCase,
    ) -> AuthController:
        return AuthController(login_uc, logout_uc, refresh_uc, register_uc, pin_auth_uc)

    @provide(scope=Scope.REQUEST)
    def provide_profile_controller(
            self,
            create_profile_uc: CreateProfileUseCase,
            get_profile_uc: GetProfileUseCase,
            update_profile_uc: UpdateProfileUseCase,
            delete_profile_uc: DeleteProfileUseCase,
            add_social_link_uc: AddSocialLinkUseCase,
            remove_social_link_uc: RemoveSocialLinkUseCase,
            get_social_links_uc: GetProfileSocialLinksUseCase,
    ) -> ProfileController:
        return ProfileController(
            create_profile_uc,
            get_profile_uc,
            update_profile_uc,
            delete_profile_uc,
            add_social_link_uc,
            remove_social_link_uc,
            get_social_links_uc,
        )

    @provide(scope=Scope.REQUEST)
    def provide_media_controller(
            self,
            upload_uc: UploadFileUseCase,
            delete_uc: DeleteFileUseCase,
            presigned_url_uc: GetPresignedUrlUseCase,
    ) -> MediaController:
        return MediaController(upload_uc, delete_uc, presigned_url_uc)

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
            create_uc, get_uc, list_uc, update_uc, delete_uc, join_uc, invite_uc
        )

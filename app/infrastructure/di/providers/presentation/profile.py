# app/infrastructure/di/providers/presentation/profile.py

from dishka import Provider, Scope, provide

from app.application.controllers.profile_controller import ProfileController
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


class ProfileControllerProvider(Provider):
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

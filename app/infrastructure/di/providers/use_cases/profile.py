from dishka import Provider, Scope, provide

from app.application.use_cases.profile.create_profile import CreateProfileUseCase
from app.application.use_cases.profile.delete_profile import DeleteProfileUseCase
from app.application.use_cases.profile.get_profile import GetProfileUseCase
from app.application.use_cases.profile.update_profile import UpdateProfileUseCase
from app.domain.ports.repositories.profile import IProfileRepository


class ProfileUseCaseProvider(Provider):
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

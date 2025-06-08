from dishka import Provider, Scope, provide

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
from app.domain.ports.repositories.motorcycle import IMotorcycleRepository


class MotorcycleUseCaseProvider(Provider):
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

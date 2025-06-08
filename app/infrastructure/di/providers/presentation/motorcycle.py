# app/infrastructure/di/providers/presentation/motorcycle.py

from dishka import Provider, Scope, provide

from app.application.controllers.motorcycle_controller import MotorcycleController
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


class MotorcycleControllerProvider(Provider):
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

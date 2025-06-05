# app/application/controllers/user_controller.py

from uuid import UUID

from app.application.exceptions import NotFoundError
from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.delete_user import DeleteUserUseCase
from app.application.use_cases.user.get_user import GetUserUseCase
from app.application.use_cases.user.list_users import ListUsersUseCase
from app.application.use_cases.user.update_user import UpdateUserUseCase
from app.domain.entities.user import User, UserRole
from app.infrastructure.specs.user.user_by_id import UserById


class UserController:
    def __init__(
        self,
        list_uc: ListUsersUseCase,
        get_uc: GetUserUseCase,
        create_uc: CreateUserUseCase,
        update_uc: UpdateUserUseCase,
        delete_uc: DeleteUserUseCase,
    ):
        self.list_uc = list_uc
        self.get_uc = get_uc
        self.create_uc = create_uc
        self.update_uc = update_uc
        self.delete_uc = delete_uc

    async def list_users(self) -> list[User]:
        return await self.list_uc.execute()

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        spec = UserById(user_id=user_id)
        result = await self.get_uc.execute(spec)
        return result.to_dto() if result else None

    async def create(self, username: str, password: str, role: UserRole) -> User:
        return await self.create_uc.execute(username, password, role)

    async def update_user(
        self,
        user_id: UUID,
        username: str | None,
        password: str | None,
        role: UserRole | None,
        deactivate: bool = False,
    ) -> User | None:
        updated = await self.update_uc.execute(
            user_id,
            new_username=username,
            new_password=password,
            new_role=role,
            deactivate=deactivate,
        )
        if updated is None:
            raise NotFoundError("User not found")
        return updated

    async def delete_user(self, user_id: UUID) -> None:
        ok = await self.delete_uc.execute(user_id)
        if not ok:
            raise NotFoundError("User not found")

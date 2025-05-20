# app/application/controllers/user_controller.py

from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status

from app.application.use_cases.user.list_users import ListUsersUseCase
from app.application.use_cases.user.get_user import GetUserUseCase
from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.update_user import UpdateUserUseCase
from app.application.use_cases.user.delete_user import DeleteUserUseCase
from app.domain.entities.user import User, UserRole


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

    async def list_users(self) -> List[User]:
        return await self.list_uc.execute()

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.get_uc.execute(user_id)

    async def create(self, username: str, password: str, role: UserRole) -> User:
        return await self.create_uc.execute(username, password, role)

    async def update_user(
        self,
        user_id: UUID,
        username: Optional[str],
        password: Optional[str],
        role: Optional[UserRole],
        deactivate: bool = False,
    ) -> Optional[User]:
        updated = await self.update_uc.execute(
            user_id,
            new_username=username,
            new_password=password,
            new_role=role,
            deactivate=deactivate,
        )
        if updated is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated

    async def delete_user(self, user_id: UUID) -> None:
        ok = await self.delete_uc.execute(user_id)
        if not ok:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

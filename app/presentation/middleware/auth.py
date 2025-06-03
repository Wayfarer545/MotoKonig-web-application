# app/presentation/middleware/auth.py

from typing import Optional, List, Dict, Any
from uuid import UUID

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from dishka import AsyncContainer
from dishka.integrations.fastapi import FromDishka

from app.domain.ports.token_service import TokenServicePort
from app.domain.entities.user import UserRole


class JWTBearer(HTTPBearer):
    """JWT Bearer authentication"""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme"
                )

            # Получаем токен-сервис из DI контейнера
            container: AsyncContainer = request.scope.get("dishka_container")
            if not container:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="DI container not found"
                )

            async with container() as di_context:
                token_service = await di_context.get(TokenServicePort)

                # Проверяем токен
                if not await self.verify_jwt(credentials.credentials, token_service):
                    raise HTTPException(
                        status_code=HTTP_403_FORBIDDEN,
                        detail="Invalid or expired token"
                    )

            return credentials.credentials
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Invalid authorization code"
            )

    async def verify_jwt(self, token: str, token_service: TokenServicePort) -> bool:
        """Проверить JWT токен"""
        try:
            # Проверяем blacklist
            if await token_service.is_token_blacklisted(token):
                return False

            # Декодируем токен
            payload = await token_service.decode_token(token)

            # Проверяем тип токена
            if payload.get("type") != "access":
                return False

            return True
        except Exception:
            return False


# Dependency для получения текущего пользователя
async def get_current_user(
        token: str = Depends(JWTBearer()),
        token_service: FromDishka[TokenServicePort] = None
) -> Dict[str, Any]:
    """Получить данные текущего пользователя из токена"""
    try:
        payload = await token_service.decode_token(token)
        return {
            "user_id": UUID(payload["sub"]),
            "username": payload["username"],
            "role": UserRole[payload["role"]]
        }
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


# Декоратор для проверки ролей
def require_role(allowed_roles: List[UserRole]):
    """Декоратор для проверки ролей пользователя"""

    async def role_checker(
            current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        user_role = current_user["role"]
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user

    return role_checker


# Shortcuts для частых проверок
require_admin = require_role([UserRole.ADMIN])
require_operator = require_role([UserRole.ADMIN, UserRole.OPERATOR])
require_authenticated = require_role([UserRole.ADMIN, UserRole.OPERATOR, UserRole.USER])
# app/presentation/middleware/auth.py

from typing import Any
from uuid import UUID

import structlog
from dishka.integrations.fastapi import FromDishka
from fastapi import HTTPException, Request
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from app.domain.entities.user import UserRole
from app.domain.ports.services.token import TokenServicePort


async def get_token_from_header(request: Request) -> str | None:
    """Извлечь токен из заголовка Authorization"""
    authorization = request.headers.get("Authorization")
    if not authorization:
        return None

    scheme, token = get_authorization_scheme_param(authorization)
    if scheme.lower() != "bearer":
        return None

    return token


async def get_current_user_dishka(
        request: Request,
        token_service: FromDishka[TokenServicePort]
) -> dict[str, Any]:
    """Получить текущего пользователя используя только Dishka"""
    token = await get_token_from_header(request)
    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Проверяем blacklist
        if await token_service.is_token_blacklisted(token):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Token is blacklisted",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Декодируем токен
        payload = await token_service.decode_token(token)

        # Проверяем тип токена
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = {
            "user_id": UUID(payload["sub"]),
            "username": payload["username"],
            "role": UserRole[payload["role"]],
        }
        structlog.contextvars.bind_contextvars(user_id=str(user["user_id"]))
        return user
    except ValueError as ex:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=str(ex),
            headers={"WWW-Authenticate": "Bearer"},
        ) from ex
    except Exception as ex:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from ex


def check_role(current_user: dict[str, Any], allowed_roles: list[UserRole]) -> None:
    """Проверить роль пользователя"""
    user_role = current_user["role"]
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

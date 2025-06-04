# app/presentation/middleware/auth.py

from typing import Optional, Dict, Any
from uuid import UUID

from fastapi import Request, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from dishka.integrations.fastapi import FromDishka

from app.domain.ports.token_service import TokenServicePort
from app.domain.entities.user import UserRole


async def get_token_from_header(request: Request) -> Optional[str]:
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
) -> Dict[str, Any]:
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

        return {
            "user_id": UUID(payload["sub"]),
            "username": payload["username"],
            "role": UserRole[payload["role"]]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_role(current_user: Dict[str, Any], allowed_roles: list[UserRole]) -> None:
    """Проверить роль пользователя"""
    user_role = current_user["role"]
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
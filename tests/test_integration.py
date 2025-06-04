# tests/test_integration.py

import pytest
from httpx import AsyncClient
import asyncio


class TestFullUserFlow:
    """Интеграционные тесты полного флоу пользователя"""

    @pytest.mark.asyncio
    async def test_complete_user_lifecycle(self, async_client: AsyncClient):
        """Полный жизненный цикл пользователя"""
        # 1. Создаём админа (первый пользователь)
        admin_resp = await async_client.post("/users/", json={
            "username": "firstadmin",
            "password": "admin123",
            "role": "ADMIN"
        })
        assert admin_resp.status_code == 201

        # 2. Логинимся как админ
        admin_login = await async_client.post("/auth/login", json={
            "username": "firstadmin",
            "password": "admin123"
        })
        admin_token = admin_login.json()["access_token"]

        # 3. Создаём обычного пользователя
        user_resp = await async_client.post(
            "/users/",
            json={
                "username": "lifecycle_user",
                "password": "user123",
                "role": "USER"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        user_id = user_resp.json()["id"]

        # 4. Пользователь логинится
        user_login = await async_client.post("/auth/login", json={
            "username": "lifecycle_user",
            "password": "user123"
        })
        user_token = user_login.json()["access_token"]
        user_refresh = user_login.json()["refresh_token"]

        # 5. Пользователь получает свой профиль
        profile_resp = await async_client.get(
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert profile_resp.status_code == 200

        # 6. Пользователь обновляет свой профиль
        update_resp = await async_client.put(
            f"/users/{user_id}",
            json={"username": "updated_lifecycle"},
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert update_resp.status_code == 200

        # 7. Пользователь обновляет токены
        refresh_resp = await async_client.post("/auth/refresh", json={
            "refresh_token": user_refresh
        })
        new_token = refresh_resp.json()["access_token"]

        # 8. Админ повышает пользователя до оператора
        promote_resp = await async_client.put(
            f"/users/{user_id}",
            json={"role": "OPERATOR"},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert promote_resp.status_code == 200

        # 9. Пользователь перелогинивается с новыми правами
        new_login = await async_client.post("/auth/login", json={
            "username": "updated_lifecycle",
            "password": "user123"
        })
        operator_token = new_login.json()["access_token"]

        # 10. Теперь может просматривать список пользователей
        list_resp = await async_client.get(
            "/users/",
            headers={"Authorization": f"Bearer {operator_token}"}
        )
        assert list_resp.status_code == 200

        # 11. Админ деактивирует пользователя
        deactivate_resp = await async_client.put(
            f"/users/{user_id}",
            json={"deactivate": True},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert deactivate_resp.status_code == 200

        # 12. Пользователь больше не может войти
        failed_login = await async_client.post("/auth/login", json={
            "username": "updated_lifecycle",
            "password": "user123"
        })
        assert failed_login.status_code == 401

        # 13. Админ удаляет пользователя
        delete_resp = await async_client.delete(
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert delete_resp.status_code == 204

    @pytest.mark.asyncio
    async def test_token_expiration_flow(self, async_client: AsyncClient):
        """Тест работы с истекшими токенами"""
        # Создаём пользователя
        await async_client.post("/users/", json={
            "username": "expiretest",
            "password": "password123",
            "role": "USER"
        })

        # Логинимся
        login_resp = await async_client.post("/auth/login", json={
            "username": "expiretest",
            "password": "password123"
        })
        tokens = login_resp.json()
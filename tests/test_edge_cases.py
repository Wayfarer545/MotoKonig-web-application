# tests/test_edge_cases.py

import pytest
import asyncio
from httpx import AsyncClient
from uuid import uuid4


class TestBlacklist:
    """Тесты функциональности blacklist"""

    @pytest.mark.asyncio
    async def test_token_blacklisted_after_logout(self, async_client: AsyncClient):
        """Токен добавляется в blacklist после logout"""
        # Создаём пользователя и логинимся
        await async_client.post("/users/", json={
            "username": "blacklisttest",
            "password": "password123",
            "role": "USER"
        })

        login_resp = await async_client.post("/auth/login", json={
            "username": "blacklisttest",
            "password": "password123"
        })
        token = login_resp.json()["access_token"]

        # Проверяем, что токен работает
        resp = await async_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert resp.status_code == 200

        # Logout
        await async_client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Проверяем, что токен больше не работает
        resp = await async_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_old_refresh_token_blacklisted(self, async_client: AsyncClient):
        """Старый refresh token блокируется после обновления"""
        # Логинимся
        login_resp = await async_client.post("/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        old_refresh = login_resp.json()["refresh_token"]

        # Обновляем токены
        refresh_resp = await async_client.post("/auth/refresh", json={
            "refresh_token": old_refresh
        })
        assert refresh_resp.status_code == 200

        # Пытаемся использовать старый refresh token
        resp = await async_client.post("/auth/refresh", json={
            "refresh_token": old_refresh
        })
        assert resp.status_code == 401


class TestValidation:
    """Тесты валидации данных"""

    @pytest.mark.asyncio
    async def test_username_min_length(self, async_client: AsyncClient, admin_token: str):
        """Проверка минимальной длины username"""
        resp = await async_client.post(
            "/users/",
            json={
                "username": "ab",  # Меньше 3 символов
                "password": "password123",
                "role": "USER"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_password_min_length(self, async_client: AsyncClient, admin_token: str):
        """Проверка минимальной длины пароля"""
        resp = await async_client.post(
            "/users/",
            json={
                "username": "testuser",
                "password": "12345",  # Меньше 6 символов
                "role": "USER"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_invalid_role(self, async_client: AsyncClient, admin_token: str):
        """Проверка невалидной роли"""
        resp = await async_client.post(
            "/users/",
            json={
                "username": "testuser",
                "password": "password123",
                "role": "SUPERADMIN"  # Несуществующая роль
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_duplicate_username(self, async_client: AsyncClient, admin_token: str):
        """Проверка уникальности username"""
        # Создаём первого пользователя
        resp = await async_client.post(
            "/users/",
            json={
                "username": "duplicate",
                "password": "password123",
                "role": "USER"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 201

        # Пытаемся создать с тем же username
        resp = await async_client.post(
            "/users/",
            json={
                "username": "duplicate",
                "password": "password456",
                "role": "USER"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 400  # или 409 в зависимости от обработки

    @pytest.mark.asyncio
    async def test_username_case_insensitive(self, async_client: AsyncClient, admin_token: str):
        """Username должен быть case-insensitive"""
        # Создаём пользователя
        resp = await async_client.post(
            "/users/",
            json={
                "username": "TestCase",
                "password": "password123",
                "role": "USER"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["username"] == "testcase"  # Должен быть в lowercase

        # Логинимся с разным регистром
        resp = await async_client.post("/auth/login", json={
            "username": "TESTCASE",
            "password": "password123"
        })
        assert resp.status_code == 200


class TestConcurrency:
    """Тесты для проверки параллельных запросов"""

    @pytest.mark.asyncio
    async def test_concurrent_user_creation(self, async_client: AsyncClient, admin_token: str):
        """Проверка создания пользователей параллельно"""

        async def create_user(index: int):
            return await async_client.post(
                "/users/",
                json={
                    "username": f"concurrent{index}",
                    "password": "password123",
                    "role": "USER"
                },
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        # Создаём 5 пользователей параллельно
        tasks = [create_user(i) for i in range(5)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Проверяем, что все успешно созданы
        for resp in responses:
            assert not isinstance(resp, Exception)
            assert resp.status_code == 201

    @pytest.mark.asyncio
    async def test_concurrent_same_username(self, async_client: AsyncClient, admin_token: str):
        """Проверка создания пользователей с одинаковым username параллельно"""

        async def create_user():
            return await async_client.post(
                "/users/",
                json={
                    "username": "racecondition",
                    "password": "password123",
                    "role": "USER"
                },
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        # Пытаемся создать 3 пользователя с одинаковым username
        tasks = [create_user() for _ in range(3)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Только один должен успешно создаться
        success_count = sum(
            1 for resp in responses
            if not isinstance(resp, Exception) and resp.status_code == 201
        )
        assert success_count == 1


class TestPasswordHashing:
    """Тесты хеширования паролей"""

    @pytest.mark.asyncio
    async def test_password_is_hashed(self, async_client: AsyncClient, admin_token: str):
        """Проверка, что пароль хешируется"""
        # Этот тест требует доступа к БД напрямую
        # или специального endpoint'а для тестирования
        # Пока проверяем косвенно через смену пароля

        # Создаём пользователя
        resp = await async_client.post(
            "/users/",
            json={
                "username": "hashtest",
                "password": "originalpass",
                "role": "USER"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        user_id = resp.json()["id"]

        # Меняем пароль
        resp = await async_client.put(
            f"/users/{user_id}",
            json={"password": "newpassword"},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 200

        # Проверяем, что старый пароль не работает
        resp = await async_client.post("/auth/login", json={
            "username": "hashtest",
            "password": "originalpass"
        })
        assert resp.status_code == 401

        # Проверяем, что новый работает
        resp = await async_client.post("/auth/login", json={
            "username": "hashtest",
            "password": "newpassword"
        })
        assert resp.status_code == 200
# tests/test_auth_comprehensive.py

import pytest
from httpx import AsyncClient
from uuid import UUID
from tests.conftest import create_test_user


@pytest.fixture
async def admin_token(async_client: AsyncClient, create_test_user) -> str:
    """Создаём админа и получаем его токен"""
    # Создаём админа
    await create_test_user("admin", "admin123", "ADMIN")

    # Логинимся
    resp = await async_client.post("/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    return resp.json()["access_token"]


@pytest.fixture
async def operator_token(async_client: AsyncClient, admin_token: str, create_test_user) -> str:
    """Создаём оператора и получаем его токен"""
    # Создаём оператора под админом
    await async_client.post(
        "/users/",
        json={
            "username": "operator",
            "password": "operator123",
            "role": "OPERATOR"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    # Логинимся
    resp = await async_client.post("/auth/login", json={
        "username": "operator",
        "password": "operator123"
    })
    return resp.json()["access_token"]


@pytest.fixture
async def user_token(async_client: AsyncClient, admin_token: str) -> str:
    """Создаём обычного пользователя и получаем его токен"""
    # Создаём пользователя под админом
    resp = await async_client.post(
        "/users/",
        json={
            "username": "user",
            "password": "user123",
            "role": "USER"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    # Логинимся
    resp = await async_client.post("/auth/login", json={
        "username": "user",
        "password": "user123"
    })
    return resp.json()["access_token"]


class TestAuthentication:
    """Тесты аутентификации"""

    @pytest.mark.asyncio
    async def test_login_success(self, async_client: AsyncClient, admin_token: str):
        """Успешный вход"""
        resp = await async_client.post("/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, async_client: AsyncClient, admin_token: str):
        """Вход с неверным паролем"""
        resp = await async_client.post("/auth/login", json={
            "username": "admin",
            "password": "wrong"
        })
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, async_client: AsyncClient):
        """Вход несуществующего пользователя"""
        resp = await async_client.post("/auth/login", json={
            "username": "nonexistent",
            "password": "password"
        })
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_get_me(self, async_client: AsyncClient, user_token: str):
        """Получение информации о себе"""
        resp = await async_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "user"
        assert data["role"] == "USER"

    @pytest.mark.asyncio
    async def test_get_me_without_token(self, async_client: AsyncClient):
        """Получение информации без токена"""
        resp = await async_client.get("/auth/me")
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_logout(self, async_client: AsyncClient, user_token: str):
        """Выход из системы"""
        # Logout
        resp = await async_client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert resp.status_code == 200

        # Проверяем, что токен больше не работает
        resp = await async_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_refresh_token(self, async_client: AsyncClient):
        """Обновление токенов"""
        # Логинимся
        login_resp = await async_client.post("/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        tokens = login_resp.json()

        # Обновляем
        resp = await async_client.post("/auth/refresh", json={
            "refresh_token": tokens["refresh_token"]
        })
        assert resp.status_code == 200
        new_tokens = resp.json()

        # Проверяем, что получили новые токены
        assert "access_token" in new_tokens
        assert "refresh_token" in new_tokens
        assert new_tokens["access_token"] != tokens["access_token"]


class TestUserCRUD:
    """Тесты CRUD операций с пользователями"""

    @pytest.mark.asyncio
    async def test_create_user_as_admin(self, async_client: AsyncClient, admin_token: str):
        """Создание пользователя админом"""
        resp = await async_client.post(
            "/users/",
            json={
                "username": "newuser",
                "password": "password123",
                "role": "USER"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["username"] == "newuser"
        assert data["role"] == "USER"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_user_as_operator(self, async_client: AsyncClient, operator_token: str):
        """Оператор не может создавать пользователей"""
        resp = await async_client.post(
            "/users/",
            json={
                "username": "newuser2",
                "password": "password123",
                "role": "USER"
            },
            headers={"Authorization": f"Bearer {operator_token}"}
        )
        assert resp.status_code == 403

    @pytest.mark.asyncio
    async def test_list_users_as_admin(self, async_client: AsyncClient, admin_token: str):
        """Получение списка пользователей админом"""
        resp = await async_client.get(
            "/users/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # Минимум сам админ

    @pytest.mark.asyncio
    async def test_list_users_as_operator(self, async_client: AsyncClient, operator_token: str):
        """Получение списка пользователей оператором"""
        resp = await async_client.get(
            "/users/",
            headers={"Authorization": f"Bearer {operator_token}"}
        )
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_list_users_as_user(self, async_client: AsyncClient, user_token: str):
        """Обычный пользователь не может получить список"""
        resp = await async_client.get(
            "/users/",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert resp.status_code == 403

    @pytest.mark.asyncio
    async def test_get_own_profile(self, async_client: AsyncClient, user_token: str):
        """Получение своего профиля"""
        # Сначала получаем ID
        me_resp = await async_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        user_id = me_resp.json()["user_id"]

        # Получаем профиль
        resp = await async_client.get(
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "user"

    @pytest.mark.asyncio
    async def test_get_other_profile_as_user(self, async_client: AsyncClient, user_token: str, admin_token: str):
        """Пользователь не может получить чужой профиль"""
        # Получаем ID админа
        me_resp = await async_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        admin_id = me_resp.json()["user_id"]

        # Пытаемся получить профиль админа как обычный пользователь
        resp = await async_client.get(
            f"/users/{admin_id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert resp.status_code == 403

    @pytest.mark.asyncio
    async def test_update_own_profile(self, async_client: AsyncClient, user_token: str):
        """Обновление своего профиля"""
        # Получаем свой ID
        me_resp = await async_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        user_id = me_resp.json()["user_id"]

        # Обновляем username
        resp = await async_client.put(
            f"/users/{user_id}",
            json={"username": "updateduser"},
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "updateduser"

    @pytest.mark.asyncio
    async def test_user_cannot_change_role(self, async_client: AsyncClient, user_token: str):
        """Пользователь не может изменить свою роль"""
        # Получаем свой ID
        me_resp = await async_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        user_id = me_resp.json()["user_id"]

        # Пытаемся изменить роль
        resp = await async_client.put(
            f"/users/{user_id}",
            json={"role": "ADMIN"},
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert resp.status_code == 403

    @pytest.mark.asyncio
    async def test_admin_can_change_user_role(self, async_client: AsyncClient, admin_token: str, user_token: str):
        """Админ может изменить роль пользователя"""
        # Получаем ID пользователя
        me_resp = await async_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        user_id = me_resp.json()["user_id"]

        # Меняем роль на OPERATOR
        resp = await async_client.put(
            f"/users/{user_id}",
            json={"role": "OPERATOR"},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["role"] == "OPERATOR"

    @pytest.mark.asyncio
    async def test_delete_user(self, async_client: AsyncClient, admin_token: str):
        """Удаление пользователя админом"""
        # Создаём пользователя для удаления
        create_resp = await async_client.post(
            "/users/",
            json={
                "username": "todelete",
                "password": "password123",
                "role": "USER"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        user_id = create_resp.json()["id"]

        # Удаляем
        resp = await async_client.delete(
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 204

        # Проверяем, что пользователь удалён
        resp = await async_client.get(
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_deactivate_user(self, async_client: AsyncClient, admin_token: str):
        """Деактивация пользователя"""
        # Создаём пользователя
        create_resp = await async_client.post(
            "/users/",
            json={
                "username": "todeactivate",
                "password": "password123",
                "role": "USER"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        user_id = create_resp.json()["id"]

        # Деактивируем
        resp = await async_client.put(
            f"/users/{user_id}",
            json={"deactivate": True},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["is_active"] is False

        # Проверяем, что деактивированный пользователь не может войти
        login_resp = await async_client.post("/auth/login", json={
            "username": "todeactivate",
            "password": "password123"
        })
        assert login_resp.status_code == 401
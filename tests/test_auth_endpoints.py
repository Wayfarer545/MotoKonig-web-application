# tests/test_auth_endpoints.py

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient):
    """Тест успешного входа"""
    # Сначала создаём пользователя (пока без авторизации для теста)
    await async_client.post("/users/", json={
        "username": "testauth",
        "password": "password123",
        "role": "USER"
    })

    # Логинимся
    resp = await async_client.post("/auth/login", json={
        "username": "testauth",
        "password": "password123"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client: AsyncClient):
    """Тест входа с неверными данными"""
    resp = await async_client.post("/auth/login", json={
        "username": "nonexistent",
        "password": "wrongpass"
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me(async_client: AsyncClient):
    """Тест получения текущего пользователя"""
    # Создаём и логинимся
    await async_client.post("/users/", json={
        "username": "metest",
        "password": "password123",
        "role": "OPERATOR"
    })

    login_resp = await async_client.post("/auth/login", json={
        "username": "metest",
        "password": "password123"
    })
    token = login_resp.json()["access_token"]

    # Получаем /me
    resp = await async_client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "metest"
    assert data["role"] == "OPERATOR"


@pytest.mark.asyncio
async def test_logout(async_client: AsyncClient):
    """Тест выхода из системы"""
    # Логинимся
    await async_client.post("/users/", json={
        "username": "logouttest",
        "password": "password123",
        "role": "USER"
    })

    login_resp = await async_client.post("/auth/login", json={
        "username": "logouttest",
        "password": "password123"
    })
    token = login_resp.json()["access_token"]

    # Logout
    resp = await async_client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200

    # Проверяем, что токен больше не работает
    resp = await async_client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_refresh_token(async_client: AsyncClient):
    """Тест обновления токенов"""
    # Логинимся
    await async_client.post("/users/", json={
        "username": "refreshtest",
        "password": "password123",
        "role": "USER"
    })

    login_resp = await async_client.post("/auth/login", json={
        "username": "refreshtest",
        "password": "password123"
    })
    tokens = login_resp.json()

    # Обновляем токены
    resp = await async_client.post("/auth/refresh", json={
        "refresh_token": tokens["refresh_token"]
    })
    assert resp.status_code == 200
    new_tokens = resp.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens
    # Новые токены должны отличаться
    assert new_tokens["access_token"] != tokens["access_token"]


@pytest.mark.asyncio
async def test_protected_endpoint_without_auth(async_client: AsyncClient):
    """Тест защищённого эндпоинта без авторизации"""
    resp = await async_client.get("/users/")
    assert resp.status_code == 403
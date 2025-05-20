# tests/test_user_endpoints.py

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_and_get_user(async_client: AsyncClient):
    # 1) Создаём пользователя
    resp = await async_client.post("/users/", json={
        "username": "testuser",
        "password": "password123",
        "role": "user"
    })
    assert resp.status_code == 201
    data = resp.json()
    user_id = data["id"]
    assert data["username"] == "testuser"
    assert data["role"] == "user"
    assert data["is_active"] is True

    # 2) Получаем того же пользователя
    resp = await async_client.get(f"/users/{user_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == user_id
    assert data["username"] == "testuser"

@pytest.mark.asyncio
async def test_list_users(async_client: AsyncClient):
    resp = await async_client.get("/users/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # В списке должен быть, как минимум, созданный ранее testuser
    assert any(u["username"] == "testuser" for u in data)

@pytest.mark.asyncio
async def test_update_user(async_client: AsyncClient):
    # Создаём нового
    resp = await async_client.post("/users/", json={
        "username": "upduser",
        "password": "pass123",
        "role": "user"
    })
    uid = resp.json()["id"]

    # Обновляем имя и роль
    resp = await async_client.put(f"/users/{uid}", json={
        "username": "updated",
        "password": "newpass",
        "role": "admin",
        "deactivate": False
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "updated"
    assert data["role"] == "admin"

    # Деактивируем
    resp = await async_client.put(f"/users/{uid}", json={
        "deactivate": True
    })
    data = resp.json()
    assert data["is_active"] is False

@pytest.mark.asyncio
async def test_delete_user(async_client: AsyncClient):
    # Создаём для удаления
    resp = await async_client.post("/users/", json={
        "username": "deluser",
        "password": "pass123",
        "role": "user"
    })
    uid = resp.json()["id"]

    # Удаляем
    resp = await async_client.delete(f"/users/{uid}")
    assert resp.status_code == 204

    # После удаления – 404 при GET
    resp = await async_client.get(f"/users/{uid}")
    assert resp.status_code == 404

# tests/test_pin_auth.py

import pytest
from httpx import AsyncClient

from presentation.routers.auth import refresh_token


@pytest.mark.asyncio
async def test_pin_setup_and_login(async_client: AsyncClient):
    """Тест установки PIN и входа"""
    # Создаём пользователя и логинимся
    await async_client.post("/auth/register", json={
        "username": "pinuser",
        "password": "password123",
        "password_confirm": "password123"
    })

    login_resp = await async_client.post("/auth/login", json={
        "username": "pinuser",
        "password": "password123"
    })
    access_token = login_resp.json()["access_token"]
    refresh_token = login_resp.json()["refresh_token"]

    # Устанавливаем PIN
    pin_resp = await async_client.post(
        "/auth/setup-pin",
        json={
            "pin_code": "1234",
            "device_id": "test-device-123",
            "device_name": "Test iPhone"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert pin_resp.status_code == 200
    device_token = pin_resp.json()["device_token"]

    # Входим по PIN
    pin_login_resp = await async_client.post("/auth/pin-login", json={
        "pin_code": "1234",
        "device_id": "test-device-123",
        "refresh_token": refresh_token
    })
    assert pin_login_resp.status_code == 200

    # Проверяем, что получили новые токены
    new_access = pin_login_resp.json()["access_token"]
    new_refresh = pin_login_resp.json()["refresh_token"]
    assert new_access != access_token
    assert new_refresh != refresh_token

    # Проверяем, что старый refresh больше не работает
    retry_resp = await async_client.post("/auth/pin-login", json={
        "pin_code": "1234",
        "device_id": "test-device-123",
        "refresh_token": refresh_token  # старый
    })
    assert retry_resp.status_code == 401


@pytest.mark.asyncio
async def test_pin_brute_force_protection(async_client: AsyncClient):
    """Тест защиты от брутфорса"""
    # Подготовка...

    # Пытаемся войти с неправильным PIN 5 раз
    for i in range(5):
        resp = await async_client.post("/auth/pin-login", json={
            "pin_code": "9999",
            "device_id": "test-device",
            "refresh_token": refresh_token
        })

    # 6-я попытка должна быть заблокирована
    resp = await async_client.post("/auth/pin-login", json={
        "pin_code": "1234",  # даже с правильным PIN
        "device_id": "test-device",
        "refresh_token": refresh_token
    })
    assert resp.status_code == 429  # Too Many Requests
# tests/conftest.py

import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport


@pytest.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Создаём асинхронный клиент для тестирования"""
    from app.presentation.api import app

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
async def create_test_user(async_client: AsyncClient):
    """Фабрика для создания тестовых пользователей"""
    created_users = []

    async def _create_user(username: str, password: str, role: str = "USER"):
        resp = await async_client.post("/users/", json={
            "username": username,
            "password": password,
            "role": role
        })
        if resp.status_code == 201:
            user_data = resp.json()
            created_users.append(user_data["id"])
            return user_data
        return None

    yield _create_user
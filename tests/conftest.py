# tests/conftest.py

import pytest
import asyncio
from httpx import AsyncClient
from app.main import app

@pytest.fixture(scope="session")
def event_loop():
    """Используем один цикл для всех тестов."""
    return asyncio.get_event_loop()

@pytest.fixture(scope="session")
async def async_client():
    """
    HTTPX AsyncClient для тестирования FastAPI.
    Базовый URL – http://testserver, чтобы маршруты работали без поднятого сервера.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

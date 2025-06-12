import time
from collections.abc import Generator

import pytest
from pytest import MonkeyPatch
from pytest_databases.docker.postgres import PostgresService
from tests.factories.user_factory import UserFactory
from tests.factories.motorcycle_factory import MotorcycleFactory
from tests.factories.listing_factory import ListingFactory
from tests.factories.profile_factory import ProfileFactory
from tests.fixtures.enhanced_repositories import (
    EnhancedFakeUserRepository,
    EnhancedFakeMotorcycleRepository
)
from tests.fixtures.smart_mocks import SmartTokenServiceMock, SmartPasswordServiceMock

pytest_plugins = [
    "pytest_databases.docker",
    "pytest_databases.docker.postgres",
]


@pytest.fixture(scope="session")
def monkeypatch_session() -> Generator[MonkeyPatch, None, None]:
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope="session")
def postgres_psycopg_url(postgres_service: PostgresService) -> str:
    """Return a DSN for connecting to the temporary PostgreSQL instance."""
    dsn = "postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
    return dsn.format(
        user=postgres_service.user,
        password=postgres_service.password,
        host=postgres_service.host,
        port=postgres_service.port,
        database=postgres_service.database,
    )

@pytest.fixture
def user_factory():
    """Фабрика пользователей"""
    return UserFactory

@pytest.fixture
def motorcycle_factory():
    """Фабрика мотоциклов"""
    return MotorcycleFactory

@pytest.fixture
def listing_factory():
    """Фабрика объявлений"""
    return ListingFactory

@pytest.fixture
def profile_factory():
    """Фабрика профилей"""
    return ProfileFactory

@pytest.fixture
def user_repository():
    """Улучшенный фейковый репозиторий пользователей"""
    return EnhancedFakeUserRepository()

@pytest.fixture
def motorcycle_repository():
    """Улучшенный фейковый репозиторий мотоциклов"""
    return EnhancedFakeMotorcycleRepository()

@pytest.fixture
def token_service():
    """Умный мок токен-сервиса"""
    return SmartTokenServiceMock()

@pytest.fixture
def password_service():
    """Умный мок пароль-сервиса"""
    return SmartPasswordServiceMock()

@pytest.fixture
def performance_tracker():
    """Трекер производительности тестов"""
    start_time = time.time()
    yield
    end_time = time.time()
    execution_time = end_time - start_time
    if execution_time > 1.0:
        pytest.fail(f"Test execution too slow: {execution_time:.2f}s (limit: 1.0s)")
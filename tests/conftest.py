from collections.abc import Generator

import pytest
from pytest import MonkeyPatch
from pytest_databases.docker.postgres import PostgresService

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

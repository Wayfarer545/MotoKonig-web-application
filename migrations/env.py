import asyncio

from advanced_alchemy.base import AdvancedDeclarativeBase
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from app.config.settings import Config
from app.infrastructure.models import Base  # noqa: F401

db_url = Config().postgres.get_dsn()

# Создаём асинхронный движок
engine = create_async_engine(db_url, echo=False)

# Импортируем метаданные моделей
target_metadata = AdvancedDeclarativeBase.metadata

config = context.config
config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline():
    """Запуск миграций в оффлайн-режиме (без подключения к БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online_async():
    """Запуск миграций в онлайн-режиме для асинхронного движка."""
    async with engine.connect() as connection:
        # Конфигурируем контекст Alembic с синхронным соединением через run_sync
        await connection.run_sync(
            lambda conn: context.configure(connection=conn, target_metadata=target_metadata)
        )
        # Выполняем миграции в рамках асинхронной транзакции
        async with connection.begin():
            await connection.run_sync(lambda conn: context.run_migrations())

def run_migrations_online():
    """Синхронная обёртка для асинхронных миграций."""
    asyncio.run(run_migrations_online_async())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

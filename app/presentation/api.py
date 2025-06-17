# app/presentation/api.py

from contextlib import asynccontextmanager

import uvicorn
from advanced_alchemy.extensions.fastapi import (
    AdvancedAlchemy,
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
)
from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from app.config.logging import setup_logging
from app.config.settings import Config
from app.infrastructure.di.container import (
    InfrastructureProvider,
    PresentationProvider,
    UseCaseProvider,
)
from app.infrastructure.messaging.redis_client import RedisClient
from app.presentation.middleware.cors import add_cors_middleware
from app.presentation.middleware.logging import LoggingContextMiddleware
from app.presentation.routers.main import router as main_router

# 1. Инициализируем логирование
setup_logging()

# 2. Загружаем конфиг
config = Config()

# 3. Настраиваем Advanced-Alchemy вместе с FastAPI
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=config.postgres.get_dsn(),
    session_config=AsyncSessionConfig(expire_on_commit=False),
    create_all=False,
    commit_mode="autocommit",
)

# Lifecycle manager для очистки ресурсов
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    # Startup
    app_config = app_instance.state.config
    await RedisClient.create_pool(app_config.redis)
    yield
    # Shutdown
    await RedisClient.close_pool()

# 4. Создаём приложение с lifecycle manager
app = FastAPI(
    title=config.project.project_name,
    version=config.project.version,
    docs_url="/openapi",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# 5. Сохраняем конфиг в state
app.state.config = config  # noqa

# 6. Инициализируем Advanced-Alchemy
alchemy = AdvancedAlchemy(config=sqlalchemy_config, app=app)

# 7. Конфигурируем DI-контейнер
container = make_async_container(
    InfrastructureProvider(alchemy, config),
    UseCaseProvider(),
    PresentationProvider(),
    FastapiProvider()
)

# 8. Подключаем middleware
app.add_middleware(LoggingContextMiddleware)
add_cors_middleware(app)

# 9. Подключаем Dishka и роуты
setup_dishka(container, app)
app.include_router(main_router)

@app.get("/health", tags=["System"])
async def health_check() -> dict:
    return {"status": "ok", "version": config.project.version}


# 10. Точка входа
if __name__ == "__main__":
    uvicorn.run("app.presentation.api:app", host="0.0.0.0", port=8000, reload=True)

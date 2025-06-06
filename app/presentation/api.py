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

from app.config.logging_config import setup_logging
from app.config.settings import Config
from app.infrastructure.di.container import (
    InfrastructureProvider,
    PresentationProvider,
    UseCaseProvider,
)
from app.infrastructure.messaging.redis_client import RedisClient
from app.presentation.middleware.cors import add_cors_middleware
from app.presentation.routers.auth import router as auth_router
from app.presentation.routers.motorcycle import router as motorcycle_router
from app.presentation.routers.user import router as user_router


# Lifecycle manager для очистки ресурсов
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    config = app.state.config
    await RedisClient.create_pool(config.redis)
    yield
    # Shutdown
    await RedisClient.close_pool()


# 1. Загружаем конфиг
config = Config()

# 2. Настраиваем Advanced-Alchemy вместе с FastAPI
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=config.sqlite.sqlite_dsn,
    session_config=AsyncSessionConfig(expire_on_commit=False),
    create_all=False,
    commit_mode="autocommit",
)

# Создаём приложение с lifecycle manager
app = FastAPI(
    title=config.project.project_name,
    version=config.project.version,
    docs_url="/openapi",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Сохраняем конфиг в state
app.state.config = config  # noqa

# Инициализируем Advanced-Alchemy
alchemy = AdvancedAlchemy(config=sqlalchemy_config, app=app)

# 3. Конфигурируем DI-контейнер
container = make_async_container(
    InfrastructureProvider(alchemy, config),
    UseCaseProvider(),
    PresentationProvider(),
    FastapiProvider(),
)

# 4. Подключаем middleware
add_cors_middleware(app)

# 5. Подключаем Dishka и роуты
setup_dishka(container, app)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(motorcycle_router, prefix="/motorcycle", tags=["Motorcycle"])

# 6. Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "version": config.project.version}


# 7. Точка входа
if __name__ == "__main__":
    uvicorn.run("app.presentation.api:app", host="0.0.0.0", port=8000, reload=True)

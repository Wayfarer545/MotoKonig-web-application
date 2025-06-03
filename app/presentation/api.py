# app/presentation/api.py

import uvicorn
from fastapi import FastAPI

from advanced_alchemy.extensions.fastapi import (
    AdvancedAlchemy,
    SQLAlchemyAsyncConfig,
    AsyncSessionConfig,
)
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka, FastapiProvider

from app.config.settings import Config
from app.infrastructure.di.container import ApplicationProvider
from app.presentation.routers.user import router as user_router

# 1. Загружаем конфиг
config = Config()

# 2. Настраиваем Advanced-Alchemy вместе с FastAPI сразу в конструкторе
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=config.sqlite.sqlite_dsn,
    session_config=AsyncSessionConfig(expire_on_commit=False),
    create_all=True,
    commit_mode="autocommit",
)
# Передаём app прямо в __init__, чтобы не было попытки set property later:
app = FastAPI(
    title="AiOS NVR API",
    docs_url="/openapi",
    openapi_url="/openapi.json",
)
alchemy = AdvancedAlchemy(config=sqlalchemy_config, app=app)

# 3. Конфигурируем DI-контейнер
container = make_async_container(
    ApplicationProvider(alchemy),
    FastapiProvider(),
    context={Config: config},
)

# 4. Подключаем Dishka и роуты
setup_dishka(container, app)
app.include_router(user_router, prefix="/users", tags=["Users"])

# 5. Точка входа
if __name__ == "__main__":
    uvicorn.run("app.presentation.api:app", host="0.0.0.0", port=8000, reload=True)

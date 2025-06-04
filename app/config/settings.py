# src/infrastructure/config.py

from os import environ as env
from typing import Final

from pydantic import Field, BaseModel
from pathlib import Path


class ProjectConfig(BaseModel):
    project_name: str = "MotoKonig API Gateway"
    version: str = Field(alias='VERSION', default='dev')


class SecuritySettings(BaseModel):
    secret_key: str = Field(alias='SECRET_KEY', default="my_projects_most_secret_key_ever")
    algorithm: str = Field(alias='ALGORITHM', default="HS256")


class RedisConfig(BaseModel):
    redis_host: str = Field(alias='REDIS_HOST', default='localhost')
    redis_port: int = Field(alias='REDIS_PORT', default=6379)


class SQLiteConfig(BaseModel):
    sqlite_dsn: str = "sqlite+aiosqlite:///app/infrastructure/database/app.db"


class StorageConfig(BaseModel):
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    log_dir: Path = base_dir / "logs"
    root_path: Path = base_dir / "data"
    temp_path: Path = root_path / "temp"
    media_path: Path = root_path / "media"


class LoggingConfig(BaseModel):
    log_level_console: str = "INFO"
    log_level_file: str = "DEBUG"


class RabbitMQConfig(BaseModel):
    host: str = Field(alias='RABBITMQ_HOST', default='localhost')
    port: int = Field(alias='RABBITMQ_PORT', default=5672)
    login: str = Field(alias='RABBITMQ_USER', default='guest')
    password: str = Field(alias='RABBITMQ_PASS', default='guest')


class Config(BaseModel):
    project: ProjectConfig = Field(default_factory=lambda: ProjectConfig(**env))
    security: SecuritySettings = Field(default_factory=lambda: SecuritySettings(**env))
    redis: RedisConfig = Field(default_factory=lambda: RedisConfig(**env))
    sqlite: SQLiteConfig = Field(default_factory=lambda: SQLiteConfig(**env))
    storage: StorageConfig = Field(default_factory=lambda: StorageConfig(**env))
    logging: LoggingConfig = Field(default_factory=lambda: LoggingConfig(**env))
    rabbitmq: RabbitMQConfig = Field(default_factory=lambda: RabbitMQConfig(**env))

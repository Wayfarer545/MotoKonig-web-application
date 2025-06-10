# src/infrastructure/config.py

from os import environ as env
from pathlib import Path

from pydantic import BaseModel, Field


class ProjectConfig(BaseModel):
    project_name: str = "MotoKonig API Gateway"
    version: str = Field(alias='VERSION', default='dev')


class SecuritySettings(BaseModel):
    secret_key: str = Field(alias='SECRET_KEY', default="my_projects_most_secret_key_ever")
    algorithm: str = Field(alias='ALGORITHM', default="HS256")


class PostgresConfig(BaseModel):
    postgres_db: str = Field(alias='POSTGRES_DB', default="motokonig")
    postgres_user: str = Field(alias='POSTGRES_USER', default="motokonig")
    postgres_password: str = Field(alias='POSTGRES_PASSWORD', default="motokonig")
    postgres_host: str = Field(alias='POSTGRES_HOST', default="localhost")
    postgres_port: int = Field(alias='POSTGRES_PORT', default=5432)
    
    def get_dsn(self) -> str:
        """Return the PostgreSQL DSN."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


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


class MinIOConfig(BaseModel):
    """Конфигурация MinIO"""
    endpoint: str = Field(alias='MINIO_ENDPOINT', default='localhost:9000')
    access_key: str = Field(alias='MINIO_ACCESS_KEY', default='minioadmin')
    secret_key: str = Field(alias='MINIO_SECRET_KEY', default='minioadmin')
    secure: bool = Field(alias='MINIO_SECURE', default=False)
    region: str = Field(alias='MINIO_REGION', default='us-east-1')

    # Названия бакетов
    avatars_bucket: str = Field(alias='MINIO_AVATARS_BUCKET', default='avatars')
    motorcycles_bucket: str = Field(alias='MINIO_MOTORCYCLES_BUCKET', default='motorcycles')
    events_bucket: str = Field(alias='MINIO_EVENTS_BUCKET', default='events')
    temp_bucket: str = Field(alias='MINIO_TEMP_BUCKET', default='temp')


class Config(BaseModel):
    project: ProjectConfig = Field(default_factory=lambda: ProjectConfig(**env))
    security: SecuritySettings = Field(default_factory=lambda: SecuritySettings(**env))
    redis: RedisConfig = Field(default_factory=lambda: RedisConfig(**env))
    sqlite: SQLiteConfig = Field(default_factory=lambda: SQLiteConfig(**env))
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    storage: StorageConfig = Field(default_factory=lambda: StorageConfig(**env))
    logging: LoggingConfig = Field(default_factory=lambda: LoggingConfig(**env))
    rabbitmq: RabbitMQConfig = Field(default_factory=lambda: RabbitMQConfig(**env))
    minio: MinIOConfig = Field(default_factory=lambda: MinIOConfig(**env))

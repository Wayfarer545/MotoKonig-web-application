"""add media files table

Revision ID: add_media_files_table
Revises: add_profiles_tables
Create Date: 2025-06-06 15:30:00.000000

"""
from collections.abc import Sequence

import advanced_alchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'add_media_files_table'
down_revision: str | None = 'add_profiles_tables'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    # Создаем enum для типов файлов
    file_type_enum = sa.Enum(
        'avatar', 'motorcycle_photo', 'event_photo', 'document', 'temp',
        name='file_type',
        native_enum=False
    )

    # Создаем таблицу медиафайлов
    op.create_table(
        'media_files',
        sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Связь с владельцем
        sa.Column('owner_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),

        # Информация о файле
        sa.Column('file_type', file_type_enum, nullable=False),
        sa.Column('original_name', sa.String(length=255), nullable=False),
        sa.Column('file_key', sa.String(length=500), nullable=False),
        sa.Column('bucket', sa.String(length=100), nullable=False),

        # Метаданные файла
        sa.Column('content_type', sa.String(length=100), nullable=False),
        sa.Column('size_bytes', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(length=1000), nullable=False),

        # Настройки доступа
        sa.Column('is_public', sa.Boolean(), nullable=False, server_default='false'),

        # Дополнительные метаданные
        sa.Column('file_metadata', sa.Text(), nullable=True),

        # Ограничения
        sa.PrimaryKeyConstraint('id', name=op.f('pk_media_files')),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name=op.f('fk_media_files_owner_id_users')),
        sa.UniqueConstraint('file_key', name=op.f('uq_media_files_file_key')),
    )

    # Создаем индексы для оптимизации запросов
    op.create_index(op.f('ix_media_files_owner_id'), 'media_files', ['owner_id'], unique=False)
    op.create_index(op.f('ix_media_files_file_type'), 'media_files', ['file_type'], unique=False)
    op.create_index(op.f('ix_media_files_file_key'), 'media_files', ['file_key'], unique=True)
    op.create_index(op.f('ix_media_files_bucket'), 'media_files', ['bucket'], unique=False)
    op.create_index(op.f('ix_media_files_is_public'), 'media_files', ['is_public'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем индексы
    op.drop_index(op.f('ix_media_files_is_public'), table_name='media_files')
    op.drop_index(op.f('ix_media_files_bucket'), table_name='media_files')
    op.drop_index(op.f('ix_media_files_file_key'), table_name='media_files')
    op.drop_index(op.f('ix_media_files_file_type'), table_name='media_files')
    op.drop_index(op.f('ix_media_files_owner_id'), table_name='media_files')

    # Удаляем таблицу
    op.drop_table('media_files')

    # Удаляем enum
    op.execute('DROP TYPE IF EXISTS file_type')
"""add motorcycles table

Revision ID: add_motorcycles_table
Revises: c8b24b17d9fb
Create Date: 2025-06-05 12:00:00.000000

"""
from collections.abc import Sequence

import advanced_alchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'add_motorcycles_table'
down_revision: str | None = 'c8b24b17d9fb'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Создаем enum'ы для типов двигателей и мотоциклов
    engine_type_enum = sa.Enum(
        'inline_2', 'inline_3', 'inline_4', 'v_twin', 'v4',
        'single', 'boxer', 'electric',
        name='engine_type',
        native_enum=False
    )

    motorcycle_type_enum = sa.Enum(
        'sport', 'naked', 'touring', 'cruiser', 'chopper',
        'adventure', 'dirt_bike', 'supermoto', 'cafe_racer',
        'scrambler', 'scooter', 'trike', 'electric',
        name='motorcycle_type',
        native_enum=False
    )

    # Создаем таблицу мотоциклов
    op.create_table(
        'motorcycles',
        sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Связь с владельцем
        sa.Column('owner_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),

        # Основная информация
        sa.Column('brand', sa.String(length=100), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),

        # Технические характеристики
        sa.Column('engine_volume', sa.Integer(), nullable=False),
        sa.Column('engine_type', engine_type_enum, nullable=False),
        sa.Column('motorcycle_type', motorcycle_type_enum, nullable=False),
        sa.Column('power', sa.Integer(), nullable=True),
        sa.Column('mileage', sa.Integer(), nullable=True),

        # Дополнительная информация
        sa.Column('color', sa.String(length=50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),

        # Статус
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),

        # Ограничения
        sa.PrimaryKeyConstraint('id', name=op.f('pk_motorcycles')),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name=op.f('fk_motorcycles_owner_id_users')),
    )

    # Создаем индексы для оптимизации запросов
    op.create_index(op.f('ix_motorcycles_owner_id'), 'motorcycles', ['owner_id'], unique=False)
    op.create_index(op.f('ix_motorcycles_brand'), 'motorcycles', ['brand'], unique=False)
    op.create_index(op.f('ix_motorcycles_model'), 'motorcycles', ['model'], unique=False)
    op.create_index(op.f('ix_motorcycles_year'), 'motorcycles', ['year'], unique=False)
    op.create_index(op.f('ix_motorcycles_motorcycle_type'), 'motorcycles', ['motorcycle_type'], unique=False)
    op.create_index(op.f('ix_motorcycles_is_active'), 'motorcycles', ['is_active'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем индексы
    op.drop_index(op.f('ix_motorcycles_is_active'), table_name='motorcycles')
    op.drop_index(op.f('ix_motorcycles_motorcycle_type'), table_name='motorcycles')
    op.drop_index(op.f('ix_motorcycles_year'), table_name='motorcycles')
    op.drop_index(op.f('ix_motorcycles_model'), table_name='motorcycles')
    op.drop_index(op.f('ix_motorcycles_brand'), table_name='motorcycles')
    op.drop_index(op.f('ix_motorcycles_owner_id'), table_name='motorcycles')

    # Удаляем таблицу
    op.drop_table('motorcycles')

    # Удаляем enum'ы
    op.execute('DROP TYPE IF EXISTS engine_type')
    op.execute('DROP TYPE IF EXISTS motorcycle_type')

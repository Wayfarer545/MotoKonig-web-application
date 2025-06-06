"""add profiles and social links tables

Revision ID: add_profiles_tables
Revises: add_motorcycles_table
Create Date: 2025-06-06 02:48:00.000000

"""
from collections.abc import Sequence

import advanced_alchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'add_profiles_tables'
down_revision: str | None = 'add_motorcycles_table'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    # Создаем enum'ы для уровней приватности и социальных платформ
    privacy_level_enum = sa.Enum(
        'public', 'friends_only', 'moto_club_members', 'private',
        name='privacy_level',
        native_enum=False
    )

    phone_privacy_enum = sa.Enum(
        'public', 'friends_only', 'moto_club_members', 'private',
        name='phone_privacy_level',
        native_enum=False
    )

    location_privacy_enum = sa.Enum(
        'public', 'friends_only', 'moto_club_members', 'private',
        name='location_privacy_level',
        native_enum=False
    )

    social_platform_enum = sa.Enum(
        'vk', 'telegram', 'whatsapp', 'instagram', 'facebook', 'youtube',
        name='social_platform',
        native_enum=False
    )

    social_privacy_enum = sa.Enum(
        'public', 'friends_only', 'moto_club_members', 'private',
        name='social_privacy_level',
        native_enum=False
    )

    # Создаем таблицу профилей
    op.create_table(
        'profiles',
        sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Связь с пользователем (One-to-One)
        sa.Column('user_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),

        # Основная информация
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('location', sa.String(length=200), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('riding_experience', sa.Integer(), nullable=True),

        # Аватар
        sa.Column('avatar_url', sa.String(length=500), nullable=True),

        # Настройки приватности
        sa.Column('privacy_level', privacy_level_enum, nullable=False, server_default='public'),
        sa.Column('phone_privacy', phone_privacy_enum, nullable=False, server_default='friends_only'),
        sa.Column('location_privacy', location_privacy_enum, nullable=False, server_default='public'),

        # Ограничения
        sa.PrimaryKeyConstraint('id', name=op.f('pk_profiles')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_profiles_user_id_users')),
        sa.UniqueConstraint('user_id', name=op.f('uq_profiles_user_id')),
    )

    # Создаем индексы для профилей
    op.create_index(op.f('ix_profiles_user_id'), 'profiles', ['user_id'], unique=True)

    # Создаем таблицу социальных ссылок
    op.create_table(
        'social_links',
        sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Связь с профилем
        sa.Column('profile_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),

        # Информация о ссылке
        sa.Column('platform', social_platform_enum, nullable=False),
        sa.Column('url', sa.String(length=500), nullable=False),

        # Настройки и статус
        sa.Column('privacy_level', social_privacy_enum, nullable=False, server_default='friends_only'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),

        # Ограничения
        sa.PrimaryKeyConstraint('id', name=op.f('pk_social_links')),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], name=op.f('fk_social_links_profile_id_profiles')),
        sa.UniqueConstraint('profile_id', 'platform', name=op.f('uq_profile_platform')),
    )

    # Создаем индексы для социальных ссылок
    op.create_index(op.f('ix_social_links_profile_id'), 'social_links', ['profile_id'], unique=False)
    op.create_index(op.f('ix_social_links_platform'), 'social_links', ['platform'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем индексы социальных ссылок
    op.drop_index(op.f('ix_social_links_platform'), table_name='social_links')
    op.drop_index(op.f('ix_social_links_profile_id'), table_name='social_links')

    # Удаляем таблицу социальных ссылок
    op.drop_table('social_links')

    # Удаляем индексы профилей
    op.drop_index(op.f('ix_profiles_user_id'), table_name='profiles')

    # Удаляем таблицу профилей
    op.drop_table('profiles')

    # Удаляем enum'ы
    op.execute('DROP TYPE IF EXISTS social_privacy_level')
    op.execute('DROP TYPE IF EXISTS social_platform')
    op.execute('DROP TYPE IF EXISTS location_privacy_level')
    op.execute('DROP TYPE IF EXISTS phone_privacy_level')
    op.execute('DROP TYPE IF EXISTS privacy_level')
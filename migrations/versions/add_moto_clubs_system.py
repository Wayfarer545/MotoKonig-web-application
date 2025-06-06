"""add moto clubs system

Revision ID: add_moto_clubs_system
Revises: add_media_files_table
Create Date: 2025-06-07 18:00:00.000000

"""
from collections.abc import Sequence

import advanced_alchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'add_moto_clubs_system'
down_revision: str | None = 'add_media_files_table'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    # Создаем enum для ролей в клубе
    club_role_enum = sa.Enum(
        'PRESIDENT', 'VICE_PRESIDENT', 'SECRETARY', 'TREASURER',
        'EVENT_ORGANIZER', 'MODERATOR', 'SENIOR_MEMBER', 'MEMBER',
        name='club_role',
        native_enum=False
    )

    # Создаем таблицу мотоклубов
    op.create_table(
        'moto_clubs',
        sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Основная информация
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),

        # Связь с президентом
        sa.Column('president_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),

        # Настройки клуба
        sa.Column('is_public', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('max_members', sa.Integer(), nullable=True),
        sa.Column('location', sa.String(length=200), nullable=True),
        sa.Column('website', sa.String(length=500), nullable=True),

        # Медиа
        sa.Column('avatar_url', sa.String(length=1000), nullable=True),

        # Статус и даты
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('founded_date', sa.String(length=50), nullable=True),

        # Ограничения
        sa.PrimaryKeyConstraint('id', name=op.f('pk_moto_clubs')),
        sa.ForeignKeyConstraint(['president_id'], ['users.id'], name=op.f('fk_moto_clubs_president_id_users')),
    )

    # Создаем индексы для мотоклубов
    op.create_index(op.f('ix_moto_clubs_name'), 'moto_clubs', ['name'], unique=False)
    op.create_index(op.f('ix_moto_clubs_president_id'), 'moto_clubs', ['president_id'], unique=False)
    op.create_index(op.f('ix_moto_clubs_is_public'), 'moto_clubs', ['is_public'], unique=False)
    op.create_index(op.f('ix_moto_clubs_is_active'), 'moto_clubs', ['is_active'], unique=False)

    # Создаем таблицу членства в клубах
    op.create_table(
        'club_memberships',
        sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Связи
        sa.Column('club_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('user_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),

        # Информация о членстве
        sa.Column('role', club_role_enum, nullable=False, server_default='MEMBER'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='active'),

        # Дополнительная информация
        sa.Column('joined_at', sa.String(length=50), nullable=False),
        sa.Column('invited_by', advanced_alchemy.types.guid.GUID(length=16), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),

        # Ограничения
        sa.PrimaryKeyConstraint('id', name=op.f('pk_club_memberships')),
        sa.ForeignKeyConstraint(['club_id'], ['moto_clubs.id'], name=op.f('fk_club_memberships_club_id_moto_clubs')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_club_memberships_user_id_users')),
        sa.ForeignKeyConstraint(['invited_by'], ['users.id'], name=op.f('fk_club_memberships_invited_by_users')),
        sa.UniqueConstraint('club_id', 'user_id', name=op.f('uq_club_user_membership')),
    )

    # Создаем индексы для членства
    op.create_index(op.f('ix_club_memberships_club_id'), 'club_memberships', ['club_id'], unique=False)
    op.create_index(op.f('ix_club_memberships_user_id'), 'club_memberships', ['user_id'], unique=False)
    op.create_index(op.f('ix_club_memberships_role'), 'club_memberships', ['role'], unique=False)
    op.create_index(op.f('ix_club_memberships_status'), 'club_memberships', ['status'], unique=False)

    # Создаем enum для ролей в приглашениях (может отличаться от ролей в членстве)
    invited_club_role_enum = sa.Enum(
        'PRESIDENT', 'VICE_PRESIDENT', 'SECRETARY', 'TREASURER',
        'EVENT_ORGANIZER', 'MODERATOR', 'SENIOR_MEMBER', 'MEMBER',
        name='invited_club_role',
        native_enum=False
    )

    # Создаем таблицу приглашений в клубы
    op.create_table(
        'club_invitations',
        sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Связи
        sa.Column('club_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('inviter_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('invitee_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),

        # Информация о приглашении
        sa.Column('invited_role', invited_club_role_enum, nullable=False, server_default='MEMBER'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('message', sa.Text(), nullable=True),

        # Временные рамки
        sa.Column('expires_at', sa.String(length=50), nullable=False),
        sa.Column('responded_at', sa.String(length=50), nullable=True),

        # Ограничения
        sa.PrimaryKeyConstraint('id', name=op.f('pk_club_invitations')),
        sa.ForeignKeyConstraint(['club_id'], ['moto_clubs.id'], name=op.f('fk_club_invitations_club_id_moto_clubs')),
        sa.ForeignKeyConstraint(['inviter_id'], ['users.id'], name=op.f('fk_club_invitations_inviter_id_users')),
        sa.ForeignKeyConstraint(['invitee_id'], ['users.id'], name=op.f('fk_club_invitations_invitee_id_users')),
    )

    # Создаем индексы для приглашений
    op.create_index(op.f('ix_club_invitations_club_id'), 'club_invitations', ['club_id'], unique=False)
    op.create_index(op.f('ix_club_invitations_inviter_id'), 'club_invitations', ['inviter_id'], unique=False)
    op.create_index(op.f('ix_club_invitations_invitee_id'), 'club_invitations', ['invitee_id'], unique=False)
    op.create_index(op.f('ix_club_invitations_status'), 'club_invitations', ['status'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем индексы приглашений
    op.drop_index(op.f('ix_club_invitations_status'), table_name='club_invitations')
    op.drop_index(op.f('ix_club_invitations_invitee_id'), table_name='club_invitations')
    op.drop_index(op.f('ix_club_invitations_inviter_id'), table_name='club_invitations')
    op.drop_index(op.f('ix_club_invitations_club_id'), table_name='club_invitations')

    # Удаляем таблицу приглашений
    op.drop_table('club_invitations')

    # Удаляем индексы членства
    op.drop_index(op.f('ix_club_memberships_status'), table_name='club_memberships')
    op.drop_index(op.f('ix_club_memberships_role'), table_name='club_memberships')
    op.drop_index(op.f('ix_club_memberships_user_id'), table_name='club_memberships')
    op.drop_index(op.f('ix_club_memberships_club_id'), table_name='club_memberships')

    # Удаляем таблицу членства
    op.drop_table('club_memberships')

    # Удаляем индексы клубов
    op.drop_index(op.f('ix_moto_clubs_is_active'), table_name='moto_clubs')
    op.drop_index(op.f('ix_moto_clubs_is_public'), table_name='moto_clubs')
    op.drop_index(op.f('ix_moto_clubs_president_id'), table_name='moto_clubs')
    op.drop_index(op.f('ix_moto_clubs_name'), table_name='moto_clubs')

    # Удаляем таблицу клубов
    op.drop_table('moto_clubs')

    # Удаляем enum'ы
    op.execute('DROP TYPE IF EXISTS invited_club_role')
    op.execute('DROP TYPE IF EXISTS club_role')

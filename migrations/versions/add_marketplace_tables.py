"""add marketplace tables

Revision ID: add_marketplace_tables
Revises: add_moto_clubs_system
Create Date: 2025-06-10 20:00:00.000000

"""
from collections.abc import Sequence

import advanced_alchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'add_marketplace_tables'
down_revision: str | None = 'add_moto_clubs_system'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    # Создаем enum'ы для категорий и статусов объявлений
    listing_category_enum = sa.Enum(
        'motorcycles', 'parts', 'equipment', 'services', 'accessories',
        name='listing_category',
        native_enum=False
    )

    listing_status_enum = sa.Enum(
        'draft', 'moderation', 'active', 'sold', 'expired', 'rejected', 'suspended',
        name='listing_status',
        native_enum=False
    )

    # Создаем таблицу объявлений
    op.create_table(
        'listings',
        sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Связь с продавцом
        sa.Column('seller_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),

        # Основная информация
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', listing_category_enum, nullable=False),

        # Цена и торговля
        sa.Column('price', sa.Integer(), nullable=False),  # в копейках
        sa.Column('currency', sa.String(length=3), nullable=False, server_default='RUB'),
        sa.Column('is_negotiable', sa.Boolean(), nullable=False, server_default='true'),

        # Локация
        sa.Column('location', sa.String(length=200), nullable=False),

        # Статус и модерация
        sa.Column('status', listing_status_enum, nullable=False, server_default='draft'),
        sa.Column('moderation_notes', sa.Text(), nullable=True),

        # Контактная информация
        sa.Column('contact_phone', sa.String(length=20), nullable=True),
        sa.Column('contact_email', sa.String(length=100), nullable=True),

        # Медиа (JSON массив URL'ов)
        sa.Column('photo_urls', sa.Text(), nullable=True),

        # Статистика
        sa.Column('views_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_featured', sa.Boolean(), nullable=False, server_default='false'),

        # Сроки
        sa.Column('expires_at', sa.String(length=50), nullable=True),  # ISO формат

        # Ограничения
        sa.PrimaryKeyConstraint('id', name=op.f('pk_listings')),
        sa.ForeignKeyConstraint(['seller_id'], ['users.id'], name=op.f('fk_listings_seller_id_users')),
    )

    # Создаем индексы для объявлений
    op.create_index(op.f('ix_listings_seller_id'), 'listings', ['seller_id'], unique=False)
    op.create_index(op.f('ix_listings_title'), 'listings', ['title'], unique=False)
    op.create_index(op.f('ix_listings_category'), 'listings', ['category'], unique=False)
    op.create_index(op.f('ix_listings_price'), 'listings', ['price'], unique=False)
    op.create_index(op.f('ix_listings_location'), 'listings', ['location'], unique=False)
    op.create_index(op.f('ix_listings_status'), 'listings', ['status'], unique=False)
    op.create_index(op.f('ix_listings_is_featured'), 'listings', ['is_featured'], unique=False)

    # Создаем таблицу избранных объявлений
    op.create_table(
        'listing_favorites',
        sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Связи
        sa.Column('user_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('listing_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),

        # Ограничения
        sa.PrimaryKeyConstraint('id', name=op.f('pk_listing_favorites')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_listing_favorites_user_id_users')),
        sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], name=op.f('fk_listing_favorites_listing_id_listings')),
        sa.UniqueConstraint('user_id', 'listing_id', name=op.f('uq_user_listing_favorite')),
    )

    # Создаем индексы для избранного
    op.create_index(op.f('ix_listing_favorites_user_id'), 'listing_favorites', ['user_id'], unique=False)
    op.create_index(op.f('ix_listing_favorites_listing_id'), 'listing_favorites', ['listing_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем индексы избранного
    op.drop_index(op.f('ix_listing_favorites_listing_id'), table_name='listing_favorites')
    op.drop_index(op.f('ix_listing_favorites_user_id'), table_name='listing_favorites')

    # Удаляем таблицу избранного
    op.drop_table('listing_favorites')

    # Удаляем индексы объявлений
    op.drop_index(op.f('ix_listings_is_featured'), table_name='listings')
    op.drop_index(op.f('ix_listings_status'), table_name='listings')
    op.drop_index(op.f('ix_listings_location'), table_name='listings')
    op.drop_index(op.f('ix_listings_price'), table_name='listings')
    op.drop_index(op.f('ix_listings_category'), table_name='listings')
    op.drop_index(op.f('ix_listings_title'), table_name='listings')
    op.drop_index(op.f('ix_listings_seller_id'), table_name='listings')

    # Удаляем таблицу объявлений
    op.drop_table('listings')

    # Удаляем enum'ы
    op.execute('DROP TYPE IF EXISTS listing_status')
    op.execute('DROP TYPE IF EXISTS listing_category')
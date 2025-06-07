"""add marketplace tables

Revision ID: add_marketplace_tables
Revises: add_moto_clubs_system
Create Date: 2025-06-08 10:00:00.000000

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

    # Создаем enum'ы для маркетплейса
    listing_type_enum = sa.Enum(
        'sale', 'service', 'wanted', 'exchange', 'rent', 'free',
        name='listing_type',
        native_enum=False
    )

    listing_status_enum = sa.Enum(
        'draft', 'active', 'featured', 'inactive', 'expired',
        'sold', 'archived', 'moderation', 'rejected',
        name='listing_status',
        native_enum=False
    )

    # Создаем таблицу категорий объявлений
    op.create_table(
        'listing_categories',
        sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Основная информация
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),

        # Иерархия категорий
        sa.Column('parent_id', advanced_alchemy.types.guid.GUID(length=16), nullable=True),

        # Настройки отображения
        sa.Column('icon', sa.String(length=100), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),

        # Ограничения
        sa.PrimaryKeyConstraint('id', name=op.f('pk_listing_categories')),
        sa.ForeignKeyConstraint(['parent_id'], ['listing_categories.id'],
                                name=op.f('fk_listing_categories_parent_id_listing_categories')),
        sa.UniqueConstraint('slug', name=op.f('uq_listing_categories_slug')),
    )

    # Создаем индексы для категорий
    op.create_index(op.f('ix_listing_categories_name'), 'listing_categories', ['name'], unique=False)
    op.create_index(op.f('ix_listing_categories_slug'), 'listing_categories', ['slug'], unique=True)
    op.create_index(op.f('ix_listing_categories_parent_id'), 'listing_categories', ['parent_id'], unique=False)
    op.create_index(op.f('ix_listing_categories_sort_order'), 'listing_categories', ['sort_order'], unique=False)
    op.create_index(op.f('ix_listing_categories_is_active'), 'listing_categories', ['is_active'], unique=False)

    # Создаем таблицу объявлений
    op.create_table(
        'listings',
        sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Связи
        sa.Column('seller_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('category_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),

        # Основная информация
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),

        # Тип и статус
        sa.Column('listing_type', listing_type_enum, nullable=False),
        sa.Column('status', listing_status_enum, nullable=False, server_default='draft'),

        # Геолокация
        sa.Column('location', sa.String(length=200), nullable=True),
        sa.Column('latitude', sa.Numeric(10, 8), nullable=True),
        sa.Column('longitude', sa.Numeric(11, 8), nullable=True),

        # Контакты
        sa.Column('contact_phone', sa.String(length=20), nullable=True),
        sa.Column('contact_email', sa.String(length=100), nullable=True),

        # Дополнительные поля
        sa.Column('is_negotiable', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('condition', sa.String(length=50), nullable=True),
        sa.Column('brand', sa.String(length=100), nullable=True),
        sa.Column('model', sa.String(length=100), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('mileage', sa.Integer(), nullable=True),

        # Статистика
        sa.Column('is_featured', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('views_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('favorites_count', sa.Integer(), nullable=False, server_default='0'),

        # Время действия
        sa.Column('expires_at', sa.String(length=50), nullable=True),

        # Ограничения
        sa.PrimaryKeyConstraint('id', name=op.f('pk_listings')),
        sa.ForeignKeyConstraint(['seller_id'], ['users.id'], name=op.f('fk_listings_seller_id_users')),
        sa.ForeignKeyConstraint(['category_id'], ['listing_categories.id'],
                                name=op.f('fk_listings_category_id_listing_categories')),
    )

    # Создаем индексы для объявлений
    op.create_index(op.f('ix_listings_seller_id'), 'listings', ['seller_id'], unique=False)
    op.create_index(op.f('ix_listings_category_id'), 'listings', ['category_id'], unique=False)
    op.create_index(op.f('ix_listings_title'), 'listings', ['title'], unique=False)
    op.create_index(op.f('ix_listings_price'), 'listings', ['price'], unique=False)
    op.create_index(op.f('ix_listings_listing_type'), 'listings', ['listing_type'], unique=False)
    op.create_index(op.f('ix_listings_status'), 'listings', ['status'], unique=False)
    op.create_index(op.f('ix_listings_location'), 'listings', ['location'], unique=False)
    op.create_index(op.f('ix_listings_brand'), 'listings', ['brand'], unique=False)
    op.create_index(op.f('ix_listings_model'), 'listings', ['model'], unique=False)
    op.create_index(op.f('ix_listings_year'), 'listings', ['year'], unique=False)
    op.create_index(op.f('ix_listings_is_featured'), 'listings', ['is_featured'], unique=False)
    op.create_index(op.f('ix_listings_expires_at'), 'listings', ['expires_at'], unique=False)

    # Создаем таблицу изображений объявлений
    op.create_table(
        'listing_images',
        sa.Column('id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('sa_orm_sentinel', sa.Integer(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),

        # Связи
        sa.Column('listing_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),
        sa.Column('media_file_id', advanced_alchemy.types.guid.GUID(length=16), nullable=False),

        # Информация об изображении
        sa.Column('url', sa.String(length=1000), nullable=False),
        sa.Column('thumbnail_url', sa.String(length=1000), nullable=True),
        sa.Column('alt_text', sa.String(length=200), nullable=True),

        # Настройки отображения
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default='false'),

        # Метаданные изображения
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),

        # Ограничения
        sa.PrimaryKeyConstraint('id', name=op.f('pk_listing_images')),
        sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], name=op.f('fk_listing_images_listing_id_listings')),
        sa.ForeignKeyConstraint(['media_file_id'], ['media_files.id'],
                                name=op.f('fk_listing_images_media_file_id_media_files')),
    )

    # Создаем индексы для изображений
    op.create_index(op.f('ix_listing_images_listing_id'), 'listing_images', ['listing_id'], unique=False)
    op.create_index(op.f('ix_listing_images_media_file_id'), 'listing_images', ['media_file_id'], unique=False)
    op.create_index(op.f('ix_listing_images_sort_order'), 'listing_images', ['sort_order'], unique=False)
    op.create_index(op.f('ix_listing_images_is_primary'), 'listing_images', ['is_primary'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""

    # Удаляем индексы изображений
    op.drop_index(op.f('ix_listing_images_is_primary'), table_name='listing_images')
    op.drop_index(op.f('ix_listing_images_sort_order'), table_name='listing_images')
    op.drop_index(op.f('ix_listing_images_media_file_id'), table_name='listing_images')
    op.drop_index(op.f('ix_listing_images_listing_id'), table_name='listing_images')

    # Удаляем таблицу изображений
    op.drop_table('listing_images')

    # Удаляем индексы объявлений
    op.drop_index(op.f('ix_listings_expires_at'), table_name='listings')
    op.drop_index(op.f('ix_listings_is_featured'), table_name='listings')
    op.drop_index(op.f('ix_listings_year'), table_name='listings')
    op.drop_index(op.f('ix_listings_model'), table_name='listings')
    op.drop_index(op.f('ix_listings_brand'), table_name='listings')
    op.drop_index(op.f('ix_listings_location'), table_name='listings')
    op.drop_index(op.f('ix_listings_status'), table_name='listings')
    op.drop_index(op.f('ix_listings_listing_type'), table_name='listings')
    op.drop_index(op.f('ix_listings_price'), table_name='listings')
    op.drop_index(op.f('ix_listings_title'), table_name='listings')
    op.drop_index(op.f('ix_listings_category_id'), table_name='listings')
    op.drop_index(op.f('ix_listings_seller_id'), table_name='listings')

    # Удаляем таблицу объявлений
    op.drop_table('listings')

    # Удаляем индексы категорий
    op.drop_index(op.f('ix_listing_categories_is_active'), table_name='listing_categories')
    op.drop_index(op.f('ix_listing_categories_sort_order'), table_name='listing_categories')
    op.drop_index(op.f('ix_listing_categories_parent_id'), table_name='listing_categories')
    op.drop_index(op.f('ix_listing_categories_slug'), table_name='listing_categories')
    op.drop_index(op.f('ix_listing_categories_name'), table_name='listing_categories')

    # Удаляем таблицу категорий
    op.drop_table('listing_categories')

    # Удаляем enum'ы
    op.execute('DROP TYPE IF EXISTS listing_status')
    op.execute('DROP TYPE IF EXISTS listing_type')
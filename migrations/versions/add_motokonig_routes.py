"""add motokonig tables

Revision ID: add_motokonig_routes
Revises: add_marketplace_tables
Create Date: 2025-06-10 22:00:00.000000

"""
from collections.abc import Sequence

import advanced_alchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'add_motokonig_routes'
down_revision: str | None = 'add_marketplace_tables'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add MotoKonig related tables"""

    # Create motokonig_profiles table with UUIDAuditBase fields
    op.create_table(
        'motokonig_profiles',
        sa.Column('id', advanced_alchemy.types.GUID(length=16), nullable=False),
        sa.Column('user_id', advanced_alchemy.types.GUID(length=16), nullable=False),
        sa.Column('nickname', sa.String(30), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('experience_points', sa.Integer(), nullable=False),
        sa.Column('total_distance', sa.Integer(), nullable=False),
        sa.Column('total_rides', sa.Integer(), nullable=False),
        sa.Column('average_speed', sa.Float(), nullable=True),
        sa.Column('max_speed', sa.Float(), nullable=True),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('created_at', advanced_alchemy.types.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.DateTimeUTC(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
        sa.UniqueConstraint('nickname')
    )
    op.create_index(op.f('ix_motokonig_profiles_status'), 'motokonig_profiles', ['status'], unique=False)
    op.create_index(op.f('ix_motokonig_profiles_rating'), 'motokonig_profiles', ['rating'], unique=False)

    # Create rides table with UUIDAuditBase fields
    op.create_table(
        'rides',
        sa.Column('id', advanced_alchemy.types.GUID(length=16), nullable=False),
        sa.Column('organizer_id', advanced_alchemy.types.GUID(length=16), nullable=False),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('difficulty', sa.Integer(), nullable=False),
        sa.Column('planned_distance', sa.Integer(), nullable=False),
        sa.Column('max_participants', sa.Integer(), nullable=False),
        sa.Column('start_location', sa.String(200), nullable=False),
        sa.Column('end_location', sa.String(200), nullable=False),
        sa.Column('planned_start', sa.DateTime(timezone=True), nullable=False),
        sa.Column('planned_duration', sa.Integer(), nullable=False),
        sa.Column('actual_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('actual_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('actual_distance', sa.Integer(), nullable=True),
        sa.Column('route_gpx', sa.Text(), nullable=True),
        sa.Column('weather_conditions', sa.String(200), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.DateTimeUTC(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['organizer_id'], ['motokonig_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rides_planned_start'), 'rides', ['planned_start'], unique=False)
    op.create_index(op.f('ix_rides_is_completed'), 'rides', ['is_completed'], unique=False)

    # Create motokonig_achievements table with UUIDAuditBase fields
    op.create_table(
        'motokonig_achievements',
        sa.Column('id', advanced_alchemy.types.GUID(length=16), nullable=False),
        sa.Column('motokonig_id', advanced_alchemy.types.GUID(length=16), nullable=False),
        sa.Column('achievement_type', sa.String(50), nullable=False),
        sa.Column('earned_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('extra_data', sa.JSON(), nullable=True),
        sa.Column('created_at', advanced_alchemy.types.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.DateTimeUTC(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['motokonig_id'], ['motokonig_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('motokonig_id', 'achievement_type', name='uq_motokonig_achievement_type')
    )

    # Create ride_participants table with UUIDAuditBase fields
    op.create_table(
        'ride_participants',
        sa.Column('id', advanced_alchemy.types.GUID(length=16), nullable=False),
        sa.Column('ride_id', advanced_alchemy.types.GUID(length=16), nullable=False),
        sa.Column('motokonig_id', advanced_alchemy.types.GUID(length=16), nullable=False),
        sa.Column('joined_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('left_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('distance_covered', sa.Integer(), nullable=False),
        sa.Column('average_speed', sa.Float(), nullable=True),
        sa.Column('max_speed', sa.Float(), nullable=True),
        sa.Column('is_leader', sa.Boolean(), nullable=False),
        sa.Column('created_at', advanced_alchemy.types.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.DateTimeUTC(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['ride_id'], ['rides.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['motokonig_id'], ['motokonig_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ride_id', 'motokonig_id', name='uq_ride_participant')
    )

    # Create ride_checkpoints table with UUIDAuditBase fields
    op.create_table(
        'ride_checkpoints',
        sa.Column('id', advanced_alchemy.types.GUID(length=16), nullable=False),
        sa.Column('ride_id', advanced_alchemy.types.GUID(length=16), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('name', sa.String(100), nullable=True),
        sa.Column('reached_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('created_at', advanced_alchemy.types.DateTimeUTC(timezone=True), nullable=False),
        sa.Column('updated_at', advanced_alchemy.types.DateTimeUTC(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['ride_id'], ['rides.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ride_checkpoints_order'), 'ride_checkpoints', ['ride_id', 'order_index'], unique=False)


def downgrade() -> None:
    """Drop MotoKonig related tables"""
    op.drop_index(op.f('ix_ride_checkpoints_order'), table_name='ride_checkpoints')
    op.drop_table('ride_checkpoints')
    op.drop_table('ride_participants')
    op.drop_table('motokonig_achievements')
    op.drop_index(op.f('ix_rides_is_completed'), table_name='rides')
    op.drop_index(op.f('ix_rides_planned_start'), table_name='rides')
    op.drop_table('rides')
    op.drop_index(op.f('ix_motokonig_profiles_rating'), table_name='motokonig_profiles')
    op.drop_index(op.f('ix_motokonig_profiles_status'), table_name='motokonig_profiles')
    op.drop_table('motokonig_profiles')

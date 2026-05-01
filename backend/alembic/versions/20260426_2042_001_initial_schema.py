"""initial schema

Revision ID: 001
Revises: 
Create Date: 2026-04-26 20:42:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    
    # Create tracked_products table
    op.create_table(
        'tracked_products',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('product_name', sa.String(length=500), nullable=False),
        sa.Column('product_url', sa.Text(), nullable=False),
        sa.Column('current_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('price_threshold', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=10), nullable=False),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_checked', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_tracked_products_user_id', 'tracked_products', ['user_id'], unique=False)
    op.create_index('idx_tracked_products_last_checked', 'tracked_products', ['last_checked'], unique=False)
    
    # Create price_history table
    op.create_table(
        'price_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tracked_product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('checked_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['tracked_product_id'], ['tracked_products.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_price_history_product_id', 'price_history', ['tracked_product_id'], unique=False)
    op.create_index('idx_price_history_checked_at', 'price_history', ['checked_at'], unique=False)
    
    # Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tracked_product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('old_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('new_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('sent_at', sa.DateTime(), nullable=False),
        sa.Column('delivery_status', sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tracked_product_id'], ['tracked_products.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_notifications_user_id', 'notifications', ['user_id'], unique=False)
    op.create_index('idx_notifications_sent_at', 'notifications', ['sent_at'], unique=False)
    
    # Create platform_errors table
    op.create_table(
        'platform_errors',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('error_type', sa.String(length=100), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('occurred_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_platform_errors_occurred_at', 'platform_errors', ['occurred_at'], unique=False)
    op.create_index('idx_platform_errors_platform', 'platform_errors', ['platform'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign key constraints)
    op.drop_index('idx_platform_errors_platform', table_name='platform_errors')
    op.drop_index('idx_platform_errors_occurred_at', table_name='platform_errors')
    op.drop_table('platform_errors')
    
    op.drop_index('idx_notifications_sent_at', table_name='notifications')
    op.drop_index('idx_notifications_user_id', table_name='notifications')
    op.drop_table('notifications')
    
    op.drop_index('idx_price_history_checked_at', table_name='price_history')
    op.drop_index('idx_price_history_product_id', table_name='price_history')
    op.drop_table('price_history')
    
    op.drop_index('idx_tracked_products_last_checked', table_name='tracked_products')
    op.drop_index('idx_tracked_products_user_id', table_name='tracked_products')
    op.drop_table('tracked_products')
    
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')

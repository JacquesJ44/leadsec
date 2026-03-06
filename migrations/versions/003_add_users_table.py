"""Add users table

Revision ID: 003
Revises: 001
Create Date: 2026-02-25 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(length=150), nullable=False, unique=True),
        sa.Column('email', sa.String(length=255), nullable=True, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=func.now()),
    )


def downgrade():
    op.drop_table('users')

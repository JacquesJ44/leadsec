"""Fix image_data column to support larger images

Revision ID: 002
Revises: 001
Create Date: 2026-02-23 17:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Alter the image_data column to use LONGTEXT
    # MySQL doesn't support direct Text -> LongText conversion, so we drop and recreate
    from sqlalchemy import text
    op.execute(text('ALTER TABLE invoice_images MODIFY COLUMN image_data LONGTEXT'))


def downgrade():
    # Revert to Text
    from sqlalchemy import text
    op.execute(text('ALTER TABLE invoice_images MODIFY COLUMN image_data TEXT'))

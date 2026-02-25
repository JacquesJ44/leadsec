"""Add invoice_images table

Revision ID: 001
Revises: 
Create Date: 2026-02-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the invoice_images table
    op.create_table(
        'invoice_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('jobcard_id', sa.Integer(), nullable=False),
        sa.Column('image_data', sa.Text().with_variant(sa.dialects.mysql.LONGTEXT(), 'mysql'), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('send_to_client', sa.Boolean(), nullable=False),
        sa.Column('upload_timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['jobcard_id'], ['jobcards.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_invoice_images_jobcard_id'), 'invoice_images', ['jobcard_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_invoice_images_jobcard_id'), table_name='invoice_images')
    op.drop_table('invoice_images')

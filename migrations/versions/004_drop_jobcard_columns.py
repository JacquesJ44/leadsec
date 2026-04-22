"""Drop columns from jobcards table: client_email, client_phone, cost_estimate, client_signature

Revision ID: 004
Revises: 003
Create Date: 2026-04-21 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('jobcards') as batch_op:
        batch_op.drop_column('client_email')
        batch_op.drop_column('client_phone')
        batch_op.drop_column('cost_estimate')
        batch_op.drop_column('client_signature')

def downgrade():
    with op.batch_alter_table('jobcards') as batch_op:
        batch_op.add_column(sa.Column('client_email', sa.String(255), nullable=False))
        batch_op.add_column(sa.Column('client_phone', sa.String(20)))
        batch_op.add_column(sa.Column('cost_estimate', sa.Numeric(10, 2)))
        batch_op.add_column(sa.Column('client_signature', sa.Text))

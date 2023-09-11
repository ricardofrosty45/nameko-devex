"""init

Revision ID: 94906b42fedf
Revises: 51552872ec8b
Create Date: 2023-09-11 19:07:08.803000

"""

# revision identifiers, used by Alembic.
revision = '94906b42fedf'
down_revision = '51552872ec8b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_order_details_order_id', table_name='order_details')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_order_details_order_id', 'order_details', ['order_id'], unique=False)
    # ### end Alembic commands ###
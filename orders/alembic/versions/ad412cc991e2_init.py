"""init

Revision ID: ad412cc991e2
Revises: dd33cb03d01f
Create Date: 2023-09-05 17:07:24.699304

"""

# revision identifiers, used by Alembic.
revision = 'ad412cc991e2'
down_revision = 'dd33cb03d01f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_details', 'product_id',
               existing_type=sa.VARCHAR(),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_details', 'product_id',
               existing_type=sa.String(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    # ### end Alembic commands ###
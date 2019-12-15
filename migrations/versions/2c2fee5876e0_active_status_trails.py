"""active status trails

Revision ID: 2c2fee5876e0
Revises: 4b1cce66e293
Create Date: 2019-12-15 14:33:58.775684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c2fee5876e0'
down_revision = '4b1cce66e293'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trails', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trails', 'active')
    # ### end Alembic commands ###
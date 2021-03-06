"""reported table

Revision ID: cbb52787c330
Revises: c7acbb09501c
Create Date: 2019-12-18 19:31:47.352000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbb52787c330'
down_revision = 'c7acbb09501c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reporters',
    sa.Column('reporter_id', sa.Integer(), nullable=True),
    sa.Column('reported_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['reported_id'], ['status.id'], ),
    sa.ForeignKeyConstraint(['reporter_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reporters')
    # ### end Alembic commands ###

"""subscribers table

Revision ID: 626becf9e5b6
Revises: e2f64baedeb1
Create Date: 2019-12-09 19:12:17.130000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '626becf9e5b6'
down_revision = 'e2f64baedeb1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscribers',
    sa.Column('subscriber_id', sa.Integer(), nullable=True),
    sa.Column('subscribed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subscribed_id'], ['trails.id'], ),
    sa.ForeignKeyConstraint(['subscriber_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscribers')
    # ### end Alembic commands ###
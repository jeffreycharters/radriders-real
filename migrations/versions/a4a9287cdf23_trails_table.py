"""trails table

Revision ID: a4a9287cdf23
Revises: c68ede7dc820
Create Date: 2019-12-05 18:19:03.578000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4a9287cdf23'
down_revision = 'c68ede7dc820'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trails_name'), 'trails', ['name'], unique=False)
    op.add_column('status', sa.Column('trail_system', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'status', 'trails', ['trail_system'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'status', type_='foreignkey')
    op.drop_column('status', 'trail_system')
    op.drop_index(op.f('ix_trails_name'), table_name='trails')
    op.drop_table('trails')
    # ### end Alembic commands ###

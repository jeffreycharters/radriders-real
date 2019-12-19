"""status remove reported

Revision ID: c7acbb09501c
Revises: 7f17e8d46069
Create Date: 2019-12-18 19:22:33.275000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c7acbb09501c'
down_revision = '7f17e8d46069'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('status', 'trail_system',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('status', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_column('status', 'reported')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('status', sa.Column('reported', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.alter_column('status', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('status', 'trail_system',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    # ### end Alembic commands ###
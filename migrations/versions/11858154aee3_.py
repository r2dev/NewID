"""empty message

Revision ID: 11858154aee3
Revises: ddc0976b21f
Create Date: 2015-07-16 11:38:15.177000

"""

# revision identifiers, used by Alembic.
revision = '11858154aee3'
down_revision = 'ddc0976b21f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('alibaba', sa.String(length=30), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'alibaba')
    ### end Alembic commands ###
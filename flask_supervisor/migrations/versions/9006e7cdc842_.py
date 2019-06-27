"""empty message

Revision ID: 9006e7cdc842
Revises: 11cb4ab0e684
Create Date: 2019-06-21 10:14:48.257962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9006e7cdc842'
down_revision = '11cb4ab0e684'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('host_info', table_name='sv_hosts')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('host_info', 'sv_hosts', ['host_info'], unique=True)
    # ### end Alembic commands ###
"""empty message

Revision ID: 83e7aa52e848
Revises: 66176ec42974
Create Date: 2019-05-09 16:04:55.806640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83e7aa52e848'
down_revision = '66176ec42974'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sv_userGroups',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sv_roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('roleName', sa.String(length=120), nullable=False),
    sa.Column('sv_userGroup_Id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sv_userGroup_Id'], ['sv_userGroups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sv_roles_roleName'), 'sv_roles', ['roleName'], unique=True)
    op.create_table('sv_navs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('navTitle', sa.String(length=120), nullable=False),
    sa.Column('navUrl', sa.String(length=120), nullable=True),
    sa.Column('navType', sa.Boolean(), nullable=True),
    sa.Column('is_del', sa.Boolean(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['sv_roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('navTitle')
    )
    op.create_index(op.f('ix_sv_navs_navUrl'), 'sv_navs', ['navUrl'], unique=False)
    op.create_table('users_groups',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('userGroup_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['userGroup_id'], ['sv_userGroups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['sv_users.id'], )
    )
    op.create_table('sv_subnavs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('nav_url', sa.String(length=200), nullable=False),
    sa.Column('nav_Id', sa.Integer(), nullable=True),
    sa.Column('is_del', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['nav_Id'], ['sv_navs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sv_subnavs_nav_url'), 'sv_subnavs', ['nav_url'], unique=True)
    op.create_index(op.f('ix_sv_subnavs_title'), 'sv_subnavs', ['title'], unique=True)
    op.add_column('sv_users', sa.Column('userGroup_Id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'sv_users', 'sv_userGroups', ['userGroup_Id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sv_users', type_='foreignkey')
    op.drop_column('sv_users', 'userGroup_Id')
    op.drop_index(op.f('ix_sv_subnavs_title'), table_name='sv_subnavs')
    op.drop_index(op.f('ix_sv_subnavs_nav_url'), table_name='sv_subnavs')
    op.drop_table('sv_subnavs')
    op.drop_table('users_groups')
    op.drop_index(op.f('ix_sv_navs_navUrl'), table_name='sv_navs')
    op.drop_table('sv_navs')
    op.drop_index(op.f('ix_sv_roles_roleName'), table_name='sv_roles')
    op.drop_table('sv_roles')
    op.drop_table('sv_userGroups')
    # ### end Alembic commands ###
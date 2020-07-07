"""init commit

Revision ID: ed84d6b0b6f5
Revises: 
Create Date: 2020-07-07 16:56:59.110226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed84d6b0b6f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_role',
    sa.Column('role_id', sa.Integer(), nullable=False, comment='角色Id'),
    sa.Column('role_name', sa.String(length=64), nullable=True, comment='角色名字'),
    sa.Column('permission_id', sa.BIGINT(), nullable=True, comment='权限ID'),
    sa.PrimaryKeyConstraint('role_id')
    )
    op.create_index(op.f('ix_admin_role_role_id'), 'admin_role', ['role_id'], unique=False)
    op.create_table('admin_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=32), nullable=True, comment='用户id'),
    sa.Column('email', sa.String(length=128), nullable=False, comment='邮箱'),
    sa.Column('phone', sa.VARCHAR(length=16), nullable=False, comment='手机号'),
    sa.Column('nickname', sa.String(length=128), nullable=True, comment='用户昵称'),
    sa.Column('hashed_password', sa.String(length=128), nullable=False, comment='密码'),
    sa.Column('is_active', sa.Boolean(), nullable=True, comment='是否激活'),
    sa.Column('role_id', sa.Integer(), nullable=True, comment='角色表'),
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('update_time', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.Column('is_delete', sa.Integer(), nullable=True, comment='逻辑删除:0=未删除,1=删除'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_user_email'), 'admin_user', ['email'], unique=True)
    op.create_index(op.f('ix_admin_user_id'), 'admin_user', ['id'], unique=False)
    op.create_index(op.f('ix_admin_user_phone'), 'admin_user', ['phone'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_admin_user_phone'), table_name='admin_user')
    op.drop_index(op.f('ix_admin_user_id'), table_name='admin_user')
    op.drop_index(op.f('ix_admin_user_email'), table_name='admin_user')
    op.drop_table('admin_user')
    op.drop_index(op.f('ix_admin_role_role_id'), table_name='admin_role')
    op.drop_table('admin_role')
    # ### end Alembic commands ###
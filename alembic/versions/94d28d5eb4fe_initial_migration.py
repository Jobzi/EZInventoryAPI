"""Initial migration

Revision ID: 94d28d5eb4fe
Revises: 
Create Date: 2021-05-06 19:41:47.902229

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '94d28d5eb4fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'DELETED', name='statusconstants'), nullable=True),
    sa.Column('activated_on', sa.DateTime(), nullable=True),
    sa.Column('deleted_on', sa.DateTime(), nullable=True),
    sa.Column('reactivated_on', sa.DateTime(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('customer',
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'DELETED', name='statusconstants'), nullable=True),
    sa.Column('activated_on', sa.DateTime(), nullable=True),
    sa.Column('deleted_on', sa.DateTime(), nullable=True),
    sa.Column('reactivated_on', sa.DateTime(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('dni', sa.String(length=20), nullable=False),
    sa.Column('dni_type', sa.Enum('STANDARD', 'RUC', 'PASSPORT', name='dnitypes'), nullable=True),
    sa.Column('main_address', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('permision_template',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('detail', sa.String(), nullable=True),
    sa.Column('resources', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('product_template',
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'DELETED', name='statusconstants'), nullable=True),
    sa.Column('activated_on', sa.DateTime(), nullable=True),
    sa.Column('deleted_on', sa.DateTime(), nullable=True),
    sa.Column('reactivated_on', sa.DateTime(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('public_unit_price', sa.Integer(), nullable=False),
    sa.Column('provicer_unit_price', sa.Integer(), nullable=False),
    sa.Column('reorder_level', sa.Integer(), nullable=True),
    sa.Column('reorder_ammount', sa.Integer(), nullable=True),
    sa.Column('picture_path', sa.String(), nullable=True),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('provider',
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'DELETED', name='statusconstants'), nullable=True),
    sa.Column('activated_on', sa.DateTime(), nullable=True),
    sa.Column('deleted_on', sa.DateTime(), nullable=True),
    sa.Column('reactivated_on', sa.DateTime(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('main_address', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('role',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('permissions', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'DELETED', name='statusconstants'), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('tenant',
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'DELETED', name='statusconstants'), nullable=True),
    sa.Column('activated_on', sa.DateTime(), nullable=True),
    sa.Column('deleted_on', sa.DateTime(), nullable=True),
    sa.Column('reactivated_on', sa.DateTime(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('main_address', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('user',
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'DELETED', name='statusconstants'), nullable=True),
    sa.Column('activated_on', sa.DateTime(), nullable=True),
    sa.Column('deleted_on', sa.DateTime(), nullable=True),
    sa.Column('reactivated_on', sa.DateTime(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('username', sa.String(length=200), nullable=False),
    sa.Column('password', sa.String(length=300), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('product',
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'DELETED', name='statusconstants'), nullable=True),
    sa.Column('activated_on', sa.DateTime(), nullable=True),
    sa.Column('deleted_on', sa.DateTime(), nullable=True),
    sa.Column('reactivated_on', sa.DateTime(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('public_unit_price', sa.Integer(), nullable=False),
    sa.Column('provicer_unit_price', sa.Integer(), nullable=False),
    sa.Column('reorder_level', sa.Integer(), nullable=True),
    sa.Column('reorder_ammount', sa.Integer(), nullable=True),
    sa.Column('picture_path', sa.String(), nullable=True),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('tenant_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('category_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['category_uuid'], ['category.uuid'], ),
    sa.ForeignKeyConstraint(['tenant_uuid'], ['tenant.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('user_roles_by_tenant',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('tenant_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('role_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_uuid'], ['role.uuid'], ),
    sa.ForeignKeyConstraint(['tenant_uuid'], ['tenant.uuid'], ),
    sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('invoice',
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'DELETED', name='statusconstants'), nullable=True),
    sa.Column('activated_on', sa.DateTime(), nullable=True),
    sa.Column('deleted_on', sa.DateTime(), nullable=True),
    sa.Column('reactivated_on', sa.DateTime(), nullable=True),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('product_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('customer_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('product_ammount', sa.Integer(), nullable=False),
    sa.Column('product_unit_price', sa.Integer(), nullable=False),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['customer_uuid'], ['provider.uuid'], ),
    sa.ForeignKeyConstraint(['product_uuid'], ['product.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('product_providers',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('product_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('provider_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['product_uuid'], ['product.uuid'], ),
    sa.ForeignKeyConstraint(['provider_uuid'], ['provider.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('stock',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('product_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('current_ammount', sa.Integer(), nullable=False),
    sa.Column('changed_by', sa.Integer(), nullable=False),
    sa.Column('operation', sa.Enum('ADD', 'REMOVE', name='operationconstants'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_uuid'], ['product.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock')
    op.drop_table('product_providers')
    op.drop_table('invoice')
    op.drop_table('user_roles_by_tenant')
    op.drop_table('product')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('tenant')
    op.drop_table('role')
    op.drop_table('provider')
    op.drop_table('product_template')
    op.drop_table('permision_template')
    op.drop_table('customer')
    op.drop_table('category')
    # ### end Alembic commands ###

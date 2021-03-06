"""add unique together constraints

Revision ID: 9dd152edd913
Revises: e205992a2fff
Create Date: 2021-06-30 17:12:48.642488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dd152edd913'
down_revision = 'e205992a2fff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('product_providers_unique_constraint', 'product_providers', ['product_uuid', 'provider_uuid'])
    op.create_unique_constraint('user_roles_by_tenant_unique_constraint', 'user_roles_by_tenant', ['tenant_uuid', 'role_uuid', 'user_uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_roles_by_tenant_unique_constraint', 'user_roles_by_tenant', type_='unique')
    op.drop_constraint('product_providers_unique_constraint', 'product_providers', type_='unique')
    # ### end Alembic commands ###

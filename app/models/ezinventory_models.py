import uuid
from datetime import datetime

import sqlalchemy as sqla
from app.db.postgre_connector import PostgreSqlConnector
from app.db.translators.guuid import GUUID
from app.utils.constants import DniTypes, OperationConstants, StatusConstants
from passlib.hash import bcrypt
from sqlalchemy.orm import backref, relationship


class BaseTable(PostgreSqlConnector.Base):
    __abstract__ = True

    created_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow)
    updated_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    status = sqla.Column(sqla.Enum(StatusConstants), default=StatusConstants.ACTIVE)
    activated_on = sqla.Column(sqla.DateTime(), nullable=True)
    deleted_on = sqla.Column(sqla.DateTime(), nullable=True)
    reactivated_on = sqla.Column(sqla.DateTime(), nullable=True)


class Tenant(BaseTable):
    __tablename__ = 'tenant'

    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(100), nullable=False)
    main_address = sqla.Column(sqla.JSON(none_as_null=False), nullable=False)
    phone = sqla.Column(sqla.String(15))
    email = sqla.Column(sqla.String(), nullable=False)
    description = sqla.Column(sqla.String())

    def __repr__(self) -> str:
        return f'Tenant[{self.uuid}] {self.name}'


class User(BaseTable):
    __tablename__ = 'user'

    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = sqla.Column(sqla.String(200), nullable=False, unique=True, index=True)
    password = sqla.Column(sqla.String(300), nullable=False)
    email = sqla.Column(sqla.String(), nullable=False)
    phone = sqla.Column(sqla.String(15))

    roles_by_tenant = relationship('UserRolesByTenant')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.password:
            self.password = bcrypt.hash(self.password)

    def __repr__(self) -> str:
        return f'User[{self.uuid}] {self.name}'

    def validate_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password)

    def set_password(self, password: str) -> None:
        if password:
            self.password = bcrypt.hash(password)


class Role(PostgreSqlConnector.Base):
    __tablename__ = 'role'

    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(100), nullable=False)
    permissions = sqla.Column(sqla.JSON(none_as_null=False), nullable=False)
    status = sqla.Column(sqla.Enum(StatusConstants), default=StatusConstants.ACTIVE)

    def __repr__(self) -> str:
        return f'Role[{self.uuid}] {self.name}'


class UserRolesByTenant(PostgreSqlConnector.Base):
    __tablename__ = 'user_roles_by_tenant'

    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    tenant_uuid = sqla.Column(GUUID(), sqla.ForeignKey('tenant.uuid'))
    user_uuid = sqla.Column(GUUID(), sqla.ForeignKey('user.uuid'))
    role_uuid = sqla.Column(GUUID(), sqla.ForeignKey('role.uuid'))
    created_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow)

    user = relationship(
        'User',
        primaryjoin=f"and_(UserRolesByTenant.user_uuid==User.uuid, User.status!='{StatusConstants.DELETED.value}')",
        back_populates='roles_by_tenant'
    )

    role = relationship(
        'Role',
        primaryjoin=f"and_(UserRolesByTenant.role_uuid==Role.uuid, Role.status!='{StatusConstants.DELETED.value}')"
    )

    tenant = relationship(
        'Tenant',
        primaryjoin=f"and_(UserRolesByTenant.tenant_uuid==Tenant.uuid, Tenant.status!='{StatusConstants.DELETED.value}')",
    )

    __table_args__ = (sqla.UniqueConstraint('tenant_uuid', 'role_uuid', 'user_uuid', name='user_roles_by_tenant_unique_constraint'),)

    def __repr__(self) -> str:
        return f'UserRoleBytenant[{self.uuid}] tenant={self.tenant_uuid} user={self.user_uuid}'


class PermisionTemplate(PostgreSqlConnector.Base):
    __tablename__ = 'permision_template'

    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(100), nullable=False, unique=True)
    detail = sqla.Column(sqla.String(), nullable=True)
    resources = sqla.Column(sqla.JSON(none_as_null=False), nullable=False)

    def __repr__(self) -> str:
        return f'PermisionTemplate[{self.uuid}] {self.name}'


class ProductBase(BaseTable):
    __abstract__ = True

    name = sqla.Column(sqla.String(100), nullable=False)
    description = sqla.Column(sqla.String())
    # NOTE: We store prices as an integer ammount of cents to avoid presicion errors
    public_unit_price = sqla.Column(sqla.Integer(), nullable=False)
    provicer_unit_price = sqla.Column(sqla.Integer(), nullable=False)
    reorder_level = sqla.Column(sqla.Integer(), nullable=True)
    reorder_ammount = sqla.Column(sqla.Integer(), nullable=True)
    picture_path = sqla.Column(sqla.String(), nullable=True)
    meta = sqla.Column(sqla.JSON(none_as_null=False), nullable=False)


class ProductTemplate(ProductBase):
    __tablename__ = 'product_template'
    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'ProductTemplate[{self.uuid}] {self.name}'


class Product(ProductBase):
    __tablename__ = 'product'

    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    tenant_uuid = sqla.Column(GUUID(), sqla.ForeignKey('tenant.uuid'))
    category_uuid = sqla.Column(GUUID(), sqla.ForeignKey('category.uuid'))

    tenant = relationship(
        'Tenant',
        primaryjoin=f"and_(Product.tenant_uuid==Tenant.uuid, Tenant.status!='{StatusConstants.DELETED.value}')",
        backref=backref('products'))

    category = relationship(
        'Category',
        primaryjoin=f"and_(Product.category_uuid==Category.uuid, Category.status!='{StatusConstants.DELETED.value}')",
        backref=backref('products'))

    def __repr__(self) -> str:
        return f'Product[{self.uuid}] {self.name}'


class Stock(PostgreSqlConnector.Base):
    __tablename__ = 'stock'

    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    product_uuid = sqla.Column(GUUID(), sqla.ForeignKey('product.uuid'), nullable=False)
    user_uuid = sqla.Column(GUUID(), sqla.ForeignKey('user.uuid'), nullable=False)
    provider_uuid = sqla.Column(GUUID(), default=None, nullable=True)
    current_ammount = sqla.Column(sqla.Integer(), nullable=False)
    changed_by = sqla.Column(sqla.Integer(), nullable=False)
    operation = sqla.Column(sqla.Enum(OperationConstants))
    updated_at = sqla.Column(sqla.DateTime(), default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Stock[{self.uuid}] {self.product_uuid}'


class Category(BaseTable):
    __tablename__ = 'category'

    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(100), nullable=False)
    description = sqla.Column(sqla.String())

    def __repr__(self) -> str:
        return f'Category[{self.uuid}] {self.name}'


class Provider(BaseTable):
    __tablename__ = 'provider'

    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(100), nullable=False)
    main_address = sqla.Column(sqla.JSON(none_as_null=False), nullable=False)
    phone = sqla.Column(sqla.String(15))
    email = sqla.Column(sqla.String(), nullable=False)
    description = sqla.Column(sqla.String())
    meta = sqla.Column(sqla.JSON(none_as_null=False), nullable=True)

    def __repr__(self) -> str:
        return f'Category[{self.uuid}] {self.name}'


class ProductProviders(PostgreSqlConnector.Base):
    __tablename__ = 'product_providers'

    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    product_uuid = sqla.Column(GUUID(), sqla.ForeignKey('product.uuid'))
    provider_uuid = sqla.Column(GUUID(), sqla.ForeignKey('provider.uuid'))

    product = relationship(
        'Product',
        primaryjoin=f"and_(ProductProviders.product_uuid==Product.uuid, Product.status!='{StatusConstants.DELETED.value}')",
        backref=backref('providers', order_by=uuid))

    provider = relationship(
        'Provider',
        primaryjoin=f"and_(ProductProviders.provider_uuid==Provider.uuid, Provider.status!='{StatusConstants.DELETED.value}')",
        backref=backref('products', order_by=uuid))

    __table_args__ = (sqla.UniqueConstraint('product_uuid', 'provider_uuid', name='product_providers_unique_constraint'),)

    def __repr__(self) -> str:
        return f'ProductProviders[{self.uuid}] provider={self.provider_uuid} product={self.product_uuid}'


class Customer(BaseTable):
    __tablename__ = 'customer'

    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = sqla.Column(sqla.String(200), nullable=False)
    dni = sqla.Column(sqla.String(20), nullable=False)
    dni_type = sqla.Column(sqla.Enum(DniTypes))
    main_address = sqla.Column(sqla.JSON(none_as_null=False), nullable=False)
    phone = sqla.Column(sqla.String(15))
    email = sqla.Column(sqla.String(), nullable=False)
    description = sqla.Column(sqla.String())
    meta = sqla.Column(sqla.JSON(none_as_null=False), nullable=True)

    def __repr__(self) -> str:
        return f'Customer[{self.uuid}] {self.name}'


class Invoice(BaseTable):
    __tablename__ = 'invoice'

    uuid = sqla.Column(GUUID(), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    product_uuid = sqla.Column(GUUID(), sqla.ForeignKey('product.uuid'), nullable=False)
    customer_uuid = sqla.Column(GUUID(), sqla.ForeignKey('customer.uuid'), nullable=False)
    user_uuid = sqla.Column(GUUID(), sqla.ForeignKey('user.uuid'), nullable=False)
    product_ammount = sqla.Column(sqla.Integer(), nullable=False)
    # NOTE: We store prices as an integer ammount of cents to avoid presicion errors
    product_unit_price = sqla.Column(sqla.Integer(), nullable=False)
    meta = sqla.Column(sqla.JSON(none_as_null=False), nullable=True)

    product = relationship(
        'Product',
        backref=backref('invoices', order_by=uuid))

    customer = relationship(
        'Customer',
        backref=backref('invoices', order_by=uuid))

    def __repr__(self) -> str:
        return f'Invoice[{self.uuid}] customer={self.customer_uuid} product={self.product_uuid}'

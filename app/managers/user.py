from typing import List, Union

from app.models.ezinventory_models import User, UserRolesByTenant
from app.serializers.user import UserCreate
from app.utils.constants import StatusConstants
from app.utils.functions import filter_dict_keys
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from .base import BaseManager


class UserManager(BaseManager):
    model = User

    @classmethod
    async def fetch_by_uuid(cls, db: AsyncSession, uuid: str, filter_status: str = StatusConstants.DELETED) -> Union[User, None]:
        query = select(User)\
            .options(subqueryload(User.roles_by_tenant).subqueryload('role'))\
            .where(User.uuid == uuid, User.status != filter_status)
        result = await cls.execute_stmt(db, query)
        return result.scalars().first()

    @classmethod
    async def add_roles_by_tenant_to_user(cls, db: AsyncSession, user_uuid: str, tenant_uuid: str, roles: set) -> Union[UserRolesByTenant, None]:
        user_roles_by_tenant = [
            UserRolesByTenant(
                user_uuid=user_uuid,
                tenant_uuid=tenant_uuid,
                role_uuid=role_uuid
            ) for role_uuid in roles]
        return cls.add_to_session(db, user_roles_by_tenant)

    @classmethod
    async def create_user(cls, db: AsyncSession, user: UserCreate) -> Union[User, None]:
        user_dict = filter_dict_keys(user.dict(), {'roles', 'tenant_uuid'})
        db_user = cls.add_to_session(db, User(**user_dict))

        if user.tenant_uuid and user.roles:
            await cls.add_roles_by_tenant_to_user(db, db_user.uuid, user.tenant_uuid, set(user.roles))

        await db.commit()
        await db.refresh(db_user)
        return db_user

    @classmethod
    def group_permissions_by_tenant(cls, user_roles_by_tenant: List[UserRolesByTenant]) -> Union[User, None]:
        permissions_by_tenant = dict()
        for role_by_tenant in user_roles_by_tenant:
            if (tenant_uuid := str(role_by_tenant.tenant_uuid)) not in permissions_by_tenant:
                permissions_by_tenant[tenant_uuid] = list()
            permissions_by_tenant[tenant_uuid].extend(role_by_tenant.role.permissions)
        return permissions_by_tenant

    @classmethod
    async def fetch_active_user_by_username(cls, db: AsyncSession, username: str) -> Union[User, None]:
        query = select(User)\
            .options(subqueryload(User.roles_by_tenant).subqueryload('role'))\
            .where(User.username == username, User.status == StatusConstants.ACTIVE)
        result = await cls.execute_stmt(db, query)
        return result.scalars().first()

    @classmethod
    async def authenticate_user(cls, db: AsyncSession, username: str, password: str) -> Union[User, None]:
        user = await cls.fetch_active_user_by_username(db, username)
        return user if user and user.validate_password(password) else None

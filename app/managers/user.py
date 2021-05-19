from typing import Union

from app.models.ezinventory_models import User, UserRolesByTenant
from app.serializers.user import UserCreate
from app.utils.constants import StatusConstants
from app.utils.functions import filter_dict_keys
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseManager


class UserManager(BaseManager):
    model = User

    @classmethod
    async def fetch_by_uuid(cls, db: AsyncSession, uuid: str, filter_status: str = StatusConstants.DELETED) -> Union[User, None]:
        query = select(User).where(User.uuid == uuid, User.status != filter_status)
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

from typing import Union

from app.models.ezinventory_models import Role
from app.serializers.role import RoleCreate
from app.utils.constants import StatusConstants
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseManager


class RoleManager(BaseManager):
    model = Role

    @classmethod
    async def fetch_by_uuid(cls, db: AsyncSession, uuid: str, filtered_status: str = StatusConstants.DELETED) -> Union[Role, None]:
        query = select(Role).where(Role.uuid == uuid, Role.status != filtered_status)
        result = await cls.execute_stmt(db, query)
        return result.scalars().first()

    @classmethod
    async def create_role(cls, db: AsyncSession, role: RoleCreate) -> Union[Role, None]:
        db_role = cls.add_to_session(db, Role(**role.dict()))

        await db.commit()
        await db.refresh(db_role)
        return db_role

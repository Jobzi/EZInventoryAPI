from typing import Union

from app.models.ezinventory_models import Category
from app.serializers.category import CategoryCreate
from app.utils.constants import StatusConstants
from app.utils.functions import filter_dict_keys
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseManager


class CategoryManager(BaseManager):
    model = Category

    @classmethod
    async def fetch_by_uuid(cls, db: AsyncSession, uuid: str, filtered_status: str = StatusConstants.DELETED) -> Union[Category, None]:
        query = select(Category).where(Category.uuid == uuid, Category.status != filtered_status)
        result = await cls.execute_stmt(db, query)
        return result.scalars().first()

    @classmethod
    async def create_category(cls, db: AsyncSession, category: CategoryCreate) -> Union[Category, None]:
        db_category = cls.add_to_session(db, Category(**category.dict()))

        await db.commit()
        await db.refresh(db_category)
        return db_category

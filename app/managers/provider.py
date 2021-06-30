from datetime import datetime
from typing import List, Union

from app.models.ezinventory_models import ProductProviders, Provider
from app.serializers.provider import ProviderCreate
from app.utils.constants import StatusConstants
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from .base import BaseManager


class ProviderManager(BaseManager):
    model = Provider
    columns = Provider.__table__.columns

    @classmethod
    async def fetch_by_uuid(cls, db: AsyncSession, uuid: str, filtered_status: str = StatusConstants.DELETED) -> Union[Provider, None]:
        query = select(Provider).where(Provider.uuid == uuid, Provider.status != filtered_status)
        result = await cls.execute_stmt(db, query)
        return result.scalars().first()

    @classmethod
    async def fetch_by_product_uuid(cls, db: AsyncSession, product_uuid: str) -> Union[Provider, None]:
        query = select(ProductProviders)\
            .options(subqueryload(ProductProviders.provider))\
            .where(ProductProviders.product_uuid == product_uuid)
        result = await cls.execute_stmt(db, query)
        return [row.provider for row in result.scalars()]

    @classmethod
    async def add_products_to_provider(cls, db: AsyncSession, provider_uuid: str, product_uuids: List[str]):
        products_for_provider = [ProductProviders(provider_uuid=provider_uuid,
                                                  product_uuid=product_uuid) for product_uuid in set(product_uuids)]
        products_for_provider = cls.add_to_session(db, products_for_provider)
        await db.commit()
        return products_for_provider

    @classmethod
    async def create_provider(cls, db: AsyncSession, provider: ProviderCreate) -> Union[Provider, None]:
        db_role = cls.add_to_session(db, Provider(**provider.dict()))

        await db.commit()
        await db.refresh(db_role)
        return db_role

    @classmethod
    async def update_provider_by_uuid(cls, db: AsyncSession, uuid: str, update_values: dict) -> Union[Provider, None]:
        query = update(Provider)\
            .where(Provider.uuid == uuid)\
            .values(**update_values)
        result = await cls.execute_update_stmt(db, query, cls.fetch_by_uuid, uuid=uuid, filtered_status=None)
        return result

    @classmethod
    async def delete_provider(cls, db: AsyncSession, uuid: str) -> dict:
        return await cls.update_provider_by_uuid(db, uuid, {'status': StatusConstants.DELETED,
                                                            'deleted_on': datetime.utcnow()})

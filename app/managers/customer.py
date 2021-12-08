from datetime import datetime
from typing import Union

from app.models.ezinventory_models import Customer
from app.serializers.customer import CustomerCreate
from app.utils.constants import StatusConstants
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Params as PaginationParams
from fastapi_pagination.ext.async_sqlalchemy import paginate

from .base import BaseManager


class CustomerManager(BaseManager):
    model = Customer
    columns = Customer.__table__.columns

    @classmethod
    async def fetch_by_uuid(cls, db: AsyncSession, uuid: str, filtered_status: str = StatusConstants.DELETED) -> Union[Customer, None]:
        query = select(Customer).where(Customer.uuid == uuid, Customer.status != filtered_status)
        result = await cls.execute_stmt(db, query)
        return result.scalars().first()

    @classmethod
    async def search_by_unique_identifier(cls, db: AsyncSession, identifier: str, pagination_params: PaginationParams) -> Union[Customer, None]:
        query = select(Customer).where(Customer.dni.like(f'%{identifier}%'), Customer.status != StatusConstants.DELETED)
        result = await paginate(db, query, pagination_params)
        return result

    @classmethod
    async def create_customer(cls, db: AsyncSession, customer: CustomerCreate) -> Union[Customer, None]:
        db_role = cls.add_to_session(db, Customer(**customer.dict()))

        await db.commit()
        await db.refresh(db_role)
        return db_role

    @classmethod
    async def update_customer_by_uuid(cls, db: AsyncSession, uuid: str, update_values: dict) -> Union[Customer, None]:
        query = update(Customer)\
            .where(Customer.uuid == uuid)\
            .values(**update_values)
        result = await cls.execute_update_stmt(db, query, cls.fetch_by_uuid, uuid=uuid, filtered_status=None)
        return result

    @classmethod
    async def delete_customer(cls, db: AsyncSession, uuid: str) -> dict:
        return await cls.update_customer_by_uuid(db, uuid, {'status': StatusConstants.DELETED,
                                                            'deleted_on': datetime.utcnow()})

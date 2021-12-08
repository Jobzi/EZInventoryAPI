from app.db.postgre_connector import PostgreSqlConnector
from app.managers.customer import CustomerManager
from app.serializers.customer import Customer as CustomerSerializer
from app.serializers.customer import CustomerCreate as CustomerCreateSerializer
from app.serializers.customer import CustomerUpdate as CustomerUpdateSerializer
from app.utils.functions import filter_dict_keys
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination import Params as PaginationParams
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/{uuid}', response_model=CustomerSerializer)
async def get_customer(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await CustomerManager.fetch_by_uuid(db, uuid)


@router.get('/identifier/{identifier}', response_model=Page[CustomerSerializer])
async def get_customers_by_unique_identifier(identifier: str, pagination_params: PaginationParams = Depends(),
                                             db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await CustomerManager.search_by_unique_identifier(db, identifier, pagination_params)


@router.post('', response_model=CustomerSerializer)
async def create_customer(customer: CustomerCreateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await CustomerManager.create_customer(db, customer)


@router.patch('', response_model=CustomerSerializer)
async def basic_customer_update(customer: CustomerUpdateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    update_values = filter_dict_keys(customer.dict(), {'uuid'}, prune_null=True)
    return await CustomerManager.update_customer_by_uuid(db, customer.uuid, update_values)


@router.delete('/{uuid}', response_model=CustomerSerializer)
async def delete_customer(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await CustomerManager.delete_customer(db, uuid)


from typing import List

from app.db.postgre_connector import PostgreSqlConnector
from app.managers.provider import ProviderManager
from app.serializers.provider import Provider as ProviderSerializer
from app.serializers.provider import ProviderProducts as ProviderProductsSerializer
from app.serializers.provider import ProviderProductsCreate as ProviderProductsCreateSerializer
from app.serializers.provider import ProviderCreate as ProviderCreateSerializer
from app.serializers.provider import ProviderUpdate as ProviderUpdateSerializer
from app.utils.functions import filter_dict_keys
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/{uuid}', response_model=ProviderSerializer)
async def get_provider(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await ProviderManager.fetch_by_uuid(db, uuid)


@router.get('/product/{product_uuid}', response_model=List[ProviderSerializer])
async def get_providers_by_product_uuid(product_uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await ProviderManager.fetch_by_product_uuid(db, product_uuid)


@router.put('/products', response_model=List[ProviderProductsSerializer])
async def add_products_to_provider(products_by_provider: ProviderProductsCreateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await ProviderManager.add_products_to_provider(db, products_by_provider.provider_uuid, products_by_provider.product_uuids)


@router.post('', response_model=ProviderSerializer)
async def create_provider(provider: ProviderCreateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await ProviderManager.create_provider(db, provider)


@router.patch('', response_model=ProviderSerializer)
async def basic_provider_update(provider: ProviderUpdateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    update_values = filter_dict_keys(provider.dict(), {'uuid'}, prune_null=True)
    return await ProviderManager.update_provider_by_uuid(db, provider.uuid, update_values)


@router.delete('/{uuid}', response_model=ProviderSerializer)
async def delete_provider(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await ProviderManager.delete_provider(db, uuid)

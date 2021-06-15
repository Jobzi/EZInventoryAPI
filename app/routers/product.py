from app.db.postgre_connector import PostgreSqlConnector
from app.managers.product import ProductManager
from app.serializers.product import Product as ProductSerializer
from app.serializers.product import ProductCreate as ProductCreateSerializer
from app.serializers.product import ProductUpdate as ProductUpdateSerializer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/{uuid}', response_model=ProductSerializer)
async def get_product(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await ProductManager.fetch_by_uuid(db, uuid)


@router.post('', response_model=ProductSerializer)
async def create_product(product: ProductCreateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await ProductManager.create_product(db, product)


@router.put('/{uuid}', response_model=ProductSerializer)
async def update_product(uuid: str, product: ProductUpdateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await ProductManager.update_product_by_uuid(db, uuid, product.dict())


@router.delete('/{uuid}', response_model=ProductSerializer)
async def delete_product(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await ProductManager.delete_product_by_uuid(db, uuid)

from app.db.postgre_connector import PostgreSqlConnector
from app.managers.category import CategoryManager
from app.serializers.category import Category as CategorySerializer
from app.serializers.category import CategoryCreate as CategoryCreateSerializer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/{uuid}', response_model=CategorySerializer)
async def get_category(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await CategoryManager.fetch_by_uuid(db, uuid)


@router.post('', response_model=CategorySerializer)
async def create_category(category: CategoryCreateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await CategoryManager.create_category(db, category)

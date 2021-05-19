from app.db.postgre_connector import PostgreSqlConnector
from app.managers.user import UserManager
from app.serializers.user import User as UserSerializer
from app.serializers.user import UserCreate as UserCreateSerializer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/{uuid}', response_model=UserSerializer)
async def get_user(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await UserManager.fetch_by_uuid(db, uuid)


@router.post('', response_model=UserSerializer)
async def create_user(user: UserCreateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await UserManager.create_user(db, user)

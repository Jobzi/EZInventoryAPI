from app.db.postgre_connector import PostgreSqlConnector
from app.managers.role import RoleManager
from app.serializers.role import Role as RoleSerializer
from app.serializers.role import RoleCreate as RoleCreateSerializer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/{uuid}', response_model=RoleSerializer)
async def get_role(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await RoleManager.fetch_by_uuid(db, uuid)


@router.post('', response_model=RoleSerializer)
async def create_role(role: RoleCreateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await RoleManager.create_role(db, role)

from app.db.postgre_connector import PostgreSqlConnector
from app.managers.user import UserManager
from app.security import auth_user, AuthFunctions
from app.security.common_scopes import UserScopes, AdminScopes
from app.serializers.user import User as UserSerializer
from app.serializers.user import UserCreate as UserCreateSerializer
from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/{uuid}', response_model=UserSerializer)
async def get_user(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db),
                   user_permissions: dict = Security(auth_user, scopes=[UserScopes.OWN])):
    AuthFunctions.check_own_permission_by_uuid(uuid, str(getattr(user_permissions.get('user'), 'uuid', None)), user_permissions.get('scopes'))
    return await UserManager.fetch_by_uuid(db, uuid)


@router.post('', response_model=UserSerializer)
async def create_user(user: UserCreateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db),
                      user_permissions: dict = Security(auth_user, scopes=[AdminScopes.ADMIN_WRITE])):
    AuthFunctions.check_permission_mapping_by_uuid(user.tenant_uuid, user_permissions)
    return await UserManager.create_user(db, user)

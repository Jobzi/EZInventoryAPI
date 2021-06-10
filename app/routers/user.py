from typing import List

from app.db.postgre_connector import PostgreSqlConnector
from app.managers.user import UserManager
from app.security import AuthFunctions, auth_user
from app.security.common_scopes import AdminScopes, UserScopes
from app.serializers.tenant import Tenant as TenantSerializer
from app.serializers.user import User as UserSerializer
from app.serializers.user import UserCreate as UserCreateSerializer
from app.serializers.user import UserUpdate as UserUpdateSerializer
from app.serializers.user import UserRoleByTenant as UserRoleByTenantSerializer
from app.serializers.user import UserRoleByTenantCreate as UserRoleByTenantCreateSerializer
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


@router.patch('', response_model=UserSerializer)
async def basic_user_update(user: UserUpdateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await UserManager.uppdate_user_by_uuid(db, user.uuid, {'phone': user.phone})


@router.delete('/{uuid}', response_model=UserSerializer)
async def delete_user(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await UserManager.delete_user(db, uuid)


@router.get('/{uuid}/tenants', response_model=List[TenantSerializer])
async def get_tenants_related_to_user(uuid: str, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await UserManager.fetch_tenants_by_user_uuid(db, uuid)


@router.post('/role', response_model=List[UserRoleByTenantSerializer])
async def add_tenant_role_to_user(user_roles_by_tenant: UserRoleByTenantCreateSerializer, db: AsyncSession = Depends(PostgreSqlConnector.get_db)):
    return await UserManager.create_user_roles_by_tenant(db, user_roles_by_tenant)

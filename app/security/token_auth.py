from app.db.postgre_connector import PostgreSqlConnector
from app.managers.user import UserManager
from fastapi import Depends
from fastapi.security import SecurityScopes
from sqlalchemy.ext.asyncio.session import AsyncSession

from .functions import AuthFunctions


async def __get_user(db: AsyncSession, username: str) -> dict:
    active_user = await UserManager.fetch_active_user_by_username(db, username)
    return {
        'user_info': active_user,
        'permissions': UserManager.group_permissions_by_tenant(active_user.roles_by_tenant)
    } if active_user else {}


async def auth_user(permissions: SecurityScopes,
                    db: AsyncSession = Depends(PostgreSqlConnector.get_db),
                    token: str = Depends(AuthFunctions.oauth2_scheme)) -> dict:

    return await AuthFunctions.check_user_permissions(db, __get_user, permissions, token)

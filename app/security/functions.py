from datetime import datetime, timedelta
from typing import Any, Coroutine, Mapping, Optional

from app.utils.env_config import EnvConfig
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio.session import AsyncSession

from .exeptions import InvalidCredentialsError, NotEnoughPermissionsError


class JWTFunctions:
    SECRET_KEY: str = EnvConfig.SECRET_KEY
    ALGORITHM: str = 'HS256'
    DEFAULT_EXPIRE_DELTA: timedelta = timedelta(15)

    @classmethod
    def create_access_token(cls, data: dict, expire_delta: Optional[timedelta] = None) -> str:
        expire = datetime.utcnow() + (expire_delta or cls.DEFAULT_EXPIRE_DELTA)
        data_to_encode = {**data, 'exp': expire}
        return jwt.encode(data_to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_token(cls, token: str) -> dict:
        return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])


class AuthFunctions:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

    @classmethod
    async def check_user_permissions(cls, db: AsyncSession, get_user: Coroutine, permissions: SecurityScopes, token: str) -> Mapping[str, Any]:
        authenticate_header = f'Bearer {"scope="+permissions.scope_str if permissions.scopes else ""}'.strip()

        try:
            decoded_token = JWTFunctions.decode_token(token)
        except JWTError:
            raise InvalidCredentialsError(authenticate_header)

        if (username := decoded_token.get('sub')) is None:
            raise InvalidCredentialsError(authenticate_header)

        if decoded_token.get('exp') < datetime.utcnow().timestamp():
            raise InvalidCredentialsError(authenticate_header, 'Token expired')

        if not (user := await get_user(db, username)):
            raise InvalidCredentialsError(authenticate_header, 'Invalid or Deleted user')

        if not (permissions_by_tenant := user.get('permissions', {})):
            raise NotEnoughPermissionsError(authenticate_header)

        scope_set = set(permissions.scopes)
        valid_permissions_by_tenant = {tenant_uuid: permission
                                       for tenant_uuid, permission in permissions_by_tenant.items()
                                       if permission and set(permission).intersection(scope_set)}

        if not valid_permissions_by_tenant:
            raise NotEnoughPermissionsError(authenticate_header)

        return {
            'user': user.get('user_info'),
            'permissions_by_tenant': valid_permissions_by_tenant,
            'scopes': scope_set
        }

    @classmethod
    def check_permission_mapping_by_uuid(cls, source_uuid: str, user_permissions: dict) -> None:
        scopes = user_permissions.get('scopes')
        permissions_for_source = user_permissions.get('permissions_by_tenant', {}).get(source_uuid, [])
        if not permissions_for_source or not set(permissions_for_source).intersection(scopes):
            raise NotEnoughPermissionsError(f"Bearer {' '.join(scopes)}")

    @classmethod
    def check_own_permission_by_uuid(cls, source_uuid: str, target_uuid: str, scopes: list) -> None:
        if source_uuid != target_uuid:
            raise NotEnoughPermissionsError(f"Bearer {' '.join(scopes)}")

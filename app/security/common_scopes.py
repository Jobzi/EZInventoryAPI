
from typing import Optional, Sequence


class Scopes:
    __scopes: list = []

    @classmethod
    def build(cls, extra_scopes: Optional[Sequence[str]] = None):
        scopes = cls.__scopes.copy()
        if extra_scopes:
            scopes.extend(extra_scopes)
        return scopes


class AdminScopes(Scopes):
    ADMIN_READ: str = 'admin_read'
    ADMIN_WRITE: str = 'admin_read'

    __scopes: list = [ADMIN_READ, ADMIN_WRITE]


class UserScopes(Scopes):
    USER_READ: str = 'user_read'
    USER_CREATE: str = 'user_create'
    OWN: str = 'own'

    __scopes: list = [USER_READ, USER_CREATE]

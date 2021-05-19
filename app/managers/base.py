from typing import Any

from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import Executable


class BaseManager:

    model: Any = None

    @staticmethod
    async def execute_stmt(db: AsyncSession, stmt: Executable) -> Result:
        return await db.execute(stmt)

    @classmethod
    def add_to_session(cls, db: AsyncSession, obj: Any):
        '''
        We will let the parent methods manage the session commit and rollback
        This will allow method compossition with just one session.
        Example here: https://stribny.name/blog/fastapi-asyncalchemy/
        '''
        session_add = db.add_all if isinstance(obj, list) else db.add
        session_add(obj)
        return obj

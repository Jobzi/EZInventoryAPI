from typing import Any, Coroutine, Union

from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import Executable
from app.utils.constants import DbDialects
from app.utils.functions import build_from_key_value_arrays


class BaseManager:
    model: Any = None
    columns: Any = None

    @staticmethod
    async def execute_stmt(db: AsyncSession, stmt: Executable) -> Result:
        return await db.execute(stmt)

    @classmethod
    async def execute_update_stmt(cls, db: AsyncSession, stmt: Executable, return_corutine: Coroutine, 
                                    **corutine_parameters: dict) -> Union[dict, type(model)]:
        if db.bind.dialect.name == DbDialects.POSTGRESQL.value:
            result = (await db.execute(stmt.returning(*cls.columns))).first()
            await db.commit()
            return build_from_key_value_arrays(cls.columns.keys(), result)
        else:
            await db.execute(stmt)
            await db.commit()
            result = await return_corutine(db, **corutine_parameters)
            return result

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

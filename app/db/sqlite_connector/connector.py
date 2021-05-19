from typing import Union
from app.utils.env_config import EnvConfig

from ..base_connector import BaseConnector


class SqLiteConnector(BaseConnector):
    DB_URL: str = EnvConfig.TESTING_DB_URL

    @classmethod
    async def create_db(cls, model_path: str, model_files: Union[str, list]):
        # NOTE: We are importing models dinamically
        model_files = [model_files] if isinstance(model_files, str) else model_files
        try:
            __import__(model_path, globals(), locals(), model_files)
        except ImportError:
            raise ImportError(f'{model_path} is not a valid module path')
        cls.init_db_engine()
        async with cls.engine.begin() as conn:
            await conn.run_sync(cls.Base.metadata.drop_all)
            await conn.run_sync(cls.Base.metadata.create_all)

from app.utils.env_config import EnvConfig

from ..base_connector import BaseConnector


class PostgreSqlConnector(BaseConnector):
    DB_URL: str = EnvConfig.DB_URL

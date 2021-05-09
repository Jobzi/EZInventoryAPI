from sqlalchemy.ext.asyncio.engine import AsyncEngine
from app.db import Base
from app.utils.env_config import EnvConfig
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class PostgreSqlConnector:
    engine: AsyncEngine = None
    SessionLocal: AsyncSession = None
    Base = Base

    @classmethod
    def init_db_engine(cls) -> None:
        if not cls.engine:
            cls.engine = create_async_engine(EnvConfig.DB_URL, echo=True)

    @classmethod
    def init_db_session(cls) -> None:
        if not cls.SessionLocal:
            cls.init_db_engine()
            cls.SessionLocal = sessionmaker(cls.engine, class_=AsyncSession, expire_on_commit=False)

    @classmethod
    async def get_db(cls) -> AsyncSession:
        cls.init_db_session()
        async with cls.SessionLocal() as session:
            yield session

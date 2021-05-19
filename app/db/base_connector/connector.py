from app.db import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker


class BaseConnector:
    DB_URL: str = None
    engine: AsyncEngine = None
    SessionLocal: AsyncSession = None
    Base = Base

    @classmethod
    def init_db_engine(cls) -> None:
        if not cls.engine:
            if not cls.DB_URL:
                raise ValueError('DB_URL cannot be empty')
            cls.engine = create_async_engine(cls.DB_URL, echo=False)

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

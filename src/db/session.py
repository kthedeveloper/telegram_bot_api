from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, \
    async_sessionmaker

from core.config import settings

url = settings.POSTGRES_DSN

class DbEngine:
    def __init__(self):
        self.engine = None

    def get_engine(self):
        if self.engine is None:
            self.engine = create_async_engine(str(url), future=True, echo=True)

        return self.engine


db_engine = DbEngine()


class DbSessionFactory:
    def __init__(self):
        self.session = None

    def get_session(self):
        if self.session is None:
            self.session = async_sessionmaker(
                bind=db_engine.get_engine(), class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False, autoflush=False
            )
        return self.session()


db_session_factory = DbSessionFactory()
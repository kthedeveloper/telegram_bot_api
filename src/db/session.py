from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from core.config import settings


url = settings.POSTGRES_DSN

engine = create_async_engine(str(url), future=True, echo=True)

async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False,
    autocommit=False, autoflush=False
)

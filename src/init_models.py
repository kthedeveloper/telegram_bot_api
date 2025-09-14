import asyncio
from db.models.user import Base
from db.session import db_engine


async def init_models():
    engine = db_engine.get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(init_models())

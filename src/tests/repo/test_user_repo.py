import asyncio
import pytest
import pytest_asyncio
from testcontainers.postgres import PostgresContainer
from core.config import settings
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection


@pytest_asyncio.fixture
async def postgres_container() -> PostgresContainer:
    container = PostgresContainer("postgres:latest")
    container.start()

    url = container.get_connection_url(driver="asyncpg")
    settings.POSTGRES_DSN = url

    from init_models import init_models
    await init_models()

    return container


@pytest.mark.asyncio
async def test_create_user(postgres_container: PostgresContainer):
    from db.repo.user_repo import UserRepository

    engine = create_async_engine(postgres_container.get_connection_url(driver="asyncpg"))
    async with engine.begin() as connection:  # type: AsyncConnection
        statement = sqlalchemy.text("SELECT * FROM public.user")
        result = await connection.execute(statement)

        r = result.fetchall()
        assert len(r) == 0

        await UserRepository.create_user("some_user", 12222)

        result = await connection.execute(statement)
        r = result.fetchall()
        assert len(r) == 1
        for row in r:
            assert row[0] == 1
            assert row[1] == 'some_user'
            assert row[2] == 12222

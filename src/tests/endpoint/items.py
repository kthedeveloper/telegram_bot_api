import asyncio
import httpx
import multiprocessing
import uvicorn
import pytest
import pytest_asyncio
from testcontainers.postgres import PostgresContainer

from tests.repo.test_user_repo import postgres_container


# @pytest.mark.asyncio
@pytest_asyncio.fixture
async def app(postgres_container: PostgresContainer):
    from run import create_app

    app = create_app()
    p = multiprocessing.Process(
        target=lambda: uvicorn.run(app, host="0.0.0.0", port=9999),
        daemon=True
    )
    p.start()

    return p


@pytest.mark.asyncio
async def test_get_items(app):
    await asyncio.sleep(5)
    async with httpx.AsyncClient() as client:
        r = await client.get("http://127.0.0.1:9999/api/v1/items/")

        assert r.status_code == 200
        assert r.json() == {'data': [{'id': 1, 'name': 'Item 1'},
                                     {'id': 2, 'name': 'Item 2'},
                                     {'id': 3, 'name': 'Item 3'},
                                     {'id': 4, 'name': 'Item 4'}],
                            'total': 4}

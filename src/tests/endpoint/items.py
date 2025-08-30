import os
import asyncio
import httpx
import uvicorn
import pytest
import pytest_asyncio
from testcontainers.postgres import PostgresContainer

from tests.repo.test_user_repo import postgres_container
import multiprocessing


# @pytest.mark.asyncio
@pytest_asyncio.fixture
async def app(postgres_container: PostgresContainer):
    url = postgres_container.get_connection_url(driver='asyncpg')

    def run_app(_url):
        os.environ['POSTGRES_DSN'] = _url
        uvicorn.run('run:create_app', host="0.0.0.0", port=9999)

    p = multiprocessing.Process(
        target=run_app,
        daemon=True,
        args=(url,),
    )
    p.start()

    async def wait_for_server():
        while True:
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.get("http://localhost:9999")
                    if r.status_code == 404:
                        return  # Server is ready
            except Exception as e:
                await asyncio.sleep(0.01)

    await wait_for_server()

    return p


@pytest.mark.asyncio
async def test_get_items(app):
    async with httpx.AsyncClient() as client:
        r = await client.get("http://127.0.0.1:9999/api/v1/items/")

        assert r.status_code == 200
        assert r.json() == {'data': [{'id': 1, 'name': 'Item 1'},
                                     {'id': 2, 'name': 'Item 2'},
                                     {'id': 3, 'name': 'Item 3'},
                                     {'id': 4, 'name': 'Item 4'}],
                            'total': 4}


@pytest.mark.asyncio
async def test_get_single_item(app):
    await asyncio.sleep(3)
    async with httpx.AsyncClient() as client:
        r = await client.get("http://127.0.0.1:9999/api/v1/items/1")

        assert r.status_code == 200
        assert r.json() == {'id': 1, 'name': 'Item 1'}


@pytest.mark.asyncio
async def test_delete_item(app):
    await asyncio.sleep(3)
    async with httpx.AsyncClient() as client:
        r = await client.delete("http://127.0.0.1:9999/api/v1/items/4")
        assert r.status_code == 200

        r2 = await client.get("http://127.0.0.1:9999/api/v1/items/")
        assert r2.status_code == 200
        body = r2.json()
        assert body["total"] == 3
        assert {"id": 4, "name": "Item 4"} not in body["data"]

import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from core.config import settings
from api.v1.endpoints.items import router as items_router
from api.v1.endpoints.products import router as products_router
from api.v1.endpoints.telegram_webhook import router as telegram_router

from core.utils.webhook import set_webhook


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Do startup action
    if settings.UPDATE_WEBHOOK:
        _ = asyncio.create_task(set_webhook())

    # TODO: check uncompleted tasks

    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        default_response_class=JSONResponse,
        lifespan=lifespan
    )

    app.include_router(items_router, prefix=f"{settings.API_PREFIX}/items")
    app.include_router(products_router, prefix=f"{settings.API_PREFIX}/products")
    app.include_router(telegram_router, prefix=f"{settings.API_PREFIX}/webhook")
    return app


if __name__ == '__main__':
    uvicorn.run(create_app(), host=settings.BIND_HOST, port=settings.BIND_PORT)
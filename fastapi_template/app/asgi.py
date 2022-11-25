from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_pagination import add_pagination
from pydantic import BaseConfig
from starlette.staticfiles import StaticFiles

from fastapi_template.app.api.router import api_router
from fastapi_template.app.core import Response
from fastapi_template.app.core.log import logger
from fastapi_template.app.exception import HttpException, http_exception_handler
from fastapi_template.app.middleware.middleware import GlobalMiddlewares
from fastapi_template.config import settings


async def on_startup():
    """Define FastAPI startup event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#startup-event

    """
    logger.debug("Execute FastAPI startup event handler.")
    FastAPICache.init(InMemoryBackend(), prefix=settings.CACHE_PREFIX, expire=settings.CACHE_EXPIRED_SECONDS)


async def on_shutdown():
    """Define FastAPI shutdown event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#shutdown-event

    """
    logger.debug("Execute FastAPI shutdown event handler.")
    # Gracefully close utilities.


"""
Initialize FastAPI application.
Returns:FastAPI: Application object instance.
"""
app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME,
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    default_response_class=Response
)
BaseConfig.arbitrary_types_allowed = True
app.mount(f"{settings.FILE_URL_PREFIX}", StaticFiles(directory=settings.FILE_UPLOAD_FOLDER))
GlobalMiddlewares(app).init()
logger.debug("Adding application routes...")
app.include_router(api_router, prefix=settings.API_PREFIX)
logger.debug("Register global exception handler for custom HTTPException.")
app.add_exception_handler(HttpException, http_exception_handler)
# add pagination
add_pagination(app)

if __name__ == '__main__':
    uvicorn.run(f"{Path(__file__).stem}:app", host="0.0.0.0", port=8000, reload=True)

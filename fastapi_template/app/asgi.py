import os
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from loguru import logger
from pydantic import BaseConfig

from fastapi_template.app.core import Response
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
GlobalMiddlewares(app).init()

if __name__ == '__main__':
    sys.exit(uvicorn.run(f"{Path(__file__).stem}:app",
                         host=os.getenv("FASTAPI_HOST", "127.0.0.1"),
                         port=int(os.getenv("FASTAPI_PORT", "8000")),
                         reload=True,
                         log_config=None,
                         access_log=True))

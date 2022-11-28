from uuid import uuid4

from asgi_correlation_id.middleware import CorrelationIdMiddleware
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from fastapi_template.app.api.router import api_router
from fastapi_template.app.core.db.session import SQLAlchemyMiddleware
from fastapi_template.app.core.log.logging import CustomizeLogger
from fastapi_template.app.core.static import mount_static
from fastapi_template.app.exception.handler import HttpException, http_exception_handler
from fastapi_template.config import settings


class GlobalMiddlewares:
    def __init__(self, app: FastAPI):
        self.app: FastAPI = app

    def init(self):
        # logging configuration
        logger = CustomizeLogger.make_logger()
        self.app.logger = logger
        self.app.add_middleware(CorrelationIdMiddleware,
                                header_name='X-Request-ID',
                                generator=lambda: uuid4().hex,
                                transformer=lambda a: a,
                                )
        # gzip compress
        self.app.add_middleware(GZipMiddleware, minimum_size=settings.GZIP_MINIMUM_SIZE)
        # Set all CORS enabled origins
        if settings.ALLOW_CORS_ORIGINS:
            self.app.add_middleware(CORSMiddleware,
                                    allow_origins=[str(origin) for origin in settings.ALLOW_CORS_ORIGINS],
                                    allow_credentials=True,
                                    allow_methods=["*"],
                                    allow_headers=["*"],
                                    )
        # serve the static folder
        mount_static(self.app)
        self.app.include_router(api_router, prefix=settings.API_PREFIX)
        self.app.add_exception_handler(HttpException, http_exception_handler)
        # for db
        self.app.add_middleware(
            SQLAlchemyMiddleware,
            db_url=settings.SQLALCHEMY_DATABASE_URI,
            engine_args={
                "echo": False,
                "pool_pre_ping": True,
            },
        )
        # TODO: for jwt token verification, swagger security not works...???
        # self.app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend())

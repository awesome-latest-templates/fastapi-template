from uuid import uuid4

from asgi_correlation_id.middleware import is_valid_uuid4, CorrelationIdMiddleware
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from fastapi_template.app.core.db.session import SQLAlchemyMiddleware
from fastapi_template.config import settings


class GlobalMiddlewares:
    def __init__(self, app: FastAPI):
        self.app: FastAPI = app

    def init(self):
        # Set all CORS enabled origins
        if settings.ALLOW_CORS_ORIGINS:
            self.app.add_middleware(CORSMiddleware,
                                    allow_origins=[str(origin) for origin in settings.ALLOW_CORS_ORIGINS],
                                    allow_credentials=True,
                                    allow_methods=["*"],
                                    allow_headers=["*"],
                                    )
        # for db
        self.app.add_middleware(
            SQLAlchemyMiddleware,
            db_url=settings.SQLALCHEMY_DATABASE_URI,
            engine_args={
                "echo": False,
                "pool_pre_ping": True,
            },
        )
        # gzip
        self.app.add_middleware(GZipMiddleware, minimum_size=settings.GZIP_MINIMUM_SIZE)
        # for logging
        self.app.add_middleware(CorrelationIdMiddleware,
                                header_name='X-Request-ID',
                                generator=lambda: uuid4().hex,
                                validator=is_valid_uuid4,
                                transformer=lambda a: a,
                                )
        # TODO: for jwt token verification, swagger security not works...???
        # self.app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend())

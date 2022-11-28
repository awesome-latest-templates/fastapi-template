import os
from functools import lru_cache
from typing import List, Union

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    # Swagger UI
    PROJECT_NAME: str = 'FastAPI_Template'
    API_PREFIX: str = "/api"
    # file upload/download
    FILE_UPLOAD_FOLDER: str = ""
    FILE_URL_PREFIX: str = "/static"
    FILE_READ_CHUNK_SIZE: int = 1024  # 1kb
    FILE_MAX_SIZE: int = 5 * 1024 * 1024  # 100MB
    # JWT Token
    # binascii.hexlify(os.urandom(24)) or secrets.token_urlsafe(32)
    JWT_SECRET_KEY: str = "3038850e0ce74437b089276268dac510"
    JWT_EXPIRED_SECONDS: int = 604800  # 7 days
    JWT_ALGORITHM: str = "HS256"
    JWT_ISSUER: str = PROJECT_NAME
    JWT_AUDIENCE: str = PROJECT_NAME
    JWT_TOKEN_HEADER_NAME: str = 'Authorization'
    JWT_TOKEN_SCHEME_NAME: str = ''
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    ALLOW_CORS_ORIGINS: List[str] = ["*"]
    GZIP_MINIMUM_SIZE: int = 500

    @validator("ALLOW_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
    SQLALCHEMY_DATABASE_URI: str = None
    DATABASE_ENGINE_POOL_SIZE: int = 83
    DATABASE_ENGINE_MAX_OVERFLOW: int = 0

    USE_REDIS: bool = False
    # cache
    CACHE_PREFIX: str = "app"
    CACHE_EXPIRED_SECONDS: int = 600
    # snowflake
    SNOWFLAKE_INSTANCE: int = 10

    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("~/.env")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

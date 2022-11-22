from typing import List, Union

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    # Swagger UI
    PROJECT_NAME: str = 'FastAPI_Template'
    # JWT Token
    # binascii.hexlify(os.urandom(24)) or secrets.token_urlsafe(32)
    JWT_SECRET_KEY: str = "3038850e0ce74437b089276268dac510"
    JWT_EXPIRED_SECONDS: int = 604800  # 7 days
    JWT_ALGORITHM: str = "HS256"
    JWT_ISSUER: str = PROJECT_NAME
    JWT_AUDIENCE: str = PROJECT_NAME
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    ALLOW_CORS_ORIGINS: List[str] = ["*"]

    @validator("ALLOW_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
    SQLALCHEMY_DATABASE_URI: str
    DATABASE_ENGINE_POOL_SIZE: int = 20
    DATABASE_ENGINE_MAX_OVERFLOW: int = 0

    USE_REDIS: bool = False

    class Config:
        case_sensitive = True


settings = Settings()

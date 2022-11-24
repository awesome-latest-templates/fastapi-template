from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette import status

from fastapi_template.app.exception import HttpException
from fastapi_template.app.entity.auth_entity import TokenPayload, TokenResponse
from fastapi_template.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(data: TokenPayload, expires_delta: timedelta = None) -> TokenResponse:
    if not expires_delta:
        expires_delta = timedelta(seconds=settings.JWT_EXPIRED_SECONDS)
    expire = datetime.utcnow() + expires_delta

    payload = data.dict()
    payload.update({
        # "sub": "",
        # "nameid": "",
        "exp": expire,
        'iss': settings.JWT_ISSUER,
        'aud': settings.JWT_AUDIENCE
    })
    encoded_jwt = jwt.encode(
        payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    resp_data = {
        "access_token": encoded_jwt,
        "expires_in": expires_delta.total_seconds()
    }
    token_response = TokenResponse(**resp_data)
    return token_response


def verify_token(token: str) -> TokenPayload:
    credentials_exception = HttpException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "bearer"}
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if not payload.get("upn"):
            raise credentials_exception
        token_data = TokenPayload(**payload)
        return token_data
    except (jwt.JWTError, ValidationError):
        raise credentials_exception


def create_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

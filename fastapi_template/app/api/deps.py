from typing import Optional

from fastapi import Security, Depends
from fastapi.security import APIKeyHeader
from starlette import status

from fastapi_template.app import service
from fastapi_template.app.core.auth.security import verify_access_token
from fastapi_template.app.entity.user_entity import UserDetail
from fastapi_template.app.exception import HttpException
from fastapi_template.config import settings

access_token_header = APIKeyHeader(name=settings.TOKEN_HEADER_NAME, auto_error=False)


def get_access_token(
        token_header: str = Security(access_token_header),
) -> Optional[str]:
    """
    Refer: fastapi.security.oauth2.OAuth2PasswordBearer
    :return:
    """
    if not token_header:
        raise HttpException(
            detail="access-token is missing",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return token_header


async def get_current_user(access_token: str = Depends(get_access_token)) -> Optional[UserDetail]:
    user_id = await verify_access_token(access_token)
    user_detail = await service.user.get_user_detail(user_id=user_id)
    if not user_detail:
        detail = f"Not found the user with associated id={user_id}"
        raise HttpException(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "bearer"}
        )
    return UserDetail(**user_detail)


def valid_content_length():
    return settings.FILE_MAX_SIZE

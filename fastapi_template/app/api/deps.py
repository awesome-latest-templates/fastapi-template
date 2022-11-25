from typing import Optional

from fastapi import Security, Depends
from fastapi.security import APIKeyHeader
from starlette import status

from fastapi_template.app import service
from fastapi_template.app.core.auth.security import verify_access_token
from fastapi_template.app.entity.user_entity import UserDetail
from fastapi_template.app.exception import HttpException
from fastapi_template.config import settings

access_token_header = APIKeyHeader(name=settings.JWT_TOKEN_HEADER_NAME, auto_error=False)


def get_access_token(
        token_value: str = Security(access_token_header),
) -> Optional[str]:
    """
    Refer: fastapi.security.oauth2.OAuth2PasswordBearer
    :return:
    """
    if not token_value:
        raise HttpException(
            detail="access-token is missing",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return token_value


async def get_token_data(access_token):
    token_payload = await verify_access_token(access_token)
    user_id = token_payload.upn
    user_detail = await service.user.get_user_detail(user_id=user_id)
    if not user_detail:
        detail = f"Not found the user with associated id={user_id}"
        raise HttpException(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "bearer"}
        )
    user_detail = UserDetail(**user_detail)
    return user_detail


def get_current_user(roles: list = None):
    async def current_user(access_token: str = Depends(get_access_token)) -> UserDetail:
        user_detail = await get_token_data(access_token)
        user_role = user_detail.role
        if roles and not user_role:
            raise HttpException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        if roles and not set(roles).issubset(set(user_role)):
            raise HttpException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {str(roles)}  is required for this action",
            )
        return user_detail

    return current_user


def valid_content_length():
    return settings.FILE_MAX_SIZE

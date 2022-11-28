from typing import Optional

from fastapi import Security, Depends
from fastapi.security import APIKeyHeader
from starlette import status

from fastapi_template.app import service
from fastapi_template.app.core.auth.security import verify_access_token
from fastapi_template.app.exception import HttpException
from fastapi_template.app.schema.user_schema import UserDetailResponse
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
            detail="Unauthorized Request",
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
    user_detail = UserDetailResponse(**user_detail)
    return user_detail


def get_current_user(roles: list = None):
    async def current_user(access_token: str = Depends(get_access_token)) -> UserDetailResponse:
        user_detail = await get_token_data(access_token)
        user_roles = user_detail.role
        if roles:
            is_valid_role = False
            for role in roles:
                if role in user_roles:
                    is_valid_role = True
                    break

            if not is_valid_role:
                raise HttpException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions"
                )
        return user_detail

    return current_user


def valid_content_length():
    return settings.FILE_MAX_SIZE

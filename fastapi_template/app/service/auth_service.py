import datetime
from typing import Optional

from fastapi_template.app import model, crud, service
from fastapi_template.app.core import ResponseCode
from fastapi_template.app.core.auth.security import create_access_token, verify_password
from fastapi_template.app.entity.auth_entity import TokenPayload, TokenResponse, AuthLoginRequest
from fastapi_template.app.exception import HttpException


class AuthService:

    async def create_token_async(self, form_data: AuthLoginRequest) -> TokenResponse:
        username = form_data.username
        password = form_data.password
        if not (username and password):
            raise HttpException(ResponseCode.BAD_REQUEST, "username or password is empty")
        user_data: Optional[model.User] = await crud.user.query_by_username(username=username)
        if not user_data:
            raise HttpException(ResponseCode.NOT_FOUND, "not found associated user")
        store_password = user_data.password
        valid_password = verify_password(password, store_password)
        if not valid_password:
            raise HttpException(ResponseCode.BAD_REQUEST, "password is incorrect")
        is_active = user_data.is_active == 1
        if not is_active:
            raise HttpException(ResponseCode.FORBIDDEN, "user is deactivate")
        # get user roles
        user_detail = await service.user.get_user_detail(user_id=user_data.id)
        # create the oauth jwt token
        token_payload = TokenPayload()
        token_payload.upn = user_detail.id
        token_resp = create_access_token(token_payload, datetime.timedelta(days=1))
        return token_resp


auth = AuthService()

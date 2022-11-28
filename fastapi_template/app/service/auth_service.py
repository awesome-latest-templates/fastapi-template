import datetime
from typing import Optional

from fastapi_template.app import model, crud, service
from fastapi_template.app.core import ResponseCode
from fastapi_template.app.core.auth.security import create_access_token, verify_password
from fastapi_template.app.exception.handler import HttpException
from fastapi_template.app.schema.auth_schema import TokenPayload, TokenResponse, AuthLoginRequest


class AuthService:

    async def create_token_async(self, form_data: AuthLoginRequest) -> TokenResponse:
        username = form_data.username
        password = form_data.password
        if not (username and password):
            raise HttpException(ResponseCode.USER_PASSWORD_EMPTY)
        user_data: Optional[model.User] = await crud.user.query_by_username(username=username)
        if not user_data:
            raise HttpException(ResponseCode.USER_NOT_FOUND)
        store_password = user_data.password
        valid_password = verify_password(password, store_password)
        if not valid_password:
            raise HttpException(ResponseCode.USER_PASSWORD_INVALID)
        if not user_data.is_active:
            raise HttpException(ResponseCode.USER_DISABLED)
        # get user roles
        user_detail = await service.user.get_user_detail(user_id=user_data.id, user_data=user_data)
        # create the oauth jwt token
        token_payload = TokenPayload()
        token_payload.upn = user_detail['id']
        token_resp = create_access_token(token_payload, datetime.timedelta(days=1))
        # save the login data
        update_data = {
            "last_login_time": datetime.datetime.utcnow()
        }
        await self.save_login_data(user_data, update_data)
        return token_resp

    async def save_login_data(self, previous_user_data, update_user_data):
        user_data = await crud.user.update(current_model=previous_user_data, update_schema=update_user_data)
        return user_data


auth = AuthService()

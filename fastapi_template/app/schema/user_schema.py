from pydantic import Field

from fastapi_template.app.schema.base_schema import BasePageParamModel, BaseSchemaModel


class UserCreateRequest(BaseSchemaModel):
    user_name: str = Field(..., min_length=5)
    password: str = Field(..., min_length=6)


class UserUpdateRequest(BaseSchemaModel):
    id: str
    nick_name: str = None
    avatar: str = None
    email: str = None


class UserDetailResponse(BaseSchemaModel):
    id: str = None
    user_name: str = None
    nick_name: str = None
    last_login_time: str = None
    avatar: str = None
    email: str = None
    role: list = []


class UserSearchRequest(BasePageParamModel):
    name: str = ""


class UserRoleRequest(BaseSchemaModel):
    user_id: str
    roles: list = []

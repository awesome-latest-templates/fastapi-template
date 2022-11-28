from pydantic import Field

from fastapi_template.app.entity.base_entity import BasePageParamModel, BaseEntityModel


class UserCreateRequest(BaseEntityModel):
    user_name: str = Field(..., min_length=5)
    password: str = Field(..., min_length=6)


class UserUpdateRequest(BaseEntityModel):
    id: str
    nick_name: str = None
    avatar: str = None
    email: str = None


class UserDetailResponse(BaseEntityModel):
    id: int = 0
    user_name: str = None
    nick_name: str = None
    last_login_time: str = None
    avatar: str = None
    email: str = None
    role: list = []


class UserSearchRequest(BasePageParamModel):
    name: str = ""


class UserRoleRequest(BaseEntityModel):
    user_id: int
    roles: list = []

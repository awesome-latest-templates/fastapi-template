from pydantic import BaseModel, Field

from fastapi_template.app.entity.base_entity import PageParamModel, BaseEntityModel


class UserCreateRequest(BaseModel):
    user_name: str = Field(..., min_length=5)
    password: str = Field(..., min_length=6)


class UserUpdateRequest(BaseEntityModel):
    id: str
    nick_name: str = None
    avatar: str = None
    email: str = None


class UserDetail(BaseEntityModel):
    id: int = 0
    user_name: str = None
    nick_name: str = None
    last_login_time: str = None
    avatar: str = None
    email: str = None
    role: list = []


class UserSearchRequest(PageParamModel):
    name: str = None

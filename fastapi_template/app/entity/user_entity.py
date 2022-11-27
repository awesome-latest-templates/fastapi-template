from pydantic import BaseModel

from fastapi_template.app.entity.common_entity import PageParamModel


class UserCreateRequest(BaseModel):
    pass


class UserUpdateRequest(UserCreateRequest):
    id: str


class UserDetail(BaseModel):
    id: int = 0
    user_name: str = None
    nick_name: str = None
    last_login_time: str = None
    avatar: str = None
    email: str = None
    role: list = []

    class Config:
        orm_mode = True


class UserSearchRequest(PageParamModel):
    name: str = None

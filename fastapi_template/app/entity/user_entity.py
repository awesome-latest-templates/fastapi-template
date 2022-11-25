from pydantic import BaseModel


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

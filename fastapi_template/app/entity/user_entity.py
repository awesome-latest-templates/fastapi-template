from pydantic import BaseModel


class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserCreateRequest(BaseModel):
    username: str
    password: str


class UserUpdateRequest(BaseModel):
    username: str


class UserResponse(BaseModel):
    id: int = 0
    user_name: str = None
    nick_name: str = None
    last_login_time: str = None
    avatar: str = None
    token: str = None
    email: str = None

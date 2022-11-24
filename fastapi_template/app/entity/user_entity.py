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
    Id: int = 0
    UserName: str = None
    NickName: str = None
    LastLoginTime: str = None
    Avatar: str = None
    token: str = None
    Email: str = None

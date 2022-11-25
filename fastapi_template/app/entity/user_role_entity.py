from pydantic import BaseModel


class UserRoleCreateRequest(BaseModel):
    user_id: int
    role_id: int


class UserRoleUpdateRequest(BaseModel):
    pass

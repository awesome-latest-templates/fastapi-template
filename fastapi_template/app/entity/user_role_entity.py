from fastapi_template.app.entity.base_entity import BaseEntityModel


class UserRoleCreateRequest(BaseEntityModel):
    user_id: int
    role_id: int


class UserRoleUpdateRequest(BaseEntityModel):
    pass

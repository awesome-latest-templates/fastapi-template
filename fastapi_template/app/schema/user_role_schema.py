from fastapi_template.app.schema.base_schema import BaseSchemaModel


class UserRoleCreateRequest(BaseSchemaModel):
    user_id: int
    role_id: int


class UserRoleUpdateRequest(BaseSchemaModel):
    pass

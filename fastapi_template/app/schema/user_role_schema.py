from fastapi_template.app.schema.base_schema import BaseSchemaModel


class UserRoleCreateRequest(BaseSchemaModel):
    user_id: str
    role_id: str


class UserRoleUpdateRequest(BaseSchemaModel):
    pass

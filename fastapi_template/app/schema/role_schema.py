from pydantic import Field

from fastapi_template.app.schema.base_schema import BaseSchemaModel, BasePageParamModel


class RoleCreateRequest(BaseSchemaModel):
    name: str = Field(..., min_length=4)
    description: str = Field(..., min_length=5)


class RoleUpdateRequest(RoleCreateRequest):
    id: int


class RoleSearchRequest(BasePageParamModel):
    name: str = ""

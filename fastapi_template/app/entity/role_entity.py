from pydantic import Field

from fastapi_template.app.entity.base_entity import BaseEntityModel, BasePageParamModel


class RoleCreateRequest(BaseEntityModel):
    name: str = Field(..., min_length=4)
    description: str = Field(..., min_length=5)


class RoleUpdateRequest(RoleCreateRequest):
    id: int


class RoleSearchRequest(BasePageParamModel):
    name: str = ""

from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.model.role_model import Role
from fastapi_template.app.schema.role_schema import RoleCreateRequest, RoleUpdateRequest


class RoleCrud(BaseCrud[Role, RoleCreateRequest, RoleUpdateRequest]):
    pass


role = RoleCrud(Role)

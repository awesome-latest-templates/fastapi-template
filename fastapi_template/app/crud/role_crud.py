from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.entity.role_entity import RoleCreateRequest, RoleUpdateRequest
from fastapi_template.app.model import Role


class RoleCrud(BaseCrud[Role, RoleCreateRequest, RoleUpdateRequest]):
    pass


role = RoleCrud(Role)

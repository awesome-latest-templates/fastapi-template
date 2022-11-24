from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.entity.role_entity import RoleCreate, RoleUpdate
from fastapi_template.app.model import Role


class RoleCrud(BaseCrud[Role, RoleCreate, RoleUpdate]):
    pass


role = RoleCrud(Role)

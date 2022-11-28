from fastapi import Depends

from fastapi_template.app import service
from fastapi_template.app.api.deps import get_current_user
from fastapi_template.app.core import Response
from fastapi_template.app.core.cvb import cbv
from fastapi_template.app.core.inferring_router import InferringRouter
from fastapi_template.app.schema.base_schema import IdRequest
from fastapi_template.app.schema.role_schema import RoleCreateRequest, RoleSearchRequest, RoleUpdateRequest
from fastapi_template.app.schema.user_schema import UserDetailResponse
from fastapi_template.config import roles

router = InferringRouter()


@cbv(router)
class RoleController:

    @router.post("/add", tags=["role"])
    async def create_role(self, create_role: RoleCreateRequest,
                          user: UserDetailResponse = Depends(get_current_user([roles.SUPER_ADMIN_ROLE]))):
        data = await service.role.create_role(create_role, create_by=user.id)
        return Response.ok(data)

    @router.put("/update", tags=["role"])
    async def update_role(self, update_role: RoleUpdateRequest,
                          user: UserDetailResponse = Depends(get_current_user([roles.SUPER_ADMIN_ROLE]))) -> Response:
        data = await service.role.update_role(update_role, update_by=user.id)
        return Response.ok(data)

    @router.delete("/delete", tags=["role"])
    async def deactivate_role(self, inactive_role: IdRequest, user: UserDetailResponse = Depends(
        get_current_user([roles.SUPER_ADMIN_ROLE, roles.SYSTEM_ADMIN_ROLE]))) -> Response:
        data = await service.role.inactive_role(user_id=inactive_role.id, update_by=user.id)
        return Response.ok(data)

    @router.post("/list", tags=["role"])
    async def list_role(self, search_request: RoleSearchRequest,
                        user: UserDetailResponse = Depends(get_current_user([roles.SUPER_ADMIN_ROLE]))):
        data = await service.role.list_roles(search_request)
        return Response.ok(data)

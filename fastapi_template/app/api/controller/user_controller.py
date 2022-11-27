from fastapi import Depends

from fastapi_template.app import service
from fastapi_template.app.api.deps import get_current_user
from fastapi_template.app.core import Response
from fastapi_template.app.core.cvb import cbv
from fastapi_template.app.core.inferring_router import InferringRouter
from fastapi_template.app.entity.user_entity import UserDetail, UserSearchRequest, UserCreateRequest, UserUpdateRequest
from fastapi_template.config import roles

router = InferringRouter()


@cbv(router)
class UserController:

    @router.get("/detail")
    async def get_user_detail(self, user: UserDetail = Depends(get_current_user())) -> Response:
        return Response.ok(user)

    @router.post("/add")
    async def create_user(self, create_user: UserCreateRequest,
                          user: UserDetail = Depends(get_current_user([roles.SUPER_ADMIN_ROLE]))) -> Response:
        data = await service.user.create_user(create_user, create_by=user.id)
        return Response.ok(data)

    @router.put("/update")
    async def update_user(self, update_user: UserUpdateRequest,
                          user: UserDetail = Depends(get_current_user([roles.SUPER_ADMIN_ROLE]))) -> Response:
        data = await service.user.update_user(update_user, update_by=user.id)
        return Response.ok(data)

    @router.post("/list")
    async def list_user(self, user_request: UserSearchRequest,
                        user: UserDetail = Depends(get_current_user([roles.SUPER_ADMIN_ROLE]))) -> Response:
        users = await service.user.get_users(user_request)
        return Response.ok(users)

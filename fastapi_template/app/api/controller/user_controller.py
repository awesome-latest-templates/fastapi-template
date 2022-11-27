from fastapi import Depends

from fastapi_template.app import service
from fastapi_template.app.api.deps import get_current_user
from fastapi_template.app.core import Response
from fastapi_template.app.core.cvb import cbv
from fastapi_template.app.core.inferring_router import InferringRouter
from fastapi_template.app.entity.user_entity import UserDetail, UserSearchRequest
from fastapi_template.config import roles

router = InferringRouter()


@cbv(router)
class UserRouter:

    @router.get("/detail")
    async def get_user_detail(self, user: UserDetail = Depends(get_current_user())) -> Response:
        return Response.ok(user)

    @router.post("/list")
    async def list_user(self, user_request: UserSearchRequest,
                        user: UserDetail = Depends(get_current_user([roles.SUPER_ADMIN_ROLE]))) -> Response:
        users = await service.user.get_users(user_request)
        return Response.ok(users)

from fastapi_template.app.core import Response
from fastapi_template.app.core.cvb import cbv
from fastapi_template.app.core.inferring_router import InferringRouter
from fastapi_template.app.entity.user_entity import UserLoginRequest
from fastapi_template.app.service.user_service import UserService

router = InferringRouter()


@cbv(router)
class UserRouter:
    user_service = UserService()

    @router.post("/login")
    async def get_all_users(self, user: UserLoginRequest) -> Response:
        token_data = await self.user_service.login(user)
        return Response.ok(token_data)

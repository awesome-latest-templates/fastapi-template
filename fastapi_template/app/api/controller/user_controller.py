from fastapi import Depends

from fastapi_template.app import service
from fastapi_template.app.api.deps import oauth2_scheme
from fastapi_template.app.core import Response
from fastapi_template.app.core.cvb import cbv
from fastapi_template.app.core.inferring_router import InferringRouter
from fastapi_template.app.entity.user_entity import UserLoginRequest

router = InferringRouter()


@cbv(router)
class UserRouter:

    @router.post("/auth")
    async def create_token_async(self, user: UserLoginRequest) -> Response:
        token_data = await service.user.create_token_async(user)
        return Response.ok(token_data)

    @router.get("/test")
    def test(self, token: str = Depends(oauth2_scheme)):
        return Response.ok(token)

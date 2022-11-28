from fastapi_template.app import service
from fastapi_template.app.core.cvb import cbv
from fastapi_template.app.core.inferring_router import InferringRouter
from fastapi_template.app.schema.auth_schema import TokenResponse, AuthLoginRequest

router = InferringRouter()


@cbv(router)
class AuthController:

    @router.post("/login", name="Create access token via username and password", tags=["auth"])
    async def create_token_async(self, form_data: AuthLoginRequest) -> TokenResponse:
        token_data = await service.auth.create_token_async(form_data)
        return token_data

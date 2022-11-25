from fastapi import UploadFile, File, Depends
from starlette.requests import Request

from fastapi_template.app import service
from fastapi_template.app.api import deps
from fastapi_template.app.api.deps import get_current_user
from fastapi_template.app.core import Response, ResponseCode
from fastapi_template.app.core.cvb import cbv
from fastapi_template.app.core.inferring_router import InferringRouter
from fastapi_template.app.entity.user_entity import UserDetail

router = InferringRouter()


@cbv(router)
class FileController:

    @router.post("/upload")
    async def upload_file(self,
                          request: Request,
                          file: UploadFile = File(...),
                          file_size: int = Depends(deps.valid_content_length),
                          user: UserDetail = Depends(get_current_user())) -> Response:
        # check file payload data
        if not file:
            return Response.fail(ResponseCode.BAD_REQUEST, "no upload file received")
        if not (user and user.id):
            return Response.fail(ResponseCode.BAD_REQUEST, "no upload file received")
        user_id = user.id
        resp = await service.file.upload_file(request=request, file=file, file_size=file_size, user_id=user_id)
        return Response.ok(resp)

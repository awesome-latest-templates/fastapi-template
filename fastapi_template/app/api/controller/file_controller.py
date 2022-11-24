from fastapi import UploadFile

from fastapi_template.app.core import Response, ResponseCode
from fastapi_template.app.core.cvb import cbv
from fastapi_template.app.core.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class FileController:

    @router.post("/upload")
    def upload_file(self, file: UploadFile | None = None) -> Response:
        # payload data
        if not file:
            return Response.fail(ResponseCode.BAD_REQUEST, "no upload file received")

        return Response.ok()

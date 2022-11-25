import os
import uuid

import aiofiles
from fastapi import UploadFile
from starlette import status
from starlette.requests import Request

from fastapi_template.app import crud
from fastapi_template.app.core.log import logger
from fastapi_template.app.entity.file_entity import FileCreateRequest, FileResponse
from fastapi_template.app.exception import HttpException
from fastapi_template.config import settings


class FileService:

    async def upload_file(self, request: Request, file: UploadFile, file_size: int, user_id: int) -> FileResponse:
        # save the file
        file_content_type = file.content_type
        file_key = str(uuid.uuid4().hex)
        upload_file_size = 0
        original_filename, file_extension = os.path.splitext(file.filename)
        new_file_name = f"{file_key}{file_extension}"
        file_path = f"{settings.FILE_UPLOAD_FOLDER}/{new_file_name}"
        try:
            async with aiofiles.open(file_path, "wb") as out_file:
                while content := await file.read(settings.FILE_READ_CHUNK_SIZE):  # async read chunk
                    upload_file_size += len(content)
                    if upload_file_size > file_size:
                        raise HttpException(
                            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail="Too large file, file shoult not exceed ",
                        )
                    await out_file.write(content)  # async write chunk
            msg = f"Successfully uploaded {file.filename} for processing"
        except IOError:
            msg = "There was an error uploading your file"
        logger.info(msg)
        # save into database
        file_url = f"{settings.FILE_URL_PREFIX}/{new_file_name}"
        file_entity = FileCreateRequest(file_key=file_key,
                                        file_url=file_url,
                                        file_name=new_file_name,
                                        file_size=upload_file_size,
                                        content_type=file_content_type)
        created_file = await crud.file.create(create_entity=file_entity, created_by=user_id)
        access_url = f"{str(request.base_url)[:-1]}{file_url}"
        resp = FileResponse(file_key=file_key, file_url=access_url, upload_time=created_file.update_time)
        return resp


file = FileService()

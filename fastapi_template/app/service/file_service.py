import os
import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile
from fastapi_pagination import Params, Page
from loguru import logger
from sqlalchemy import select
from starlette import status
from starlette.requests import Request

from fastapi_template.app import crud
from fastapi_template.app.core import ResponseCode
from fastapi_template.app.entity.file_entity import FileCreateRequest, FileResponse, FileSearchRequest
from fastapi_template.app.exception import HttpException
from fastapi_template.app.model import FileInfo
from fastapi_template.config import settings


class FileService:

    async def upload_file(self, request: Request, file: UploadFile, file_size: int, user_id: int) -> FileResponse:
        # save the file
        file_content_type = file.content_type
        file_key = str(uuid.uuid4().hex)
        upload_file_size = 0
        original_filename, file_extension = os.path.splitext(file.filename)
        new_file_name = f"{file_key}{file_extension}"
        file_path = f"{settings.FILE_UPLOAD_FOLDER or str(Path.home())}/{new_file_name}"
        try:
            async with aiofiles.open(file_path, "wb") as out_file:
                while content := await file.read(settings.FILE_READ_CHUNK_SIZE):  # async read chunk
                    upload_file_size += len(content)
                    if upload_file_size > file_size:
                        raise HttpException(
                            code=ResponseCode.BAD_REQUEST,
                            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail="File size exceeded the maximum allowed",
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
        created_file = await crud.file.add(create_entity=file_entity, created_by=user_id)
        access_url = f"{str(request.base_url)[:-1]}{file_url}"
        resp = FileResponse(file_key=file_key, file_url=access_url, upload_time=created_file.update_time)
        return resp

    async def list_files(self, search: FileSearchRequest) -> Page[FileInfo]:
        page_num = search.page
        page_size = search.size
        params = Params(page=page_num, size=page_size)
        results: Page[FileInfo] = await crud.file.list_paginated_ordered(
            query=select(FileInfo).where(FileInfo.is_active == 1).order_by(FileInfo.create_time.desc()),
            params=params
        )
        return results


file = FileService()

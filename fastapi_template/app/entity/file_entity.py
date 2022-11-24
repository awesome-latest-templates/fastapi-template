from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel


class FileCreate(BaseModel):
    file: UploadFile
    file_key: UUID
    file_url: str
    file_name: str


class FileUpdate(BaseModel):
    pass


class FileResponse(BaseModel):
    file_key: str = None
    file_url: str = None
    update_time: str = None

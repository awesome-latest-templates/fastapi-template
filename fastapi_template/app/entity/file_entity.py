from pydantic import BaseModel

from fastapi_template.app.entity.common_entity import PageParamModel


class FileCreateRequest(BaseModel):
    file_key: str
    file_url: str
    file_name: str
    file_size: int
    content_type: str


class FileUpdateRequest(BaseModel):
    pass


class FileSearchRequest(PageParamModel):
    pass


class FileResponse(BaseModel):
    file_key: str = None
    file_url: str = None
    upload_time: str = None

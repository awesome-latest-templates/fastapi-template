from fastapi_template.app.entity.base_entity import BasePageParamModel, BaseEntityModel


class FileCreateRequest(BaseEntityModel):
    file_key: str
    file_url: str
    file_name: str
    file_size: int
    content_type: str


class FileUpdateRequest(BaseEntityModel):
    pass


class FileSearchRequest(BasePageParamModel):
    pass


class FileResponse(BaseEntityModel):
    file_key: str = None
    file_url: str = None
    upload_time: str = None

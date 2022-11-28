from fastapi_template.app.schema.base_schema import BasePageParamModel, BaseSchemaModel


class FileCreateRequest(BaseSchemaModel):
    file_key: str
    file_url: str
    file_name: str
    file_size: int
    content_type: str


class FileUpdateRequest(BaseSchemaModel):
    pass


class FileSearchRequest(BasePageParamModel):
    pass


class FileResponse(BaseSchemaModel):
    file_key: str = None
    file_url: str = None
    upload_time: str = None

from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.model import FileInfo
from fastapi_template.app.schema.file_schema import FileCreateRequest, FileUpdateRequest


class FileCrud(BaseCrud[FileInfo, FileCreateRequest, FileUpdateRequest]):
    pass


file = FileCrud(FileInfo)

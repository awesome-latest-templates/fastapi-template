from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.entity.file_entity import FileCreateRequest, FileUpdateRequest
from fastapi_template.app.model import FileInfo


class FileCrud(BaseCrud[FileInfo, FileCreateRequest, FileUpdateRequest]):
    pass


file = FileCrud(FileInfo)

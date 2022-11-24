from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.entity.file_entity import FileCreate, FileUpdate
from fastapi_template.app.model import FileInfo


class FileCrud(BaseCrud[FileInfo, FileCreate, FileUpdate]):
    pass


file = FileCrud(FileInfo)

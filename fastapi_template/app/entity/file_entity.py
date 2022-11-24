from pydantic import BaseModel


class FileResponse(BaseModel):
    file_key: str = None
    file_url: str = None
    update_time: str = None

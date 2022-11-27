from sqlalchemy import Column, Text, text

from fastapi_template.app.model import BaseSQLModel


class FileInfo(BaseSQLModel):
    file_key = Column(Text, nullable=False)
    file_url = Column(Text, nullable=False)
    file_name = Column(Text, server_default=text("''"))
    file_size = Column(Text, server_default=text('0'))
    content_type = Column(Text, server_default=text("''"))

from sqlalchemy import Column, Text, text

from fastapi_template.app.model import BaseSQLModel


class Project(BaseSQLModel):
    name = Column(Text, nullable=False, server_default=text("''"))
    description = Column(Text)

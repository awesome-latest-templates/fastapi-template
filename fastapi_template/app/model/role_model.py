from sqlalchemy import Column, Text, text

from fastapi_template.app.model.base_model import BaseSQLModel


class Role(BaseSQLModel):
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False, server_default=text("''"))

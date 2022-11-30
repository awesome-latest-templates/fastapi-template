from sqlalchemy import Column, Text, text

from fastapi_template.app.model.base_model import BaseSQLModel


class Setting(BaseSQLModel):
    setting_type = Column(Text, nullable=False, server_default=text("''"))
    setting_value = Column(Text, server_default=text("''"))

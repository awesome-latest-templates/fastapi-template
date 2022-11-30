from sqlalchemy import Column, Text, text

from fastapi_template.app.model.base_model import BaseSQLModel


class User(BaseSQLModel):
    user_name = Column(Text, nullable=False, server_default=text("''"))
    password = Column(Text, nullable=False, server_default=text("''"))

    nick_name = Column(Text, server_default=text("''"))
    email = Column(Text, server_default=text("''"))
    last_login_time = Column(Text)
    avatar = Column(Text)

from sqlalchemy import Column, Integer, Text, text

from fastapi_template.app.model import BaseSQLModel


class Menu(BaseSQLModel):
    pid = Column(Integer, nullable=False, server_default=text('0'))
    title = Column(Text, nullable=False, server_default=text("''"))
    keep_alive = Column(Integer, nullable=False, server_default=text('1'))
    name = Column(Text)
    type = Column(Text)
    path = Column(Text)
    icon = Column(Text)
    menu_type = Column(Text)
    component = Column(Text)
    extend = Column(Text)
    remark = Column(Text)

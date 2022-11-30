from sqlalchemy import Column, Integer

from fastapi_template.app.model.base_model import BaseSQLModel


class UserRole(BaseSQLModel):
    user_id = Column(Integer, nullable=False)
    role_id = Column(Integer, nullable=False)

from sqlalchemy import Column, Integer

from fastapi_template.app.model.base_model import BaseSQLModel


class ProjectMember(BaseSQLModel):
    project_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

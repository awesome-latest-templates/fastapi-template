from typing import List, TypeVar

from pydantic import BaseModel
from sqlmodel import SQLModel

EntityType = TypeVar("EntityType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=SQLModel)


def map_models_entities(models: List[ModelType], entity: EntityType):
    return list(map(lambda model: entity.from_orm(model), models))

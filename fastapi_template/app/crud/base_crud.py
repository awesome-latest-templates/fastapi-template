from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Result
from sqlmodel import SQLModel, select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select

from fastapi_template.app.core.db import db
from fastapi_template.app.entity.common_entity import OrderEnum

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateEntityType = TypeVar("CreateEntityType", bound=BaseModel)
UpdateEntityType = TypeVar("UpdateEntityType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class BaseCrud(Generic[ModelType, CreateEntityType, UpdateEntityType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLModel model class
        * `entity`: A Pydantic model (entity) class
        """
        self.model = model

    async def get_by_id(self,
                        *,
                        item_id: Union[UUID, str, int],
                        db_session: Optional[AsyncSession] = None,
                        ) -> Optional[ModelType]:
        """
        Get the item data by id
        :param item_id:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        query = select(self.model).where(self.model.id == item_id)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_by_ids(self,
                         *,
                         list_ids: List[Union[UUID, str, int]],
                         db_session: Optional[AsyncSession] = None,
                         ) -> Optional[List[ModelType]]:
        """
        Get the item data by ids
        :param list_ids:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        response = await db_session.execute(
            select(self.model).where(self.model.id.in_(list_ids))
        )
        return response.scalars().all()

    async def get_count(self,
                        db_session: Optional[AsyncSession] = None,
                        ) -> Optional[ModelType]:
        """
        Get the item data count
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        response = await db_session.execute(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.scalar_one()

    async def get_many(self,
                       *,
                       skip: int = 0,
                       limit: int = 100,
                       query: Optional[Union[T, Select[T]]] = None,
                       db_session: Optional[AsyncSession] = None,
                       ) -> List[ModelType]:
        """
        Get all the item data
        :param skip:
        :param limit:
        :param query:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        if query is None:
            query = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        response = await db_session.execute(query)
        return response.scalars().all()

    async def get_many_paginated(self,
                                 *,
                                 params: Optional[Params] = Params(),
                                 query: Optional[Union[T, Select[T]]] = None,
                                 db_session: Optional[AsyncSession] = None,
                                 ) -> Page[ModelType]:
        """
        Get all the item data with pagination
        :param params:
        :param query:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        if query is None:
            query = select(self.model)
        return await paginate(db_session, query, params)  # type: ignore

    async def get_many_paginated_ordered(self,
                                         *,
                                         params: Optional[Params] = Params(),
                                         query: Optional[Union[T, Select[T]]] = None,
                                         order_by: Optional[str] = None,
                                         order: Optional[OrderEnum] = OrderEnum.descendent,
                                         db_session: Optional[AsyncSession] = None,
                                         ) -> Page[ModelType]:
        """
        Get all the item data with pagination and order
        :param params:
        :param order_by:
        :param order:
        :param query:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        columns = self.model.__table__.columns

        if order_by not in columns or order_by is None:
            order_by = self.model.id

        if query is None:
            if order == OrderEnum.ascendent:
                query = select(self.model).order_by(columns[order_by.value].asc())
            else:
                query = select(self.model).order_by(columns[order_by.value].desc())

        return await paginate(db_session, query, params)  # type: ignore

    async def get_many_ordered(self,
                               *,
                               order_by: Optional[str] = None,
                               order: Optional[OrderEnum] = OrderEnum.descendent,
                               skip: int = 0,
                               limit: int = 100,
                               db_session: Optional[AsyncSession] = None,
                               ) -> List[ModelType]:
        """
        Get all the Item data and order by
        :param order_by:
        :param order:
        :param skip:
        :param limit:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        columns = self.model.__table__.columns

        if order_by not in columns or order_by is None:
            order_by = self.model.id

        if order == OrderEnum.ascendent:
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .order_by(columns[order_by.value].asc())
            )
        else:
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .order_by(columns[order_by.value].desc())
            )

        response = await db_session.execute(query)
        return response.scalars().all()

    async def create(self,
                     *,
                     create_entity: Union[CreateEntityType, ModelType],
                     created_by: Optional[Union[UUID, str, int]] = None,
                     db_session: Optional[AsyncSession] = None,
                     ) -> ModelType:
        """
        Create the item data
        :param create_entity:
        :param created_by:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        db_obj = self.model.from_orm(create_entity)  # type: ignore
        db_obj.create_time = datetime.utcnow()
        db_obj.update_time = datetime.utcnow()
        if created_by:
            db_obj.create_by = created_by

        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def update(self,
                     *,
                     current_entity: ModelType,
                     update_entity: Union[UpdateEntityType, Dict[str, Any], ModelType],
                     db_session: Optional[AsyncSession] = None,
                     ) -> ModelType:
        """
        Update the item data by previous model data
        :param current_entity:
        :param update_entity:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        obj_data = jsonable_encoder(current_entity)

        if isinstance(update_entity, dict):
            update_data = update_entity
        else:
            update_data = update_entity.dict(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in obj_data:
            if field in update_data:
                setattr(current_entity, field, update_data[field])
            if field == "update_time":
                setattr(current_entity, field, datetime.utcnow())

        db_session.add(current_entity)
        await db_session.commit()
        await db_session.refresh(current_entity)
        return current_entity

    async def update_by_id(self,
                           *,
                           item_id: Union[UUID, str, int],
                           update_entity: Union[UpdateEntityType, Dict[str, Any], ModelType],
                           db_session: Optional[AsyncSession] = None,
                           ) -> ModelType:
        """
        Update the item data by id
        :param item_id:
        :param current_entity:
        :param update_entity:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        current_entity: Optional[ModelType] = await self.get_by_id(item_id=item_id, db_session=db_session)
        update_result = await self.update(current_entity=current_entity,
                                          update_entity=update_entity,
                                          db_session=db_session)
        return update_result

    async def remove(self,
                     *,
                     item_id: Union[UUID, str, int],
                     db_session: Optional[AsyncSession] = None
                     ) -> ModelType:
        """
        Remove the item data by item id
        :param item_id:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        response = await db_session.execute(
            select(self.model).where(self.model.id == item_id)
        )
        obj = response.scalar_one()
        await db_session.delete(obj)
        await db_session.commit()
        return obj

    async def execute(self,
                      statement: str,
                      **kwargs
                      ) -> Result:
        """
        Execute the raw sql
        :param statement:
        :param params:
        :param id:
        :param db_session:
        :return:
        """
        db_session = db.session
        response = await db_session.execute(text(statement).execution_options(autocommit=True), kwargs)
        return response.fetchall()

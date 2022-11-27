from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import func, select, text
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import TextClause

from fastapi_template.app.core.db import db
from fastapi_template.app.entity.common_entity import OrderEnum, PageDataModel
from fastapi_template.app.model.base_model import BaseSQLModel

ModelType = TypeVar("ModelType", bound=BaseSQLModel)
CreateEntityType = TypeVar("CreateEntityType", bound=BaseModel)
UpdateEntityType = TypeVar("UpdateEntityType", bound=BaseModel)
EntityType = TypeVar("EntityType", bound=BaseModel)
T = TypeVar("T", bound=BaseSQLModel)


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
        query = select(self.model).where(self.model.id.in_(list_ids))
        response = await db_session.execute(query)
        return response.scalars().all()

    async def count(self,
                    db_session: Optional[AsyncSession] = None,
                    ) -> Optional[ModelType]:
        """
        Get the item data count
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        query = select(func.count()).select_from(select(self.model).subquery())
        response = await db_session.execute(query)
        return response.scalar_one()

    async def list(self,
                   *,
                   query: Optional[Select] = None,
                   db_session: Optional[AsyncSession] = None,
                   ) -> List[ModelType]:
        """
        Get all the item data
        :param offset:
        :param limit:
        :param query:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        if query is None:
            query = select(self.model).order_by(self.model.id)
        response = await db_session.execute(query)
        return response.scalars().all()

    async def list_ordered(self,
                           *,
                           query: Optional[Select] = None,
                           order_by: Optional[str] = None,
                           order: Optional[OrderEnum] = OrderEnum.descendent,
                           db_session: Optional[AsyncSession] = None,
                           ) -> List[ModelType]:
        """
        Get all the Item data and order by
        :param order_by:
        :param order:
        :param offset:
        :param limit:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        columns = self.model.__table__.columns

        if (order_by and order_by not in columns) or order_by is None:
            order_by = self.model.id

        if query is None:
            query = (
                select(self.model)
                .order_by(columns[order_by].asc())
            ) if order == OrderEnum.ascendent else (
                select(self.model)
                .order_by(columns[order_by].desc())
            )
        else:
            query = query.order_by(order_by)

        response = await db_session.execute(query)
        return response.scalars().all()

    async def list_paginated(self,
                             *,
                             query: Optional[Select] = None,
                             params: Optional[Params] = Params(),
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

    async def list_paginated_ordered(self,
                                     *,
                                     query: Optional[Select] = None,
                                     params: Optional[Params] = Params(),
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

        if (order_by and order_by not in columns) or order_by is None:
            order_by = self.model.id

        if query is None:
            if order == OrderEnum.ascendent:
                query = select(self.model).order_by(order_by.asc())
            else:
                query = select(self.model).order_by(order_by.desc())

        return await paginate(db_session, query, params)  # type: ignore

    async def add(self,
                  *,
                  create_entity: Union[CreateEntityType, Dict[str, Any], ModelType],
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
        db_obj = create_entity
        if isinstance(create_entity, BaseModel):
            create_entity = jsonable_encoder(create_entity)
            db_obj = self.model(**create_entity)
        elif isinstance(create_entity, dict):
            create_entity = create_entity
            db_obj = self.model(**create_entity)  # type: ignore
        db_obj.create_time = datetime.utcnow()
        db_obj.update_time = datetime.utcnow()
        if created_by:
            db_obj.create_by = created_by

        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def add_all(self,
                      *,
                      create_entities: Union[List[CreateEntityType], List[Dict[str, Any]], List[ModelType]],
                      created_by: Optional[Union[UUID, str, int]] = None,
                      db_session: Optional[AsyncSession] = None,
                      ) -> List[ModelType]:
        """
        Batch to create the item data
        :param create_entities:
        :param created_by:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        await db_session.begin()
        try:
            db_objs = []
            for create_entity in create_entities:
                db_model = create_entity
                if isinstance(create_entity, BaseModel):
                    create_entity = jsonable_encoder(create_entity)
                    db_model = self.model(**create_entity)
                elif isinstance(create_entity, dict):
                    create_entity = create_entity
                    db_model = self.model(**create_entity)  # type: ignore
                db_model.create_time = datetime.utcnow()
                db_model.update_time = datetime.utcnow()
                if created_by:
                    db_model.create_by = created_by
                db_objs.append(db_model)

            db_session.add_all(db_objs)
            await db_session.commit()
            await db_session.refresh(db_objs)
            return db_objs
        except:
            await db_session.rollback()

    async def update(self,
                     *,
                     current_model: ModelType,
                     update_entity: Union[UpdateEntityType, Dict[str, Any], ModelType],
                     db_session: Optional[AsyncSession] = None,
                     ) -> ModelType:
        """
        Update the item data by previous model data
        :param current_model:
        :param update_entity:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        obj_data: dict = jsonable_encoder(current_model)

        if isinstance(update_entity, dict):
            update_data = update_entity
        else:
            update_data = update_entity.dict(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in obj_data:
            if field in update_data:
                setattr(current_model, field, update_data[field])
            if field == "update_time":
                setattr(current_model, field, datetime.utcnow())

        db_session.add(current_model)
        await db_session.commit()
        await db_session.refresh(current_model)
        return current_model

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
        update_result = await self.update(current_model=current_entity,
                                          update_entity=update_entity,
                                          db_session=db_session)
        return update_result

    async def delete(self,
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
        query = select(self.model).where(self.model.id == item_id)
        response = await db_session.execute(query)
        obj = response.scalar_one()
        await db_session.delete(obj)
        await db_session.commit()
        return obj

    async def delete_all(self,
                         *,
                         item_ids: Union[List[UUID], List[str], List[int]],
                         db_session: Optional[AsyncSession] = None
                         ) -> List[ModelType]:
        """
        Remove the item data by item id
        :param item_ids:
        :param db_session:
        :return:
        """
        db_session = db_session or db.session
        await db_session.begin()
        try:
            objs = []
            for item_id in item_ids:
                obj = await self.delete(item_id=item_id, db_session=db_session)
                objs.append(obj)
            return objs
        except:
            await db_session.rollback()

    async def execute(self,
                      sql: str,
                      params: dict = None,
                      entity: EntityType = None,
                      db_session: Optional[AsyncSession] = None
                      ) -> Union[List[EntityType], PageDataModel, List[RowMapping]]:
        """
        Execute the raw sql
        :param sql: raw native sql statement
        :param entity: pydantic entity object
        :param params: the sql parameters
        :param db_session:
        :return:
        """
        params = params if params else {}
        db_session = db_session or db.session
        raw_statement: TextClause = text(sql)
        total, page_num, page_size = 0, 0, 0
        is_pagination = False
        if "page" in params and "size" in params:
            is_pagination = True
            page_num = params["page"]
            page_size = params["size"]
            offset = page_size * (page_num - 1)
            params.pop("page", None)
            params.pop("size", None)
            count_query = text(f"SELECT COUNT(*) FROM ({raw_statement.text})")
            total = await db_session.scalar(count_query, params=params)
            raw_statement = text(f"{raw_statement.text} LIMIT {page_size} OFFSET {offset}")

        response = await db_session.execute(raw_statement, params=params)
        results: List[RowMapping] = response.mappings().unique().all()
        if entity is None and results:
            return results
        # convert to pydantic object
        entities = list(map(lambda model: entity.parse_obj(model), results))
        if not is_pagination:
            return entities
        page_entities = PageDataModel(total=total, page=page_num, size=page_size, items=entities)
        return page_entities

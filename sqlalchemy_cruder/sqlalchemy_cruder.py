"""Main module."""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from contextlib import contextmanager
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from app.db.base import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDER(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session_maker: sessionmaker[Session]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """

        # 检查 model 是否满足条件
        def is_declarative_subclass(cls):
            for base in cls.__mro__:
                if type(base) is DeclarativeMeta:
                    return True
            return False

        if not is_declarative_subclass(model):
            raise ValueError(f"model must be a subclass of a class with DeclarativeMeta metaclass, got {model}")

        self.model = model
        self.session_maker = session_maker
        self.db: Optional[Session] = None

    @contextmanager
    def get_db_session(self):
        db = self.session_maker()
        try:
            yield db
        finally:
            db.close()

    def query_by_condition(self, condition: CreateSchemaType) -> List[ModelType]:
        """
        根据指定的 BaseModel 对象条件查询数据库记录。
        **参数**
        * `condition`: 一个 Pydantic 的 BaseModel 对象，用于指定查询条件。
        **返回**
        * 满足条件的记录列表。
        """

        with self.get_db_session() as db:
            query = db.query(self.model)
            condition_data = condition.dict(exclude_unset=True)
            for field, value in condition_data.items():
                query = query.filter(getattr(self.model, field) == value)
            return query.all()

    def query_by_id(self, id: Any) -> Optional[ModelType]:
        with self.get_db_session() as db:
            return db.query(self.model).filter(self.model.id == id).first()

    def query_by_pagination(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        with self.get_db_session() as db:
            return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        with self.get_db_session() as db:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)  # type: ignore
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

    def update(self, db_obj: Optional[ModelType], obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> Optional[ModelType]:
        with self.get_db_session() as db:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

    def remove(self, id: int) -> Optional[ModelType]:
        with self.get_db_session() as db:
            obj = db.query(self.model).get(id)
            db.delete(obj)
            db.commit()
            return obj


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

    @contextmanager
    def transaction(self):
        db = self.session_maker()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
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

    def query_by_like(self, field: str, value: str) -> List[ModelType]:
        with self.get_db_session() as db:
            return db.query(self.model).filter(getattr(self.model, field).like(f"%{value}%")).all()

    def query_by_range(self, field: str, start: Any, end: Any) -> List[ModelType]:
        with self.get_db_session() as db:
            return db.query(self.model).filter(getattr(self.model, field).between(start, end)).all()

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

    def create_multi(self, objs_in: List[CreateSchemaType]) -> List[ModelType]:
        with self.transaction() as db:
            db_objs = []
            for obj_in in objs_in:
                obj_in_data = jsonable_encoder(obj_in)
                db_obj = self.model(**obj_in_data)
                db.add(db_obj)
                db_objs.append(db_obj)
            return db_objs

    def update_multi(self, db_objs: List[ModelType], obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> List[ModelType]:
        with self.transaction() as db:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for db_obj in db_objs:
                obj_data = jsonable_encoder(db_obj)
                for field in obj_data:
                    if field in update_data:
                        setattr(db_obj, field, update_data[field])
                db.add(db_obj)
            return db_objs

    def remove_multi(self, ids: List[int]) -> List[Optional[ModelType]]:
        with self.transaction() as db:
            removed_objs = []
            for id in ids:
                obj = db.query(self.model).get(id)
                if obj:
                    db.delete(obj)
                    removed_objs.append(obj)
            return removed_objs

    def combined_operation(self, create_obj: CreateSchemaType, update_obj: ModelType, update_data: Union[UpdateSchemaType, Dict[str, Any]]):
        with self.transaction() as db:
            # 创建操作
            obj_in_data = jsonable_encoder(create_obj)
            db_create_obj = self.model(**obj_in_data)
            db.add(db_create_obj)

            # 更新操作
            if isinstance(update_data, dict):
                update_dict = update_data
            else:
                update_dict = update_data.dict(exclude_unset=True)
            for field in jsonable_encoder(update_obj):
                if field in update_dict:
                    setattr(update_obj, field, update_dict[field])
            db.add(update_obj)

            return db_create_obj, update_obj

    def execute_query(self, statement) -> List[ModelType]:
        """
        执行查询语句
        :param statement: SQLAlchemy 查询语句
        :return: 查询结果列表
        """
        with self.get_db_session() as db:
            result = db.execute(statement)
            return result.scalars().all()

    def execute_statement(self, statement) -> int:
        """
        执行非查询语句（如更新、删除等）
        :param statement: SQLAlchemy 非查询语句
        :return: 受影响的行数
        """
        with self.get_db_session() as db:
            result = db.execute(statement)
            db.commit()
            return result.rowcount



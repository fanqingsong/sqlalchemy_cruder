"""Main module."""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

# from typing import Any

# from sqlalchemy.ext.declarative import as_declarative, declared_attr


# @as_declarative()
# class Base:
#     id: Any
#     __name__: str
#     # Generate __tablename__ automatically
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()


# from app.db.base_class import Base


def create_cruder_by_base(base_class: Any):
    ModelType = TypeVar("ModelType", bound=base_class)
    CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
    UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

    class CRUDER(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
        def __init__(self, model: Type[ModelType], db: Session):
            """
            CRUD object with default methods to Create, Read, Update, Delete (CRUD).
            **Parameters**
            * `model`: A SQLAlchemy model class
            * `schema`: A Pydantic model (schema) class
            """
            self.model = model
            self.db = db

        def get(self, id: Any) -> Optional[ModelType]:
            return self.db.query(self.model).filter(self.model.id == id).first()

        def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
            return self.db.query(self.model).offset(skip).limit(limit).all()

        def create(self, obj_in: CreateSchemaType) -> ModelType:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)  # type: ignore
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj

        def update(self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj

        def remove(self, id: int) -> Optional[ModelType]:
            obj = self.db.query(self.model).get(id)
            self.db.delete(obj)
            self.db.commit()
            return obj

    return CRUDER

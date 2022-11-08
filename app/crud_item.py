from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sqlachemy_cruder.sqlachemy_cruder import CRUDBase
from app.model_item import Item
from app.schema_item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    pass


item = CRUDItem(Item)






from app.model.model_item import Item
from app.schema.schema_item import ItemCreate, ItemUpdate
from sqlalchemy_cruder.sqlalchemy_cruder import CRUDER
from app.db.base import Base


# class CRUDItem(CRUDER[Item, ItemCreate, ItemUpdate]):
#     pass
#

class CRUDItem(CRUDER):
    pass






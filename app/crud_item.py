
from sqlachemy_cruder.sqlachemy_cruder import CRUDER
from app.model_item import Item
from app.schema_item import ItemCreate, ItemUpdate


class CRUDItem(CRUDER[Item, ItemCreate, ItemUpdate]):
    pass







from app.model_item import Item
from app.schema_item import ItemCreate, ItemUpdate
from sqlalchemy_cruder.sqlalchemy_cruder import create_cruder_by_base
from app.db.base_class import Base

CRUDER = create_cruder_by_base(Base)

class CRUDItem(CRUDER[Item, ItemCreate, ItemUpdate]):
    pass






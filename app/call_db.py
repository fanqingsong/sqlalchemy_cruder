import logging

from app.cruder.crud_item import CRUDItem
from app.db import base  # noqa: F401
from app.db.session import engine
from app.model.model_item import Item
from app.schema.schema_item import ItemCreate, ItemUpdate
from app.db.session import SessionLocal


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def call_db() -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    base.Base.metadata.create_all(bind=engine)

    item_in = ItemCreate(
        title='sss',
        description='ttt'
    )

    item = CRUDItem(Item, SessionLocal)

    item.create(item_in)

    res = item.query_by_id(1)
    logging.info(res.__dict__)

    item_update = ItemUpdate(
        title='sss11',
        description='ttt11'
    )
    res = item.update(res, item_update)
    logging.info(res.__dict__)

    res_multi = item.query_by_pagination()
    logging.info(res_multi)




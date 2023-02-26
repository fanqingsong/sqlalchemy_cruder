import logging

from app.crud_item import CRUDItem
from app.db import base  # noqa: F401
from app.db.session import engine
from app.model_item import Item
from app.schema_item import ItemCreate, ItemUpdate
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

    item = CRUDItem(Item, SessionLocal())

    item.create(item_in)

    res = item.get(1)
    logging.info(res.__dict__)

    item_in = ItemUpdate(
        title='sss11',
        description='ttt11'
    )
    res = item.update(res, item_in)
    logging.info(res.__dict__)

    res = item.get_multi()
    logging.info(res)




from sqlalchemy.orm import Session

from app.crud_item import item
from app.schema_item import ItemCreate
from app.db import base  # noqa: F401
from app.db.session import engine

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    base.Base.metadata.create_all(bind=engine)

    item_in = ItemCreate(
        title='sss',
        description='ttt'
    )

    item.create(db, item_in)

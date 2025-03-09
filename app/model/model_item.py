
from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.base import Base


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), index=True)
    description = Column(String(64), index=True)



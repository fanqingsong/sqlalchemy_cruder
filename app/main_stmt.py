import logging
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, select, update
from sqlalchemy_cruder.sqlalchemy_cruder import CRUDER
from pydantic import BaseModel

# Create a base class for declarative models
Base = declarative_base()

# Create a base class for declarative models
Base = declarative_base()

# Define the User model class
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Define Pydantic schemas for create and update operations
class UserCreate(BaseModel):
    name: str

class UserUpdate(BaseModel):
    name: str

# Example database configuration
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

# Create all tables
Base.metadata.create_all(engine)

# 创建 CRUDER 实例
# cruder = CRUDER[User, UserCreate, UserUpdate](model=User, session_maker=Session)
# cruder = CRUDER(model=User, session_maker=Session)


# 改进后的创建 CRUDER 实例方式
def create_cruder(model, create_schema, update_schema, session_maker):
    return CRUDER[model, create_schema, update_schema](model=model, session_maker=session_maker)

# 创建 CRUDER 实例
cruder = create_cruder(User, UserCreate, UserUpdate, Session)


# Insert a sample user
user_create = UserCreate(name='old_name')
created_user = cruder.create(user_create)

# Query example
select_stmt = select(User).where(User.id == created_user.id)
results = cruder.execute_query(select_stmt)
print("Query results:", results)

# Update example
update_stmt = (
    update(User).
    where(User.id == created_user.id).
    values(name='new_name')
)
affected_rows = cruder.execute_statement(update_stmt)
print("Affected rows:", affected_rows)



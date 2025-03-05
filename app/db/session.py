from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine("mysql://root:mysqlpw@localhost:49153/dev")
engine = create_engine('sqlite:///test22.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

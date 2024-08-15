from sqlalchemy import Column, Integer, String
from ORMDatabases import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    Token = Column(String(300), unique=True)

# Base.metadata.create_all(engine)

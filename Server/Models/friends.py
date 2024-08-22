from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ORMDatabases import Base, engine

friendship_table = Table(
    'friendship', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class LocalUser(Base):
    __tablename__ = 'localuser'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(99), unique=True, index=True)

    # Relationships
    friends = relationship(
        'LocalUser',
        secondary=friendship_table,
        primaryjoin=id==friendship_table.c.user_id,
        secondaryjoin=id==friendship_table.c.friend_id,
        backref="friend_of"
    )

Base.metadata.create_all(engine)

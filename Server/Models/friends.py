from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ORMDatabases import Base, engine

friendship_table = Table(
    'friendship', Base.metadata,
    Column('user_id', Integer, ForeignKey('LocalUser.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('LocalUser.id'), primary_key=True),
    Column('status', String(20), default='pending', onupdate='accepted')
)

class LocalUser(Base):
    __tablename__ = 'LocalUser'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(99), unique=True, index=True)

    friends = relationship(
        'LocalUser',
        secondary=friendship_table,
        primaryjoin=(id == friendship_table.c.user_id) & (friendship_table.c.status == 'accepted'),
        secondaryjoin=(id == friendship_table.c.friend_id) & (friendship_table.c.status == 'accepted'),
        backref="friend_of",
        overlaps="pending_requests"
    )

    sent_requests = relationship(
        'LocalUser',
        secondary=friendship_table,
        primaryjoin=(id == friendship_table.c.user_id) & (friendship_table.c.status == 'pending'),
        secondaryjoin=id == friendship_table.c.friend_id,
        backref="pending_requests",
        overlaps="friends, friend_of"
    )

Base.metadata.create_all(engine)

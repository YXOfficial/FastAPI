from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from ORMDatabases import Base, engine
class posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Creator = Column(String(50), nullable=False)
    title = Column(String(120))
    content = Column(String(120))
    email = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        nullable=True,
        default=None,
        onupdate=func.now(),
        server_onupdate=func.now()
    )
    share = Column(String(50), nullable=False)
    friendonly = Column(String(50), nullable=False)
Base.metadata.create_all(engine)

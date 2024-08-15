import sqlalchemy
from sqlalchemy.orm import sessionmaker
sqlalchemy.__version__
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
db_connector = 'mysql+mysqlconnector'

connection_string = f"{db_connector}://root:Khoa12345%40@localhost:3306/test"

engine = create_engine(connection_string, echo=True)
Session = sessionmaker(bind=engine)
db = Session()
Base = declarative_base()
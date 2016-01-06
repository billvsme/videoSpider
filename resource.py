from sqlalchemy.orm import sessionmaker
from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base 


engine = create_engine(
    config['database']['database_url'],
    echo=config['database'].getboolean('test') or False
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

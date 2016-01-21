from sqlalchemy.orm import sessionmaker
from config import config
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
        config['database']['database_url'],
        echo=config['database'].getboolean('test') or False,
        )

Session = sessionmaker(bind=engine)
session = Session()


Base.metadata.create_all(engine)

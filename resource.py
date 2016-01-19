from sqlalchemy.orm import sessionmaker
from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base 

import os
from sqlalchemy import event
from sqlalchemy import exc


engine = create_engine(
    config['database']['database_url'],
    echo=config['database'].getboolean('test') or False
)

@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    connection_record.info['pid'] = os.getpid()

@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    pid = os.getpid()
    if connection_record.info['pid'] != pid:
        connection_record.connection = connection_proxy.connection = None
        raise exc.DisconnectionError(
            "Connection record belongs to pid %s, "
            "attempting to check out in pid %s" %
            (connection_record.info['pid'], pid)
        )

Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

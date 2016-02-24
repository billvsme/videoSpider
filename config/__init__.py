import os
import sys

from celery import Celery
from whoosh import index
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer; analyzer = ChineseAnalyzer()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from celery.signals import worker_process_init
from sqlalchemy import event
from sqlalchemy import exc
from models import Base

if sys.version_info < (3, 0):
    import ConfigParser
    config = ConfigParser.ConfigParser()
else:
    import configparser
    config = configparser.ConfigParser()


config_path = './{}/config.ini'.format(__name__)
config_dev_path = './{}/config_dev.ini'.format(__name__)

# read config.ini file
if os.path.exists(config_path):
    config.read(config_path)
else:
    config.read(config_dev_path)


def create_new_engine():
    engine = create_engine(
            config.get('database', 'database_url'),
            echo=config.getboolean('database', 'test') or False
            )

    return engine

engine = create_new_engine()

Session = sessionmaker(bind=engine)
session = Session()

#Base.metadata.create_all(engine)


'''Why use a dict save engine and session?
Because using multiprocess, you should create new connection to database. 
In the begin, I see the
http://docs.sqlalchemy.org/en/latest/core/pooling.html#using-connection-pools-with-multiprocessing,
and use above approaches, but on the new process start, have some error.
'''
sqla = {
    'engine': engine,
    'session': session
}

@worker_process_init.connect
def new_process(signal, sender):
    engine = create_new_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    sqla['engine'] = engine
    sqla['session'] = session


# Celery
celery_app = Celery(
    'tasks',
    backend=config.get('celery', 'backend'),
    broker=config.get('celery', 'broker')
)

# Whoosh
schema = Schema(id_=ID(stored=True), title=TEXT(stored=True), summary=TEXT(stored=True, analyzer=analyzer))

exists = index.exists_in("indexdir")

if exists == True:
    ix = index.open_dir("indexdir")
else:
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = index.create_in("indexdir", schema=schema)

import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

if sys.version_info < (3, 0):
    import ConfigParser
    config = ConfigParser.ConfigParser()
else:
    import configparser
    config = configparser.ConfigParser()


config_dev_path = './{}/config.ini'.format(__name__)
config_path = './{}/config_dev.ini'.format(__name__)

# read config.ini file
if os.path.exists(config_path):
    config.read(config_path)
else:
    config.read(config_dev_path)


engine = create_engine(
        config.get('database', 'database_url'),
        echo=config.getboolean('database', 'test') or False
        )


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

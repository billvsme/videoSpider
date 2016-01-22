import os
import sys

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

import configparser
import os


config_dev_path = './{}/config.ini'.format(__name__)
config_path = './{}/config_dev.ini'.format(__name__)

# read config.ini file
config = configparser.ConfigParser()
if os.path.exists(config_path):
    config.read(config_path)
else:
    config.read(config_dev_path)

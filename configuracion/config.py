from configparser import ConfigParser
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def Config(section, filename='config.ini'):
    # Read config file
    parser = ConfigParser()
    parser.read(filename)

    # Read section
    config_param = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config_param[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config_param
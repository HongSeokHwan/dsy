import logging.config
import os
import json


def setup_logger(default_path = 'log.json', 
                default_level='logging.INFO', 
                env_key = 'LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as config_file:
            config = json.load(config_file)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
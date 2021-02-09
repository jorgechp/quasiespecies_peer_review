import configparser
from waitress import serve

from flaskr.api import launch_api

config = configparser.ConfigParser()
config.read('security/config.ini')
default_config = config['GENERAL']
security_config = config['SECURITY']
api_config = config['API']

app = launch_api(key=security_config['key'], cors_allowed=api_config['cors_allowed_origin'])

serve(app, host=default_config['host'], port=default_config['port'])
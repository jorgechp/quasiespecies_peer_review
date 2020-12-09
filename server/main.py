import configparser

from flaskr.api import launch_api

config = configparser.ConfigParser()
config.read('security/config.ini')
default_config = config['GENERAL']
security_config = config['SECURITY']

app = launch_api(key=security_config['key'])
app.run(host=default_config['host'],
        port=default_config['port'],
        debug=default_config['debug'])

import os
import configparser
from flask_cors import CORS

from flask import Flask
from flask import g

from . import db
from .captcha import construct_captcha_blueprint
from .train import construct_train_blueprint
from .user import construct_user_blueprint
from db.database_manager import DatabaseManager
from management.train_manager import TrainManager
from management.user_manager import UserManager


def launch_api(instance_path=None,test_config=None, key=None, cors_allowed='*') -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path)


    app.config.from_mapping(
        SECRET_KEY=key,
        DATABASE=os.path.join(app.instance_path, 'peer_review.db')
    )

    app.config['CORS_HEADERS'] = 'Content-Type'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.app_context().push()

    db.init_app(app)
    g.database_path = app.config['DATABASE']
    database_manager = DatabaseManager(db.get_db)
    user_manager = UserManager(database_manager, 'security/key')
    train_manager = TrainManager(database_manager)

    @app.before_request
    def before_request_func():
        g.database_path = app.config['DATABASE']



    #Enable CORS on all domains
    CORS(app, resources={r"/*": {"origins": "https://localhost/port"}})

    app.register_blueprint(construct_train_blueprint(train_manager, cors_allowed))
    app.register_blueprint(construct_user_blueprint(user_manager, cors_allowed))
    app.register_blueprint(construct_captcha_blueprint(config['SECURITY']['captcha_secret_key'], cors_allowed))

    return app


config = configparser.ConfigParser()
config.read('security/config.ini')
default_config = config['GENERAL']
security_config = config['SECURITY']
api_config = config['API']
app = launch_api(key=security_config['key'], cors_allowed=api_config['cors_allowed_origin'])
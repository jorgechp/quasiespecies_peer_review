import os

import sqlite3


from flask import Flask

from . import db, train


def launch_api(instance_path=None,test_config=None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_USERS=os.path.join(app.instance_path + "/db/", 'users.db'),
        DATABASE_ARTICLES=os.path.join(app.instance_path + "/db/", 'articles.sqlite')
    )

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

    db.init_app(app)

    app.register_blueprint(train.bp)



    return app

from flask_marshmallow import Marshmallow

__version__ = '0.1.0'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:Demian!89@localhost/specup",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=False
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # initialize db, schema
    db.init_app(app)
    ma.init_app(app)

    # register views
    from .users.views import UserView
    UserView.register(app)

    return app

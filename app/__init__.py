from flask import Flask, jsonify
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from app.queries import CustomBaseQuery

db = SQLAlchemy(query_class=CustomBaseQuery)
ma = Marshmallow()
lm = LoginManager()


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

    # import models
    from .users.models import User
    from .boards.models import Board
    from .posts.models import Post

    # initialize db, schema, login manager
    db.init_app(app)
    ma.init_app(app)
    lm.init_app(app)

    # register views
    from .users.views import UsersView
    from .boards.views import BoardsView
    from .posts.views import PostsView

    UsersView.register(app)
    BoardsView.register(app)
    PostsView.register(app)

    # @app.errorhandler(Exception)
    # def handle_error(error):
    #     response = jsonify(error.to_dict())
    #     response.status_code = error.status_code
    #     return response
    #

    @app.errorhandler(401)
    def handle_error(error):
        response = jsonify({'message': error.description})
        response.status_code = 401
        return response

    return app
